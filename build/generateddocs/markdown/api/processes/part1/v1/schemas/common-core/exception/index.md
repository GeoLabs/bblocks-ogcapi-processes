
# exception (Schema)

`ogc.api.processes.part1.v1.schemas.common-core.exception` *v1.0*

This building block corresponds to the schema for an OGC API Features exception

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
type: object
required:
- code
properties:
  code:
    type: string
  description:
    type: string
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v1.schemas.common-core.exception
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '1.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/common-core/exception/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/common-core/exception/schema.yaml)

## Sources

* [OGC API Features - Part 1 - Core corrigendum](https://docs.ogc.org/is/17-069r4/17-069r4.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v1/schemas/common-core/exception`

