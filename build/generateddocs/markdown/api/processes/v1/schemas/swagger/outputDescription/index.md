
# outputDescription schema (Schema)

`ogc.api.processes.v1.schemas.swagger.outputDescription` *v0.1*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/descriptionType/schema.yaml
- properties:
    schema:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/swagger/schema/schema.yaml
  required:
  - schema
  type: object
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.v1.schemas.swagger.outputDescription
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '0.1'
  dateOfLastChange: '2026-11-09'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/swagger/outputDescription/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/swagger/outputDescription/schema.yaml)

## Sources

* [OGC API Features - Part 1 - Core corrigendum](https://docs.ogc.org/is/17-069r4/17-069r4.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/swagger/outputDescription`

