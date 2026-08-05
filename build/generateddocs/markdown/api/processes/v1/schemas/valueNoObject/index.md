
# valueNoObject schema (Schema)

`ogc.api.processes.v1.schemas.valueNoObject` *v0.1*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
anyOf:
- type: string
- type: number
- type: integer
- type: boolean
- type: array
  items: {}
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/binaryValue/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/bbox/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/collectionValue/schema.yaml

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/valueNoObject/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/valueNoObject/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/valueNoObject`

