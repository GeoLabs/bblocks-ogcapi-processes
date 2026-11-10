
# dataClasses (Schema)

`ogc.api.processes.part1.v2.schemas.processes-core.dataClasses` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
description: 'Profiling requirements that the specified value, link, collection reference,
  selected output, or input/output

  definition must meet or adapt to, depending on context, in order to make it adequate
  for the process execution.

  These requirements are represented as URIs or safe CURIEs providing resolvable profiles
  applicable to the context.

  They directly corresponds to link references that can be employed for *Content Negotiation
  by Profile*.'
type: object
properties:
  dataClasses:
    type: array
    items:
      anyOf:
      - description: URI to a registered profile entity.
        type: string
        format: uri
      - $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/safeCurie/schema.yaml
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.processes-core.dataClasses
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/dataClasses/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/dataClasses/schema.yaml)

## Sources

* [OGC API - Processes pinned official Core component](https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi/schemas/processes-core/dataClasses.yaml)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/processes-core/dataClasses`

