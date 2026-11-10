
# bbox (Schema)

`ogc.api.processes.part1.v1.schemas.bbox` *v1.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
type: object
required:
- bbox
properties:
  bbox:
    type: array
    oneOf:
    - minItems: 4
      maxItems: 4
    - minItems: 6
      maxItems: 6
    items:
      type: number
  crs:
    type: string
    format: uri
    default: http://www.opengis.net/def/crs/OGC/1.3/CRS84
    enum:
    - http://www.opengis.net/def/crs/OGC/1.3/CRS84
    - http://www.opengis.net/def/crs/OGC/0/CRS84h
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v1.schemas.bbox
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '1.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/bbox/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/bbox/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (version 1.0, OGC 18-062r2)](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v1/schemas/bbox`

