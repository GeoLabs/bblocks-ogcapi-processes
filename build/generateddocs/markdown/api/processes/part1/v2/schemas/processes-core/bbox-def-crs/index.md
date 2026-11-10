
# bbox-def-crs (Schema)

`ogc.api.processes.part1.v2.schemas.processes-core.bbox-def-crs` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
anyOf:
- type: string
  format: uri
  enum:
  - http://www.opengis.net/def/crs/OGC/1.3/CRS84
  - http://www.opengis.net/def/crs/OGC/0/CRS84h
  default: http://www.opengis.net/def/crs/OGC/1.3/CRS84
- type: string
  format: uri
  default: http://www.opengis.net/def/crs/OGC/1.3/CRS84
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.processes-core.bbox-def-crs
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/bbox-def-crs/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/bbox-def-crs/schema.yaml)

## Sources

* [OGC API - Processes pinned official Core component](https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi/schemas/processes-core/bbox-def-crs.yaml)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/processes-core/bbox-def-crs`

