
# statusInfo schema (Schema)

`ogc.api.processes.v1.schemas.statusInfo` *v0.1*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
properties:
  created:
    format: date-time
    type: string
  finished:
    format: date-time
    type: string
  jobID:
    type: string
  links:
    items:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/link/schema.yaml
    type: array
  message:
    type: string
  processID:
    type: string
  progress:
    maximum: 100
    minimum: 0
    type: integer
  started:
    format: date-time
    type: string
  status:
    $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/statusCode/schema.yaml
  type:
    enum:
    - process
    type: string
  updated:
    format: date-time
    type: string
required:
- jobID
- status
- type
type: object
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.v1.schemas.statusInfo
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '0.1'
  dateOfLastChange: '2026-11-09'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/statusInfo/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/statusInfo/schema.yaml)

## Sources

* [OGC API Features - Part 1 - Core corrigendum](https://docs.ogc.org/is/17-069r4/17-069r4.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/statusInfo`

