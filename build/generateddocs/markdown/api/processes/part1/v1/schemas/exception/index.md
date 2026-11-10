
# exception (Schema)

`ogc.api.processes.part1.v1.schemas.exception` *v1.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
title: Exception Schema
description: JSON schema for exceptions based on RFC 7807
type: object
required:
- type
properties:
  type:
    type: string
  title:
    type: string
  status:
    type: integer
  detail:
    type: string
  instance:
    type: string
additionalProperties: true
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v1.schemas.exception
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '1.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/exception/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/exception/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (version 1.0, OGC 18-062r2)](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v1/schemas/exception`

