
# confClasses (Schema)

`ogc.api.processes.part1.v2.schemas.common-core.confClasses` *v2.0*

Compatibility identifier for the official Processes master Common Core confClasses schema.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Example of conformance class declaration
#### json
```json
{
   "conformsTo": [
      "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
      "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
      "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/html",
      "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
      "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/gmlsf0"
   ]
}

```

## Schema

```yaml
type: object
required:
- conformsTo
properties:
  conformsTo:
    type: array
    items:
      type: string
      example: http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.common-core.confClasses
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/common-core/confClasses/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/common-core/confClasses/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/common-core/confClasses`

