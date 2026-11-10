
# subscriber (Schema)

`ogc.api.processes.part1.v1.schemas.subscriber` *v1.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
description: 'Optional URIs for callbacks for this job.


  Support for this parameter is not required and the parameter may be

  removed from the API definition, if conformance class **''callback''**

  is not listed in the conformance declaration under `/conformance`.'
type: object
required:
- successUrl
properties:
  successUri:
    type: string
    format: uri
  inProgressUri:
    type: string
    format: uri
  failedUri:
    type: string
    format: uri
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v1.schemas.subscriber
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '1.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/subscriber/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/subscriber/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (version 1.0, OGC 18-062r2)](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v1/schemas/subscriber`

