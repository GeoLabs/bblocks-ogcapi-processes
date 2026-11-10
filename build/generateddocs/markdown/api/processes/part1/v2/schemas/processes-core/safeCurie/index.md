
# safeCurie (Schema)

`ogc.api.processes.part1.v2.schemas.processes-core.safeCurie` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
description: A safe Compact URI (CURIE) identifying well-known entity.
example: '[ogc-profile:my-profile]'
type: string
pattern: ^\[[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+\]$
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.processes-core.safeCurie
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/safeCurie/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/safeCurie/schema.yaml)

## Sources

* [OGC API - Processes pinned official Core component](https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi/schemas/processes-core/safeCurie.yaml)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/processes-core/safeCurie`

