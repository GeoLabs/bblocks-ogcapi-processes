"""Source-level regressions; run with unittest, no Docker or spec generator.

Mutation tests modify only in-memory documents, not repository fixtures.
"""
import copy
import json
import os
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import urldefrag

import jsonschema
import yaml

import check_embedded_sources as audit
from audit_official_sources import ROOT, V1, V2, source_for
from official_materializer import (DRAFT4, artifact, discover, embedded,
                                   canonical_index, has_boolean_exclusive_bound,
                                   inventory, mapped_reference, rendered_files, rewrite,
                                   canonical_name)


class MetadataTests(unittest.TestCase):
    def test_v1_metadata_is_two_space_indented_json_with_final_newline(self):
        for target in sorted((ROOT / '_sources/part1/v1').rglob('bblock.json')):
            with self.subTest(metadata=str(target.relative_to(ROOT))):
                text = target.read_text()
                self.assertEqual(text, json.dumps(json.loads(text), indent=2,
                                                  ensure_ascii=False) + '\n')

    def test_exact_name_cleanup_preserves_meaningful_identifiers(self):
        cases = {
            'limit parameter': 'limit', 'Job result path': 'Job result',
            'ProcessDescription response': 'ProcessDescription',
            'schema schema': 'schema', 'Schema for timeStamp schema': 'timeStamp',
            'Official schemas/processes-core/apis': 'apis',
            'Official responses/common-core/rAPI': 'rAPI',
            'Official parameters/unspecified/f-metadata': 'f-metadata',
            'Official operations/oProcessList': 'oProcessList',
            'Official parameters/processes-core/response': 'response',
            'schema': 'schema', 'response': 'response', 'Dismiss Job': 'Dismiss Job',
            'OGC API - Processes: Part 1': 'OGC API - Processes: Part 1',
            'processIdPathParam': 'processIdPathParam',
            'schemaAndOccurrences': 'schemaAndOccurrences',
            'responseCollection': 'responseCollection', 'rEmpty': 'rEmpty',
        }
        for original, expected in cases.items():
            with self.subTest(name=original):
                self.assertEqual(canonical_name(original), expected)
                self.assertEqual(canonical_name(expected), expected)

    def test_all_175_metadata_names_and_editions_without_network(self):
        plans = inventory()
        self.assertEqual(Counter(p['version'] for p in plans), {'v1': 73, 'v2': 102})
        with patch('official_materializer.embedded', return_value={}), \
                patch('requests.get', side_effect=AssertionError('Unexpected network request')):
            files = rendered_files(plans)
        for plan in plans:
            with self.subTest(block=plan['id']):
                actual = json.loads(plan['metadata'].read_text())
                self.assertEqual(actual['version'], {'v1': '1.0', 'v2': '2.0'}[plan['version']])
                self.assertEqual(actual['name'], canonical_name(actual['name']))
                self.assertFalse(actual['name'].startswith(('Official ', 'Schema for ')))
                self.assertFalse(actual['name'].endswith(
                    (' parameter', ' path', ' response', ' schema')))
                self.assertEqual(json.loads(files[plan['metadata']]), actual)

    def test_existing_and_future_metadata_preserve_other_fields_offline(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            for edition, version in (('v1', '1.0'), ('v2', '2.0')):
                for block, expected in (
                        ('schemas/future/schema', 'schema'),
                        ('responses/future/rAPI', 'rAPI'),
                        ('parameters/future/response', 'response'),
                        ('operations/oFuture', 'oFuture')):
                    with self.subTest(edition=edition, block=block):
                        target = Path(directory) / edition / block / 'bblock.json'
                        plan = {'version': edition, 'block': block, 'metadata': target,
                                'source': 'https://example.test/official.yaml'}
                        with patch('official_materializer.embedded', return_value={}), \
                                patch('requests.get', side_effect=AssertionError('Unexpected network request')):
                            new = json.loads(rendered_files([plan])[target])
                            self.assertEqual(new['name'], expected)
                            self.assertEqual(new['version'], version)
                            self.assertIn('part1-' + edition, new['tags'])
                            original = {**new, 'name': 'Official ' + block,
                                        'version': '0.1', 'custom': {'keep': [True, 1, 'é']}}
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_text(json.dumps(original))
                            before = target.read_bytes()
                            actual = json.loads(rendered_files([plan])[target])
                        self.assertEqual(actual, {**original, 'name': expected, 'version': version})
                        self.assertEqual(target.read_bytes(), before)


class ReferenceProducerTests(unittest.TestCase):
    def test_self_references_use_canonical_artifacts_and_keep_pointers(self):
        document = V1 + 'schemas/schema.yaml'
        canonical = 'bblocks://ogc.api.processes.part1.v1.schemas.schema'
        fragment_source = document + '#/definitions/node'
        fragment_id = canonical + '.node'
        index = {document: canonical, fragment_source: fragment_id}
        for reference, base, expected in (
                ('schema.yaml', document, canonical),
                ('#', document, canonical),
                (document, document, canonical),
                ('#/properties/child', document, canonical + '#/properties/child'),
                ('schema.yaml#/properties/a~1b~0c', document,
                 canonical + '#/properties/a~1b~0c'),
                (fragment_source, fragment_source, fragment_id),
                ('#/definitions/node', fragment_source, fragment_id),
                ('#/definitions/node/properties/child', fragment_source,
                 fragment_id + '#/properties/child'),
                ('#/definitions/node/properties/a~1b~0c', fragment_source,
                 fragment_id + '#/properties/a~1b~0c'),
                # A fragment-only ref is relative to the source document,
                # not to the extracted subtree: never discard its pointer.
                ('#/properties/other', fragment_source, canonical + '#/properties/other'),
                ('#/definitions/nodeSibling', fragment_source,
                 canonical + '#/definitions/nodeSibling'),
                ('#', fragment_source, canonical)):
            with self.subTest(reference=reference, base=base):
                # urljoin preserves an empty '#' on Python 3.14, unlike 3.12;
                # compare URI targets without discarding nonempty pointers.
                self.assertEqual(urldefrag(mapped_reference(reference, base, index, base)),
                                 urldefrag(expected))
        # A same-document target outside the represented subtree stays official.
        self.assertEqual(mapped_reference('#/properties/other', fragment_source,
                                          {fragment_source: fragment_id}, fragment_source),
                         document + '#/properties/other')

    def test_self_source_alias_uses_canonical_id_in_its_own_edition(self):
        source = V1 + 'schemas/schema.yaml'
        for version in ('v1', 'v2'):
            canonical = 'bblocks://ogc.api.processes.part1.' + version + '.schemas.schema'
            plans = [
                {'version': version, 'block': 'schemas/alias', 'source': source,
                 'classification': 'compatibility-alias', 'id': canonical + '.alias'},
                {'version': version, 'block': 'schemas/schema', 'source': source,
                 'classification': 'official', 'id': canonical},
                {'version': 'other', 'block': 'schemas/schema', 'source': source,
                 'classification': 'official', 'id': 'bblocks://wrong-edition'},
            ]
            index = canonical_index(plans, version)
            value = {'items': {'$ref': 'schema.yaml#/properties/child'}}
            self.assertEqual(rewrite(value, source, index, source),
                             {'items': {'$ref': canonical + '#/properties/child'}})
            self.assertEqual(value['items']['$ref'], 'schema.yaml#/properties/child')


class DialectProducerTests(unittest.TestCase):
    def test_only_undeclared_schema_with_boolean_bound_gets_draft4(self):
        legacy = {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True}
        for document, block, expected in (
                (legacy, 'schemas/test', DRAFT4),
                ({'maximum': 10, 'exclusiveMaximum': False}, 'schemas/test', DRAFT4),
                ({'allOf': [legacy]}, 'schemas/test', DRAFT4),
                ({'properties': {'exclusiveMinimum': {'type': 'boolean'}}}, 'schemas/test', None),
                ({'default': legacy, 'enum': [legacy], 'examples': [legacy]}, 'schemas/test', None),
                ({'exclusiveMinimum': 0}, 'schemas/test', None),
                ({'$schema': 'https://json-schema.org/draft/2020-12/schema', **legacy},
                 'schemas/test', 'https://json-schema.org/draft/2020-12/schema'),
                ({'schema': legacy}, 'parameters/test', None)):
            with self.subTest(document=document, block=block):
                plan = {'version': 'v1', 'block': block, 'source': V1 + 'test.yaml'}
                original = copy.deepcopy(document)
                with patch('official_materializer.official_document', return_value=document):
                    result = embedded(plan, [])
                    self.assertEqual(result, embedded(plan, []))
                self.assertEqual(result.get('$schema'), expected)
                self.assertEqual(document, original)
                self.assertEqual(audit.expected_dialect(plan, original),
                                 DRAFT4 if expected == DRAFT4 else None)
                if '$schema' not in original and expected:
                    result.pop('$schema')
                self.assertEqual(result, original)


@unittest.skipUnless(os.environ.get('OFFICIAL_SOURCE_TESTS') == '1',
                     'Source integration tests require OFFICIAL_SOURCE_TESTS=1 (cache/network)')
class EmbeddedSourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plans = inventory()

    def mutated_errors(self, version, block, mutate):
        real_artifact = artifact

        def altered(plan):
            target = real_artifact(plan)
            if plan['version'] == version and plan['block'] == block:
                value = yaml.safe_load(target.read_text())
                mutate(value)
                return SimpleNamespace(read_text=lambda: yaml.safe_dump(value, sort_keys=False))
            return target

        with patch.object(audit, 'artifact', altered):
            errors, _ = audit.check(copy.deepcopy(self.plans))
        return errors

    def test_independent_official_comparison_and_api_graphs(self):
        errors, graphs = audit.check(copy.deepcopy(self.plans))
        self.assertEqual(errors, [])
        for version in ('v1', 'v2'):
            self.assertEqual(graphs[version]['direct_path_blocks'], 9)
            for kind in ('parameters', 'responses', 'schemas'):
                self.assertGreater(graphs[version]['reachable_by_kind'][kind], 0)
        self.assertEqual(graphs['v2']['reachable_by_kind']['operations'], 2)

    def test_inventory_remains_closed_after_discovery(self):
        self.assertEqual({p['id'] for p in discover(self.plans)},
                         {p['id'] for p in self.plans})
        for plan in self.plans:
            self.assertEqual(source_for(plan['version'], plan['block'])[0], plan['source'])

    def test_new_operation_and_group_source_mapping(self):
        for block, suffix in (
                ('operations/oJobResults', 'paths/processes-core/operations/oJobResults.yaml'),
                ('schemas/processes-core/values', 'schemas/processes-core/values.yaml'),
                ('schemas/common-core/link', 'schemas/common-core/link.yaml'),
                ('parameters/unspecified/f-metadata', 'parameters/unspecified/f-metadata.yaml'),
                ('responses/common-core/rAPI', 'responses/common-core/rAPI.yaml')):
            self.assertEqual(source_for('v2', block), (V2 + suffix, 'official'))
        with self.assertRaises(ValueError):
            source_for('v3', 'api')

    def test_external_value_is_absolutized_not_mapped_to_bblock(self):
        source = V1 + 'responses/ProcessDescription.yaml'
        expected = V1.removesuffix('openapi/') + 'examples/json/ProcessDescription.json'
        value = {'examples': [{'externalValue': '../../examples/json/ProcessDescription.json'}]}
        self.assertEqual(rewrite(value, source, {expected: 'bblocks://invalid'}, None),
                         {'examples': [{'externalValue': expected}]})

    def test_rendered_artifacts_are_single_space_indented_yaml(self):
        for target, text in rendered_files(self.plans).items():
            if target.suffix != '.yaml':
                continue
            self.assertNotIn('\t', text, str(target))
            self.assertNotIn('\n{', text, str(target))
            self.assertEqual(len(list(yaml.safe_load_all(text))), 1, str(target))
            self.assertIsInstance(yaml.safe_load(text), dict)

    def test_openapi_has_no_generated_header_but_schemas_keep_it(self):
        header = '# Official definition embedded by scripts/align_official_sources.py.\n'
        for target, text in rendered_files(self.plans).items():
            if target.name not in ('openapi.yaml', 'schema.yaml'):
                continue
            with self.subTest(artifact=str(target.relative_to(ROOT))):
                if target.name == 'openapi.yaml':
                    self.assertNotIn(header, text)
                    self.assertFalse(target.read_bytes().startswith(header.encode()))
                else:
                    self.assertTrue(text.startswith(header))
                    self.assertTrue(target.read_bytes().startswith(header.encode()))

    def test_rendered_metadata_is_multiline_json(self):
        for target, text in rendered_files(self.plans).items():
            if target.name == 'bblock.json':
                with self.subTest(metadata=str(target.relative_to(ROOT))):
                    self.assertEqual(text, json.dumps(json.loads(text), indent=2,
                                                      ensure_ascii=False) + '\n')

    def test_all_actual_artifacts_match_producer_without_local_self_refs(self):
        files = rendered_files(self.plans)
        for target in sorted((ROOT / '_sources').rglob('*.yaml')):
            if target.name not in ('schema.yaml', 'openapi.yaml'):
                continue
            with self.subTest(artifact=str(target.relative_to(ROOT))):
                actual = yaml.safe_load(target.read_text())
                self.assertEqual(actual, yaml.safe_load(files[target]))
                self.assertFalse(any(ref.startswith('#') for ref in audit.refs(actual)))
        plan = next(p for p in self.plans
                    if p['version'] == 'v1' and p['block'] == 'schemas/schema')
        self.assertEqual(list(audit.refs(yaml.safe_load(artifact(plan).read_text())))
                         .count(plan['id']), 7)

    def test_all_artifacts_scanned_for_boolean_bounds_and_draft4_validity(self):
        # Exhaustive scan, not a three-file whitelist: catch future/orphan
        # artifacts too. Inspect raw trees independently of the producer.
        def boolean_bounds(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in ('exclusiveMinimum', 'exclusiveMaximum') and type(child) is bool:
                        yield key, child
                    yield from boolean_bounds(child)
            elif isinstance(value, list):
                for child in value:
                    yield from boolean_bounds(child)

        found = set()
        files = rendered_files(self.plans)
        for target in sorted((ROOT / '_sources').rglob('*.yaml')):
            if target.name not in ('schema.yaml', 'openapi.yaml'):
                continue
            schema = yaml.safe_load(target.read_text())
            if target.name == 'schema.yaml':
                jsonschema.validators.validator_for(schema).check_schema(schema)
            if not list(boolean_bounds(schema)):
                continue
            relative = str(target.relative_to(ROOT / '_sources/part1'))
            found.add(relative)
            with self.subTest(artifact=relative):
                self.assertEqual(schema['$schema'], DRAFT4)
                self.assertIs(jsonschema.validators.validator_for(schema), jsonschema.Draft4Validator)
                jsonschema.Draft4Validator.check_schema(schema)
                self.assertEqual(files[target], target.read_text())
                # Exercise the actual bound, without dereferencing unrelated
                # official resources: zero/negative/boolean must stay rejected.
                bound = schema['oneOf'][1]['properties']['multipleOf']
                validator = jsonschema.Draft4Validator(bound)
                self.assertTrue(validator.is_valid(0.5))
                for invalid in (0, -1, True):
                    self.assertFalse(validator.is_valid(invalid))
        self.assertEqual(found, {'v1/schemas/schema/schema.yaml',
                                 'v1/schemas/swagger/schema/schema.yaml',
                                 'v2/schemas/swagger/schema/schema.yaml'})
        for plan in self.plans:
            if plan['version'] == 'v2' and plan['block'] in ('schemas/schema', 'schemas/processes-core/schema'):
                schema = yaml.safe_load(artifact(plan).read_text())
                self.assertNotIn('$schema', schema)
                self.assertFalse(has_boolean_exclusive_bound(schema))

    def test_audit_rejects_dialect_and_legacy_constraint_mutations(self):
        def multiple_of(value):
            return value['oneOf'][1]['properties']['multipleOf']

        mutations = (
            lambda value: value.pop('$schema'),
            lambda value: value.update({'$schema': 'https://json-schema.org/draft/2020-12/schema'}),
            lambda value: multiple_of(value).pop('exclusiveMinimum'),
            lambda value: multiple_of(value).update({'exclusiveMinimum': False}),
            lambda value: multiple_of(value).update({'exclusiveMinimum': 1}),
            lambda value: multiple_of(value).pop('minimum'),
            lambda value: multiple_of(value).update({'$schema': DRAFT4}),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                errors = self.mutated_errors('v1', 'schemas/schema', mutate)
                self.assertTrue(any('differs from official' in e['error'] for e in errors), errors)
        errors = self.mutated_errors('v2', 'schemas/schema',
                                     lambda value: value.update({'$schema': DRAFT4}))
        self.assertTrue(any('differs from official' in e['error'] for e in errors), errors)

    def test_new_metadata_has_required_fields_and_supported_classes(self):
        # Contract from the postprocessor's bblock metadata schema. Force the
        # creation branch: checked-in metadata must not mask producer defects.
        schema = {
            'type': 'object',
            'required': ['name', 'status', 'dateTimeAddition', 'itemClass', 'version',
                         'dateOfLastChange'],
            'properties': {
                'name': {'type': 'string'},
                'status': {'enum': ['under-development']},
                'version': {'type': 'string'},
                'dateTimeAddition': {'type': 'string', 'format': 'date-time'},
                'dateOfLastChange': {'type': 'string', 'format': 'date'},
                'itemClass': {'enum': ['schema', 'datatype', 'path', 'parameter',
                                      'header', 'cookie', 'response', 'api', 'model',
                                      'requirements-class', 'clause', 'terms', 'references']},
            },
        }
        exists = Path.exists
        with patch.object(Path, 'exists', lambda target:
                          False if target.name == 'bblock.json' else exists(target)):
            files = rendered_files(self.plans)
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker())
        for plan in self.plans:
            with self.subTest(block=plan['id']):
                text = files[plan['metadata']]
                md = json.loads(text)
                self.assertEqual(list(validator.iter_errors(md)), [])
                self.assertEqual(md['dateTimeAddition'], '2026-11-10T00:00:00Z')
                self.assertEqual(md['dateOfLastChange'], '2026-11-10')
                self.assertEqual(text, json.dumps(md, indent=2) + '\n')
                if plan['block'].startswith('operations/'):
                    self.assertEqual(md['itemClass'], 'model')

    def test_checked_in_metadata_has_required_dates(self):
        for plan in self.plans:
            with self.subTest(block=plan['id']):
                md = json.loads(plan['metadata'].read_text())
                self.assertTrue(md['dateTimeAddition'])
                self.assertTrue(md['dateOfLastChange'])

    def test_official_constraint_mutation_is_rejected(self):
        errors = self.mutated_errors('v2', 'schemas/processList',
                                     lambda value: value['required'].remove('links'))
        self.assertTrue(any('differs from official' in e['error'] for e in errors), errors)

    def test_cross_edition_graph_edge_is_rejected(self):
        errors = self.mutated_errors('v2', 'api', lambda value:
            value['paths']['/'].update({'$ref': 'bblocks://ogc.api.processes.part1.v1.paths.LandingPage'}))
        self.assertTrue(any('Cross-edition' in e['error'] for e in errors), errors)

    def test_missing_api_path_is_rejected(self):
        errors = self.mutated_errors('v2', 'api', lambda value: value['paths'].pop('/processes'))
        self.assertTrue(any(e['error'] == 'API graph incomplete' for e in errors), errors)

    def test_relative_external_value_is_rejected(self):
        errors = self.mutated_errors('v1', 'responses/ProcessDescription', lambda value:
            value['content']['application/json']['examples']['processDecription'].update(
                {'externalValue': '../../examples/json/ProcessDescription.json'}))
        self.assertTrue(any('Non-absolute externalValue' in e['error'] for e in errors), errors)

    def test_local_duration_parameter_types(self):
        for plan in self.plans:
            if plan['block'] not in ('parameters/minDuration', 'parameters/maxDuration'):
                continue
            schema = yaml.safe_load(artifact(plan).read_text())['schema']
            validator = jsonschema.Draft7Validator(schema)
            self.assertEqual(validator.is_valid(5), plan['version'] == 'v2')
            self.assertEqual(validator.is_valid([5]), plan['version'] == 'v1')
            self.assertFalse(validator.is_valid('5'))

    def test_local_process_lists_require_links(self):
        for plan in self.plans:
            if plan['block'] == 'schemas/processList':
                schema = yaml.safe_load(artifact(plan).read_text())
                validator = jsonschema.Draft7Validator(schema)
                self.assertTrue(validator.is_valid({'processes': [], 'links': []}))
                self.assertFalse(validator.is_valid({'processes': []}))


if __name__ == '__main__':
    unittest.main()