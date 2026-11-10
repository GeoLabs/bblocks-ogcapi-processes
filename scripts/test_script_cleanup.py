"""Offline regressions for parsing, annotation positions and cache/CLI state."""
import copy
import hashlib
import json
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import requests
import yaml

import audit_official_sources as source_map
import check_embedded_sources as verifier
import official_materializer as producer
import official_source_loader as loader
from build_official_sources import configure_yaml


class AnnotationTests(unittest.TestCase):
    def test_strict_single_mapping_parser(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / 'schema.yaml'
            for text in ('{}\n---\n{}\n', 'properties:\n\tbroken: true\n',
                         '{}\n# Official definition embedded by scripts/align_official_sources.py.\ntype: object\n',
                         '[1, 2]\n'):
                with self.subTest(text=text):
                    target.write_text(text)
                    with self.assertRaises((TypeError, ValueError, yaml.YAMLError)):
                        producer.existing_annotations(target)
            target.write_text('type: string\nx-jsonld-id: "urn:test"\n')
            self.assertEqual(producer.existing_annotations(target)['x-jsonld-id'], 'urn:test')

    def test_preserve_nested_annotations_without_changing_constraints(self):
        value = {'properties': {'a': {'type': 'string'}}, 'additionalProperties': {'minimum': 1}}
        original = copy.deepcopy(value)
        original['x-jsonld-prefixes'] = {'test': 'urn:test:'}
        original['x-jsonld-extra-terms'] = {'test': {'x-jsonld-id': 'urn:test'}}
        original['properties']['a']['x-jsonld-id'] = 'urn:a'
        original['additionalProperties']['x-jsonld-type'] = '@id'
        producer.preserve_jsonld(value, original)
        self.assertEqual(value, original)
        original['properties']['a']['x-jsonld-id'] = 'urn:other'
        self.assertEqual(value['properties']['a']['x-jsonld-id'], 'urn:a')

    def test_unchanged_annotated_list_and_reference_mapping(self):
        source = source_map.V1 + 'test.yaml'
        index = {source: 'bblocks://test'}
        old = {'allOf': [{'$ref': 'test.yaml', 'x-jsonld-id': 'urn:a'}]}
        new = {'allOf': [{'$ref': 'bblocks://test'}]}
        producer.preserve_jsonld(new, producer.rewrite(old, source, index, source))
        self.assertEqual(new['allOf'][0]['x-jsonld-id'], 'urn:a')

    def test_changed_annotated_lists_fail_instead_of_zip(self):
        old = {'oneOf': [{'type': 'string', 'x-jsonld-id': 'urn:a'}, {'type': 'number'}]}
        for values in ([{'type': 'number'}, {'type': 'string'}],
                       [{'type': 'string'}],
                       [{'type': 'string'}, {'type': 'number'}, {'type': 'boolean'}],
                       [{'type': 'string', 'minLength': 1}, {'type': 'number'}]):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, 'Annotated list changed.*reconcile'):
                producer.preserve_jsonld({'oneOf': values}, old)

    def test_deleted_or_retyped_annotated_nodes_fail(self):
        old = {'properties': {'a': {'x-jsonld-id': 'urn:a'}}}
        for new in ({'properties': {}}, {'properties': {'a': False}}):
            with self.assertRaisesRegex(ValueError, 'reconcile'):
                producer.preserve_jsonld(new, old)

    def normalized(self, value, block='schemas/test'):
        return verifier.normalized(value, {'block': block, 'source': 'https://example.test/schema.yaml'}, {})

    def test_only_exact_schema_annotation_keys_ignored(self):
        self.assertEqual(self.normalized({'type': 'string', 'x-jsonld-id': 'urn:a'}), {'type': 'string'})
        for key in ('x-jsonld', 'x-jsonldFake', 'x-jsonld-id-extra'):
            self.assertEqual(self.normalized({key: 'data'}), {key: 'data'})

    def test_named_schema_properties_and_instance_data_not_ignored(self):
        for keyword in ('properties', 'patternProperties', '$defs', 'definitions', 'dependentSchemas'):
            for name in ('x-jsonld-id', 'x-jsonld-field', 'x-jsonldFake'):
                original = {keyword: {name: {'type': 'string'}}}
                mutated = copy.deepcopy(original)
                mutated[keyword][name]['type'] = 'number'
                self.assertNotEqual(self.normalized(original), self.normalized(mutated))
        for keyword in ('default', 'const', 'enum', 'examples'):
            value = {keyword: {'x-jsonld-id': {'schema': {'x-jsonld-type': 'data'}}}}
            self.assertEqual(self.normalized(value), value)

    def test_check_rejects_mutated_actual_x_jsonld_named_properties(self):
        with TemporaryDirectory() as directory:
            metadata = Path(directory) / 'bblock.json'
            metadata.write_text('{}')
            plan = {'id': 'bblocks://ogc.api.processes.part1.v1.schemas.test',
                    'block': 'schemas/test', 'version': 'v1', 'metadata': metadata,
                    'source': 'https://example.test/test.yaml'}
            for name in ('x-jsonld-id', 'x-jsonld-field', 'x-jsonldFake'):
                original = {'properties': {name: {'type': 'string'}}}
                for mutated in ({'properties': {}}, {'properties': {name: {'type': 'number'}}}):
                    with self.subTest(name=name, mutated=mutated), \
                            patch.object(verifier, 'artifact', return_value=SimpleNamespace(
                                read_text=lambda: yaml.safe_dump(mutated))), \
                            patch.object(verifier, 'load', return_value=original):
                        errors, _ = verifier.check([plan.copy()])
                        self.assertTrue(any(error['block'] == plan['id']
                                            and 'differs from official' in error['error']
                                            for error in errors), errors)

    def test_schema_keywords_including_additional_properties(self):
        for keyword in ('additionalProperties', 'additionalItems', 'unevaluatedProperties',
                        'items', 'not', 'if', 'then', 'else', 'contains', 'propertyNames', 'contentSchema'):
            value = {keyword: {'x-jsonld-id': 'urn:a', 'minimum': 1,
                               'properties': {'x-jsonld-id': {'type': 'string'}}}}
            normalized = self.normalized(value)
            self.assertNotIn('x-jsonld-id', normalized[keyword])
            self.assertIn('x-jsonld-id', normalized[keyword]['properties'])
            mutated = copy.deepcopy(value)
            mutated[keyword]['minimum'] = 2
            self.assertNotEqual(normalized, self.normalized(mutated))

    def test_named_openapi_components_and_payloads_preserved(self):
        value = {'components': {'schemas': {'x-jsonld-id': {
            'type': 'string', 'x-jsonld-id': 'urn:annotation'}}},
            'paths': {'/': {'get': {'responses': {'200': {'content': {'application/json': {
                'schema': {'additionalProperties': {'x-jsonld-type': '@id', 'type': 'string'}},
                'example': {'x-jsonld-id': 'payload'}}}}}}}}}
        actual = self.normalized(value, 'api')
        self.assertIn('x-jsonld-id', actual['components']['schemas'])
        self.assertNotIn('x-jsonld-id', actual['components']['schemas']['x-jsonld-id'])
        content = actual['paths']['/']['get']['responses']['200']['content']['application/json']
        self.assertEqual(content['example'], {'x-jsonld-id': 'payload'})
        self.assertEqual(content['schema']['additionalProperties'], {'type': 'string'})
        mutated = copy.deepcopy(value)
        mutated['components']['schemas'].pop('x-jsonld-id')
        self.assertNotEqual(actual, self.normalized(mutated, 'api'))


