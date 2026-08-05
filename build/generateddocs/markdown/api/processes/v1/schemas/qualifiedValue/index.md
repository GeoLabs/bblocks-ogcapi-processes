
# qualifiedValue schema (Schema)

`ogc.api.processes.v1.schemas.qualifiedValue` *v0.1*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/format/schema.yaml
- type: object
  required:
  - value
  properties:
    value:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/value/schema.yaml

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/qualifiedValue/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/qualifiedValue/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/qualifiedValue`

