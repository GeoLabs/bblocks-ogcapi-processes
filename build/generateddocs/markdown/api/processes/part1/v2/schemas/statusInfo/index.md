
# statusInfo (Schema)

`ogc.api.processes.part1.v2.schemas.statusInfo` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/descriptionType/schema.yaml
- type: object
  required:
  - id
  - status
  - processingEntityType
  properties:
    id:
      type: string
    processID:
      type: string
      format: uri
    processingEntityType:
      allOf:
      - description: 'The type of entity that created the job and is doing the processing.

          This includes all the data access apis listed in "apis.yaml" plus

          the processing APIs of OGC API Processes and OpenEO.'
      - $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/processingEntityType/schema.yaml
    profileEntityType:
      allOf:
      - description: 'The type of entity requesting this status information.  This
          may

          be differernt than the processing entity.  For example, the

          processing entity may be OGC API Processes but the status

          information is requested via the OpenEO API.'
      - $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/processingEntityType/schema.yaml
    request:
      oneOf:
      - type: string
      - type: object
      - $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/link/schema.yaml
    status:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/statusCode/schema.yaml
    message:
      type: string
    exception:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/exception/schema.yaml
    created:
      type: string
      format: date-time
    started:
      type: string
      format: date-time
    finished:
      type: string
      format: date-time
    updated:
      type: string
      format: date-time
    progress:
      type: integer
      minimum: 0
      maximum: 100
    links:
      type: array
      items:
        $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/link/schema.yaml
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.statusInfo
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/statusInfo/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/statusInfo/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/statusInfo`

