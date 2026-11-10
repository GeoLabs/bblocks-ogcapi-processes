
# schema (Schema)

`ogc.api.processes.part1.v2.schemas.schema` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
description: Attributes of the features or fields of a coverage range. Defined by
  a subset of the JSON Schema for the properties of a feature
type: object
required:
- type
- properties
properties:
  type:
    type: string
    enum:
    - object
  required:
    type: array
    minItems: 1
    items:
      type: string
  properties:
    type: object
    default: {}
    additionalProperties:
      type: object
      properties:
        title:
          type: string
        description:
          type: string
        type:
          type: string
          enum:
          - array
          - boolean
          - integer
          - 'null'
          - number
          - object
          - string
        enum:
          type: array
          minItems: 1
          items: {}
          uniqueItems: true
        format:
          type: string
        contentMediaType:
          type: string
        maximum:
          type: number
        exclusiveMaximum:
          type: number
        minimum:
          type: number
        exclusiveMinimum:
          type: number
        pattern:
          type: string
          format: regex
        maxItems:
          type: integer
          minimum: 0
        minItems:
          type: integer
          default: 0
          minimum: 0
        x-ogc-definition:
          type: string
          format: uri
        x-ogc-unit:
          type: string
        x-ogc-unitLang:
          type: string
x-jsonld-vocab: https://w3id.org/ogc/api/schema/
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.schema
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/schema/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/schema/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "@vocab": "https://w3id.org/ogc/api/schema/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/schema/context.jsonld)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/schema`

