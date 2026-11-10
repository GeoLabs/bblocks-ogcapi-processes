"""Embed official documents, routing represented references within one edition.

Only references, the documented Part 1 path selection and Job method views
change. SourceLoader preserves the upstream bare '=' scalar. Planning is
read-only; align_official_sources emits reviewable patches for source changes.
"""
import copy
import json
from pathlib import Path
from urllib.parse import urldefrag, urljoin

import yaml
from audit_official_sources import PATHS, ROOT, V2, V2_PATHS, load, refs, source_for
from schema_annotations import JSONLD_KEYS, child_context

PREFIX = 'bblocks://ogc.api.processes.part1.'
METHODS = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
DRAFT4 = 'http://json-schema.org/draft-04/schema#'


def has_boolean_exclusive_bound(schema):
    """Inspect schema positions, not instance data or keyword property names."""
    if not isinstance(schema, dict):
        return False
    if any(isinstance(schema.get(key), bool)
           for key in ('exclusiveMinimum', 'exclusiveMaximum')):
        return True
    children = []
    for key in ('properties', 'patternProperties', 'definitions', '$defs',
                'dependencies', 'dependentSchemas'):
        value = schema.get(key, {})
        if isinstance(value, dict):
            children.extend(value.values())
    for key in ('allOf', 'anyOf', 'oneOf', 'prefixItems'):
        children.extend(schema.get(key, []))
    for key in ('items', 'additionalItems', 'additionalProperties', 'not',
                'contains', 'propertyNames', 'if', 'then', 'else',
                'unevaluatedItems', 'unevaluatedProperties'):
        value = schema.get(key)
        children.extend(value if isinstance(value, list) else [value])
    return any(has_boolean_exclusive_bound(child) for child in children)


def identifier(version, relative):
    return PREFIX + version + '.' + relative.replace('/', '.')


def inventory(root=ROOT):
    plans = []
    for metadata in sorted((root / '_sources/part1').rglob('bblock.json')):
        version, *parts = metadata.parent.relative_to(root / '_sources/part1').parts
        relative = '/'.join(parts)
        source, classification = source_for(version, relative)
        plans.append({'version': version, 'block': relative, 'source': source,
                      'classification': classification,
                      'id': identifier(version, relative), 'metadata': metadata})
    return plans


def official_document(plan):
    """The official object, with only the declared edition/path projection."""
    value = copy.deepcopy(load(plan['source']))
    if plan['block'] in ('paths/Job', 'paths/DismissJob'):
        method = 'get' if plan['block'] == 'paths/Job' else 'delete'
        value = {k: v for k, v in value.items() if k not in METHODS or k == method}
    elif plan['block'] == 'api' and plan['version'] == 'v2':
        # Retain actual upstream info, servers, definitions and components.
        # The root paths also contain Parts 2, 3 and 4: select Part 1 only.
        value['paths'] = {
            PATHS[name].replace('{jobId}', '{jobID}'): {'$ref': V2 + 'paths/' + target + '.yaml'}
            for name, target in V2_PATHS.items()}
        # No separate historical identifier: embed the official /api Path Item.
        value['paths']['/api'] = rewrite(load(V2 + 'paths/common-core/pAPI.yaml'),
                                        V2 + 'paths/common-core/pAPI.yaml', {}, None)
        # All selected Path Items reference standalone official files; none
        # uses the multipart root's component catalogue (mostly CWL/PROV).
        # Keep a root component only if a selected path actually references it.
        component_refs = {r.split('/')[2] for r in refs(value['paths'])
                  if r.startswith('#/components/')}
        value['components'] = {kind: items for kind, items in value.get('components', {}).items()
                       if kind in component_refs}
    return value


def canonical_index(plans, version):
    """Prefer canonical names over aliases; never use another edition."""
    index = {}
    candidates = [p for p in plans if p['version'] == version
                  and p['classification'] != 'operation-view']
    for plan in sorted(candidates, key=lambda p: (
            p['classification'] == 'compatibility-alias', p['block'].count('/'), p['block'])):
        index.setdefault(plan['source'], plan['id'])
    return index


