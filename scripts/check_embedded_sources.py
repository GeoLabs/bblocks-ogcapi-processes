"""Independent content and graph checks for the embedded source audit."""
import json
from collections import Counter
from urllib.parse import unquote, urldefrag, urljoin, urlsplit

import yaml

from audit_official_sources import load, refs
from official_materializer import artifact, identifier
from schema_annotations import JSONLD_KEYS, child_context

METHODS = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}


def expected_dialect(plan, document):
    """Independent eligibility check; never discard $schema or constraints."""
    if not plan['block'].startswith('schemas/') or '$schema' in document:
        return None
    pending = [document]
    while pending:
        schema = pending.pop()
        if not isinstance(schema, dict):
            continue
        for keyword, value in schema.items():
            if keyword in ('exclusiveMinimum', 'exclusiveMaximum') and type(value) is bool:
                return 'http://json-schema.org/draft-04/schema#'
            if keyword in ('properties', 'patternProperties', 'definitions', '$defs',
                           'dependencies', 'dependentSchemas') and isinstance(value, dict):
                pending.extend(value.values())
            elif keyword in ('allOf', 'anyOf', 'oneOf', 'prefixItems', 'items') and isinstance(value, list):
                pending.extend(value)
            elif keyword in ('items', 'additionalItems', 'additionalProperties', 'not',
                             'contains', 'propertyNames', 'if', 'then', 'else',
                             'unevaluatedItems', 'unevaluatedProperties'):
                pending.append(value)
    return None


def expected_document(plan):
    """Independent projection of upstream bytes, never the materializer output."""
    from audit_official_sources import PATHS, V2, V2_PATHS
    value = load(plan['source'])
    if plan['block'] in ('paths/Job', 'paths/DismissJob'):
        method = 'get' if plan['block'] == 'paths/Job' else 'delete'
        return {k: v for k, v in value.items() if k not in METHODS or k == method}
    if plan['block'] == 'api' and plan['version'] == 'v2':
        value = dict(value)
        value['paths'] = {PATHS[name].replace('{jobId}', '{jobID}'):
                          {'$ref': V2 + 'paths/' + target + '.yaml'}
                          for name, target in V2_PATHS.items()}
        value['paths']['/api'] = {'$ref': V2 + 'paths/common-core/pAPI.yaml'}
        # Only selected path components are retained; multipart CWL/PROV
        # components are not part of this Part 1 projection.
        value['components'] = {}
    dialect = expected_dialect(plan, value)
    return {'$schema': dialect, **value} if dialect else value


def pointer(value, fragment):
    if not fragment:
        return value
    if not fragment.startswith('/'):
        raise ValueError(f'Unsupported JSON pointer: {fragment}')
    for token in unquote(fragment).lstrip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def source_reference(ref, plan, index):
    if ref.startswith('bblocks://'):
        block, fragment = urldefrag(ref)
        source = index[block]['source']
        if not fragment:
            return source
        return source + ('/' + fragment.lstrip('/') if '#' in source else '#' + fragment)
    if ref.startswith('#'):
        fragment = ref[1:]
        if not fragment:
            return plan['source']
        return plan['source'] + (fragment if '#' in plan['source'] else '#' + fragment)
    return urljoin(plan['source'], ref)


def normalized(value, plan, index, local=True, context=None):
    if context is None:
        context = 'schema' if plan['block'].startswith('schemas/') else 'object'
    if isinstance(value, dict):
        return {str(key): (source_reference(child, plan, index) if local else urljoin(plan['source'], child))
                if key in ('$ref', 'externalValue') and isinstance(child, str)
                else normalized(child, plan, index, local, child_context(context, key))
                for key, child in value.items()
                if not (context == 'schema' and key in JSONLD_KEYS)}
    if isinstance(value, list):
        return [normalized(child, plan, index, local, context) for child in value]
    return value


def expand_path_item(value, plan, index, documents, seen=None):
    """Expand only Path Item/Operation references; leave schema recursion alone."""
    seen = set() if seen is None else seen
    if isinstance(value, dict) and '$ref' in value:
        ref = value['$ref']
        if ref in seen:
            raise ValueError('Cyclic Path Item/Operation reference: ' + ref)
        block, fragment = urldefrag(ref)
        if block.startswith('bblocks://'):
            target = index[block]
            child = pointer(documents[block], fragment)
            return expand_path_item(child, target, index, documents, seen | {ref})
        absolute = urljoin(plan['source'], ref)
        return expand_path_item(load(absolute), {**plan, 'source': absolute}, index, documents, seen | {ref})
    if isinstance(value, dict):
        return {str(key): expand_path_item(child, plan, index, documents, seen)
                if key in METHODS else normalized(child, plan, index)
                for key, child in value.items()}
    return normalized(value, plan, index)


