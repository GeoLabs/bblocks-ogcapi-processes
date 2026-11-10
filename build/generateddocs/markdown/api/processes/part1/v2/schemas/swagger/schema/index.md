
# schema (Schema)

`ogc.api.processes.part1.v2.schemas.swagger.schema` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: http://json-schema.org/draft-04/schema#
oneOf:
- $ref: https://schemas.opengis.net/ogcapi/processes/part1/1.0/openapi/schemas/reference.yaml
- type: object
  properties:
    title:
      type: string
    multipleOf:
      type: number
      minimum: 0
      exclusiveMinimum: true
    maximum:
      type: number
    exclusiveMaximum:
      type: boolean
      default: false
    minimum:
      type: number
    exclusiveMinimum:
      type: boolean
      default: false
    maxLength:
      type: integer
      minimum: 0
    minLength:
      type: integer
      minimum: 0
      default: 0
    pattern:
      type: string
      format: regex
    maxItems:
      type: integer
      minimum: 0
    minItems:
      type: integer
      minimum: 0
      default: 0
    uniqueItems:
      type: boolean
      default: false
    maxProperties:
      type: integer
      minimum: 0
    minProperties:
      type: integer
      minimum: 0
      default: 0
    required:
      type: array
      items:
        type: string
      minItems: 1
      uniqueItems: true
    enum:
      type: array
      items: {}
      minItems: 1
      uniqueItems: false
    type:
      type: string
      enum:
      - array
      - boolean
      - integer
      - number
      - object
      - string
    properties:
      type: object
      additionalProperties:
        type: boolean
        default: true
    additionalProperties:
      type: boolean
      default: true
    description:
      type: string
    format:
      type: string
    default: {}
    nullable:
      type: boolean
      default: false
    readOnly:
      type: boolean
      default: false
    writeOnly:
      type: boolean
      default: false
    example: {}
    deprecated:
      type: boolean
      default: false
    contentMediaType:
      type: string
    contentEncoding:
      type: string
    contentSchema:
      type: string
  additionalProperties: false
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.swagger.schema
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/swagger/schema/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/swagger/schema/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/swagger/schema`

