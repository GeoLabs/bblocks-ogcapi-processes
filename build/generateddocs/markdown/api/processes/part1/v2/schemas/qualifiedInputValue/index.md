
# qualifiedInputValue (Schema)

`ogc.api.processes.part1.v2.schemas.qualifiedInputValue` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/format/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/dataClasses/schema.yaml
- type: object
  required:
  - value
  properties:
    value:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/value/schema.yaml
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.qualifiedInputValue
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/qualifiedInputValue/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/qualifiedInputValue/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/qualifiedInputValue`

