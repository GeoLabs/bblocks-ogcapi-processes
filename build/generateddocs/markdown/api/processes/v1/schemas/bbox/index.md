
# bbox schema (Schema)

`ogc.api.processes.v1.schemas.bbox` *v0.1*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
properties:
  bbox:
    items:
      type: number
    oneOf:
    - maxItems: 4
      minItems: 4
    - maxItems: 6
      minItems: 6
    type: array
  crs:
    default: http://www.opengis.net/def/crs/OGC/1.3/CRS84
    enum:
    - http://www.opengis.net/def/crs/OGC/1.3/CRS84
    - http://www.opengis.net/def/crs/OGC/0/CRS84h
    format: uri
    type: string
required:
- bbox
type: object
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.v1.schemas.bbox
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '0.1'
  dateOfLastChange: '2026-11-09'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/bbox/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/bbox/schema.yaml)

## Sources

* [OGC API Features - Part 1 - Core corrigendum](https://docs.ogc.org/is/17-069r4/17-069r4.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/bbox`

