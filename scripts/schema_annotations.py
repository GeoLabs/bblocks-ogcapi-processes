"""Exact local annotation vocabulary and schema-position traversal rules.

Named maps and instance payloads are not schema keyword positions.
Unknown x-jsonld-prefixed keys are deliberately ordinary content.
"""
JSONLD_KEYS = frozenset({
    'x-jsonld-id', 'x-jsonld-type', 'x-jsonld-container', 'x-jsonld-context',
    'x-jsonld-reverse', 'x-jsonld-prefix', 'x-jsonld-base', 'x-jsonld-vocab',
    'x-jsonld-language', 'x-jsonld-direction', 'x-jsonld-nest',
    'x-jsonld-index', 'x-jsonld-protected', 'x-jsonld-version',
    'x-jsonld-propagate', 'x-jsonld-import',
    # ogc.na.annotate_schema also uses these two non-JSON-LD-keyword helpers.
    'x-jsonld-prefixes', 'x-jsonld-extra-terms',
})
SCHEMA_MAPS = {'properties', 'patternProperties', 'definitions', '$defs',
               'dependencies', 'dependentSchemas'}
SCHEMA_CHILDREN = {'allOf', 'anyOf', 'oneOf', 'prefixItems', 'items',
                   'additionalItems', 'additionalProperties', 'not', 'contains',
                   'propertyNames', 'if', 'then', 'else', 'unevaluatedItems',
                   'unevaluatedProperties', 'contentSchema'}


def child_context(context, key):
    if context.startswith('map:'):
        return context[4:]
    if context == 'schema':
        if key in SCHEMA_MAPS:
            return 'map:schema'
        return 'schema' if key in SCHEMA_CHILDREN else 'data'
    if context == 'data':
        return 'data'
    if context == 'components':
        return 'map:schema' if key == 'schemas' else 'map:object'
    if key == 'schema':
        return 'schema'
    if key == 'components':
        return 'components'
    if key in ('example', 'examples', 'default', 'enum', 'const', 'value'):
        return 'data'
    if key in ('paths', 'responses', 'content', 'headers', 'encoding', 'callbacks',
               'webhooks', 'dependentRequired'):
        return 'map:object'
    return 'object'