class CacheTests(unittest.TestCase):
    def response(self, text):
        return SimpleNamespace(content=text.encode(), raise_for_status=lambda: None)

    def test_missing_then_snapshot_then_explicit_refresh(self):
        with TemporaryDirectory() as directory:
            cache = loader.SourceCache(directory)
            url = source_map.V1 + 'test.yaml'
            with patch('requests.get', return_value=self.response('value: old')) as get:
                self.assertEqual(cache.load(url), {'value': 'old'})
                self.assertEqual(cache.load(url), {'value': 'old'})
                get.assert_called_once_with(url, timeout=90)
            with patch('requests.get', return_value=self.response('value: new')) as get:
                self.assertEqual(loader.SourceCache(directory).load(url), {'value': 'old'})
                refreshed = loader.SourceCache(directory, refresh=True)
                self.assertEqual(refreshed.load(url + '#/value'), 'new')
                self.assertEqual(refreshed.load(url), {'value': 'new'})
                get.assert_called_once()

    def test_refresh_pinned_url_does_not_move_pin(self):
        with TemporaryDirectory() as directory, patch('requests.get', return_value=self.response('type: string')) as get:
            url = source_map.V2 + 'schema.yaml'
            loader.SourceCache(directory, refresh=True).load(url)
            get.assert_called_once_with(url, timeout=90)
            self.assertIn(source_map.PIN, url)

    def test_failed_refresh_does_not_fall_back_to_stale_cache(self):
        with TemporaryDirectory() as directory:
            url = 'https://example.test/test.yaml'
            with patch('requests.get', return_value=self.response('type: string')):
                loader.SourceCache(directory).load(url)
            before = next(Path(directory).rglob('*.yaml')).read_bytes()
            with patch('requests.get', side_effect=requests.ConnectionError('unavailable')):
                with self.assertRaises(requests.ConnectionError):
                    loader.SourceCache(directory, refresh=True).load(url)
            self.assertEqual(next(Path(directory).rglob('*.yaml')).read_bytes(), before)

    def test_offline_miss_and_conflicting_modes(self):
        with TemporaryDirectory() as directory, patch('requests.get') as get:
            with self.assertRaisesRegex(ValueError, 'Offline cache miss'):
                loader.SourceCache(directory, offline=True).load('https://example.test/missing')
            get.assert_not_called()
        with self.assertRaises(ValueError):
            loader.configure_cache(refresh=True, offline=True)

    def test_cache_supports_fragment_lists_escaped_tokens_and_equals(self):
        with TemporaryDirectory() as directory, patch('requests.get', return_value=self.response('a/b~c: [=]')):
            self.assertEqual(loader.SourceCache(directory).load('https://example.test/a#/a~1b~0c/0'), '=')

    def test_cli_output_propagates_through_named_imports(self):
        def discovery(plans):
            producer.load('https://example.test/discovery')
            return plans

        def check(plans):
            verifier.load('https://example.test/check')
            return [], {}

        def response(url, **kwargs):
            kind = 'array' if url.startswith(source_map.V1) else 'integer'
            return self.response('schema: {type: ' + kind + '}')

        old_cache = loader._cache
        try:
            with TemporaryDirectory() as directory, \
                    patch('sys.argv', ['audit_official_sources.py', '--output', directory, '--refresh']), \
                    patch.object(producer, 'inventory', return_value=[]), \
                    patch.object(producer, 'discover', side_effect=discovery), \
                    patch.object(verifier, 'check', side_effect=check), \
                    patch('requests.get', side_effect=response) as get:
                with patch('builtins.print'), self.assertRaises(SystemExit) as result:
                    runpy.run_path(str(Path(source_map.__file__)), run_name='__main__')
                self.assertEqual(result.exception.code, False)
                self.assertEqual(loader._cache.output, Path(directory))
                for call in get.call_args_list:
                    url = call.args[0]
                    digest = hashlib.sha256(url.encode()).hexdigest()
                    self.assertTrue((Path(directory) / 'http' / (digest + '.yaml')).is_file())
                self.assertEqual(get.call_count, 6)
                report = json.loads((Path(directory) / 'report.json').read_text())
                self.assertEqual(report['cache_mode'], 'refresh')
        finally:
            loader._cache = old_cache


class AdapterTests(unittest.TestCase):
    def test_adapter_preserves_scalar_and_constraints(self):
        # Restore constructors: the adapter must not leak global changes to other tests.
        loaders = [getattr(yaml, name) for name in ('SafeLoader', 'CSafeLoader', 'FullLoader', 'CFullLoader')
                   if hasattr(yaml, name)]
        originals = [dict(cls.yaml_constructors) for cls in loaders]
        try:
            configure_yaml()
            for cls in loaders:
                self.assertEqual(yaml.load('enum: [=]\nminimum: 0\nexclusiveMinimum: true', Loader=cls),
                                 {'enum': ['='], 'minimum': 0, 'exclusiveMinimum': True})
        finally:
            for cls, constructors in zip(loaders, originals):
                cls.yaml_constructors = constructors