def mapped_reference(reference, base, index, self_source):
    absolute = urljoin(base, reference)
    # Legacy v1-only blocks under v2 may depend on official v1 resources,
    # but must never depend on v1-namespace building blocks.
    for source in sorted(index, key=len, reverse=True):
        suffix = ''
        if absolute != source:
            if '#' not in source and absolute.startswith(source + '#'):
                suffix = absolute[len(source):]
            elif '#' in source and absolute.startswith(source + '/'):
                suffix = '#' + absolute[len(source):]
            else:
                continue
        if source == self_source:
            # Keep represented recursion external to the source artifact:
            # the annotator descends local '#' before marking the ref visited.
            # suffix is already relative to this represented source, including
            # when the source itself is an extracted JSON Pointer subtree.
            return index[source] + suffix
        return index[source] + suffix
    return absolute


def rewrite(value, base, index, self_source):
    if isinstance(value, dict):
        return {key: (mapped_reference(child, base, index, self_source)
                      if key == '$ref' and isinstance(child, str)
                      else urljoin(base, child)
                      if key == 'externalValue' and isinstance(child, str)
                      else rewrite(child, base, index, self_source))
                for key, child in value.items()}
    if isinstance(value, list):
        return [rewrite(child, base, index, self_source) for child in value]
    return value


def embedded(plan, plans):
    index = canonical_index(plans, plan['version'])
    value = rewrite(official_document(plan), plan['source'], index, plan['source'])
    # Legacy OAS3 schema objects use Draft4 boolean exclusive bounds. Declare
    # their dialect only when upstream omitted it; never rewrite constraints.
    if (plan['block'].startswith('schemas/') and '$schema' not in value
            and has_boolean_exclusive_bound(value)):
        value = {'$schema': DRAFT4, **value}
    if plan['block'] == 'api':
        # Path Items cannot be combined using JSON Schema allOf. Operation
        # references expose both method blocks without duplicating a method.
        job_path = PATHS['Job']
        if plan['version'] == 'v2':
            job_path = job_path.replace('{jobId}', '{jobID}')
        source, _ = source_for(plan['version'], 'paths/Job')
        upstream = rewrite(load(source), source, index, None)
        value['paths'][job_path] = {
            **{k: v for k, v in upstream.items() if k not in METHODS},
            'get': {'$ref': identifier(plan['version'], 'paths/Job') + '#/get'},
            'delete': {'$ref': identifier(plan['version'], 'paths/DismissJob') + '#/delete'},
        }
        for name, path in PATHS.items():
            if name in ('Job', 'DismissJob'):
                continue
            if plan['version'] == 'v2':
                path = path.replace('{jobId}', '{jobID}')
            value['paths'][path] = {'$ref': identifier(plan['version'], 'paths/' + name)}
    return value


def discover(plans):
    """Add missing pinned Core components, not the entire multipart/CWL API.

    Other vocabularies remain absolute official references. Existing metadata
    is never regenerated; existing identifiers win over newly discovered ones.
    """
    plans = list(plans)
    represented = {p['source'] for p in plans if p['version'] == 'v2'}
    todo = [p for p in plans if p['version'] == 'v2' and p['block'] != 'api']
    todo.append({'source': V2 + 'paths/common-core/pAPI.yaml'})
    while todo:
        plan = todo.pop()
        for ref in refs(load(plan['source'])):
            source = urldefrag(urljoin(plan['source'], ref))[0]
            if source in represented or not source.startswith(V2):
                continue
            relative = source[len(V2):]
            parts = relative.split('/')
            if len(parts) == 4 and parts[:3] == ['paths', 'processes-core', 'operations']:
                block = 'operations/' + Path(parts[-1]).stem
            elif (len(parts) == 3 and parts[0] in ('schemas', 'parameters', 'responses')
                  and parts[1] in ('common-core', 'common-geodata', 'processes-core', 'unspecified')):
                block = relative.removesuffix('.yaml')
            else:
                continue
            new = {'version': 'v2', 'block': block, 'source': source,
                   'classification': 'official', 'id': identifier('v2', block),
                   'metadata': ROOT / '_sources/part1/v2' / block / 'bblock.json'}
            represented.add(source)
            plans.append(new)
            todo.append(new)
    return sorted(plans, key=lambda p: p['id'])


def artifact(plan):
    return plan['metadata'].parent / ('schema.yaml' if plan['block'].startswith('schemas/') else 'openapi.yaml')