def check(plans):
    index = {p['id']: p for p in plans}
    documents, errors = {}, []
    for plan in plans:
        try:
            text = artifact(plan).read_text()
            if '\t' in text or text.lstrip().startswith('{'):
                raise ValueError('Artifact must use space-indented block YAML')
            body = '\n'.join(line for line in text.splitlines() if not line.startswith('#')).lstrip()
            if body.startswith(('{', '[')):
                raise ValueError('Flow-style JSON artifact is not readable block YAML')
            documents[plan['id']] = yaml.safe_load(text)
            if not isinstance(documents[plan['id']], dict):
                raise ValueError('Artifact must be one YAML mapping')
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append({'block': plan['id'], 'error': str(exc)})
    graph = {}
    for plan in plans:
        ident = plan['id']
        if ident not in documents:
            continue
        current = documents[ident]
        graph[ident] = set()
        try:
            for ref in refs(current):
                block, fragment = urldefrag(ref)
                if block.startswith('bblocks://'):
                    if block not in index:
                        raise ValueError('Unresolved building block ' + ref)
                    if index[block]['version'] != plan['version']:
                        raise ValueError('Cross-edition reference ' + ref)
                    pointer(documents[block], fragment)
                    graph[ident].add(block)
                elif ref.startswith('#'):
                    pointer(current, fragment)
                elif urlsplit(ref).scheme not in ('http', 'https'):
                    raise ValueError('Non-absolute official reference ' + ref)
            md = json.loads(plan['metadata'].read_text())
            if plan['block'].startswith('schemas/') and md.get('schema') not in (None, 'schema.yaml'):
                raise ValueError('Metadata bypasses local schema')
            for url in external_values(current):
                if urlsplit(url).scheme not in ('http', 'https'):
                    raise ValueError('Non-absolute externalValue ' + url)
            expected = expected_document(plan)
            if plan['block'] == 'api':
                # Normalize the selected official path objects independently
                # of the producer's method/ref construction.
                actual = normalized(current, plan, index)
                wanted = normalized(expected, plan, index, local=False)
                actual['paths'] = {path: expand_path_item(item, plan, index, documents)
                                   for path, item in current['paths'].items()}
                wanted['paths'] = {path: expand_path_item(item, plan, index, documents)
                                   for path, item in expected['paths'].items()}
            else:
                actual = normalized(current, plan, index)
                wanted = normalized(expected, plan, index, local=False)
            # Python equality conflates True/1 and False/0; JSON Schema does
            # not. In particular a boolean exclusive bound must stay boolean.
            if json.dumps(actual, sort_keys=True) != json.dumps(wanted, sort_keys=True):
                raise ValueError('Embedded content differs from official after reference normalization')
            plan['reference_matches'] = True
        except (OSError, ValueError, TypeError, KeyError, IndexError, yaml.YAMLError) as exc:
            plan['reference_matches'] = False
            errors.append({'block': ident, 'error': str(exc)})
    graphs = {}
    for version in ('v1', 'v2'):
        api = identifier(version, 'api')
        reached, todo = set(), list(graph.get(api, ()))
        while todo:
            node = todo.pop()
            if node not in reached:
                reached.add(node)
                todo.extend(graph.get(node, ()))
        counts = Counter(index[node]['block'].split('/')[0] for node in reached)
        direct_paths = {node for node in graph.get(api, ()) if index[node]['block'].startswith('paths/')}
        missing_paths = {identifier(version, 'paths/' + name) for name in (
            'LandingPage', 'Conformance', 'ProcessList', 'ProcessDescription', 'Execution',
            'JobList', 'Job', 'DismissJob', 'JobResult')} - direct_paths
        if missing_paths or not all(counts[kind] for kind in ('parameters', 'responses', 'schemas')):
            errors.append({'block': api, 'error': 'API graph incomplete', 'missing_paths': sorted(missing_paths)})
        # Every path must lead to responses and schemas, even through an
        # operation block. Some upstream paths legitimately have no parameters.
        for path in direct_paths:
            seen, todo = set(), list(graph.get(path, ()))
            while todo:
                node = todo.pop()
                if node not in seen:
                    seen.add(node)
                    todo.extend(graph.get(node, ()))
            kinds = {index[node]['block'].split('/')[0] for node in seen}
            if not {'responses', 'schemas'} <= kinds:
                errors.append({'block': path, 'error': 'Path graph lacks responses/schemas'})
        graphs[version] = {'direct_dependencies': len(graph.get(api, ())),
                           'direct_path_blocks': len(direct_paths),
                           'reachable_blocks': len(reached), 'reachable_by_kind': dict(counts),
                           'edges': sum(len(graph.get(node, ())) for node in reached | {api})}
    return errors, graphs


def external_values(value):
    if isinstance(value, dict):
        if isinstance(value.get('externalValue'), str):
            yield value['externalValue']
        for child in value.values():
            yield from external_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from external_values(child)