def canonical_name(name):
    """Remove decorative labels once, retaining meaningful leaf identifiers."""
    if name.startswith('Official '):
        return name.rsplit('/', 1)[-1].removeprefix('Official ')
    name = name.removeprefix('Schema for ')
    for suffix in (' parameter', ' path', ' response', ' schema'):
        if name.endswith(suffix):
            return name.removesuffix(suffix)
    return name


def rendered_files(plans):
    result = {}
    for plan in plans:
        target = artifact(plan)
        value = embedded(plan, plans)
        if target.exists():
            # Compare lists after converting old references to the same mapping
            # as the new document, not by their incidental original spelling.
            original = rewrite(existing_annotations(target), plan['source'],
                               canonical_index(plans, plan['version']), plan['source'])
            context = 'schema' if plan['block'].startswith('schemas/') else 'object'
            preserve_jsonld(value, original, context=context, location=str(target))
        header = ('# Official definition embedded by scripts/align_official_sources.py.\n'
                  if target.name == 'schema.yaml' else '')
        result[target] = (header
                          + yaml.safe_dump(value, allow_unicode=True, sort_keys=False,
                                           default_flow_style=False, indent=2, width=88))
        metadata = plan['metadata']
        if metadata.exists():
            md = json.loads(metadata.read_text())
            # URL overrides defeat the local schema and dependency discovery.
            if plan['block'].startswith('schemas/') and 'schema' in md:
                if md['schema'] not in (plan['source'], 'schema.yaml'):
                    raise ValueError(f'Unexpected schema override in {metadata}: {md["schema"]}')
                del md['schema']
        else:
            kind = plan['block'].split('/')[0]
            md = {'name': 'Official ' + plan['block'], 'status': 'under-development',
                  'dateTimeAddition': '2026-11-10T00:00:00Z',
                  'dateOfLastChange': '2026-11-10',
                  # The metadata schema has no operation class; these are
                  # standalone OpenAPI objects, not complete Path Items.
                  'itemClass': 'model' if kind == 'operations' else kind.rstrip('s'),
                  'register': 'ogcapi-processes',
                  'sources': [{'title': 'OGC API - Processes pinned official Core component',
                               'link': plan['source']}],
                  'tags': ['ogcapi-processes', 'official', 'part1-' + plan['version']]}
        md['name'] = canonical_name(md['name'])
        md['version'] = {'v1': '1.0', 'v2': '2.0'}[plan['version']]
        result[metadata] = json.dumps(md, indent=2, ensure_ascii=False) + '\n'
    return result


def existing_annotations(target):
    """Read exactly one mapping; malformed input must be repaired explicitly."""
    value = yaml.safe_load(target.read_text())
    if not isinstance(value, dict):
        raise TypeError(f'Expected one YAML mapping in {target}')
    return value


def annotation_free(value, context):
    if isinstance(value, dict):
        return {key: annotation_free(child, child_context(context, key))
                for key, child in value.items()
                if not (context == 'schema' and key in JSONLD_KEYS)}
    if isinstance(value, list):
        return [annotation_free(child, context) for child in value]
    return value


def has_annotations(value, context):
    return json.dumps(value, sort_keys=True) != json.dumps(annotation_free(value, context), sort_keys=True)


def preserve_jsonld(value, original, context='schema', location='$'):
    """Preserve annotations only at schema positions; refuse unsafe list zips."""
    if isinstance(value, dict) and isinstance(original, dict):
        for key, child in original.items():
            child_mode = child_context(context, key)
            if context == 'schema' and key in JSONLD_KEYS:
                value[key] = copy.deepcopy(child)
            elif key in value:
                preserve_jsonld(value[key], child, child_mode, location + '/' + str(key))
            elif has_annotations(child, child_mode):
                raise ValueError(f'Annotated node removed at {location}/{key}; reconcile annotations explicitly')
    elif isinstance(value, list) and isinstance(original, list):
        if not has_annotations(original, context):
            return
        if (json.dumps(annotation_free(value, context), sort_keys=True)
                != json.dumps(annotation_free(original, context), sort_keys=True)):
            raise ValueError(f'Annotated list changed at {location}; reconcile annotations explicitly before regeneration')
        for position, (child, old) in enumerate(zip(value, original)):
            preserve_jsonld(child, old, context, f'{location}/{position}')
    elif has_annotations(original, context):
        raise ValueError(f'Annotated structure changed at {location}; reconcile annotations explicitly')