
# Schema for landingPage schema (Schema)

`ogc.api.processes.v1.schemas.common-core.landingPage` *v0.1*

This building block corresponds to the schema for an OGC API Features landingPage

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$comment: Adapted from https://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/landingPage.yaml
type: object
required:
- links
properties:
  title:
    type: string
    example: Buildings in Bonn
  description:
    type: string
    example: Access to data about buildings in the city of Bonn via a Web API that
      conforms to the OGC API Features specification.
  links:
    type: array
    items:
      $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/json-link/schema.yaml
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.v1.schemas.common-core.landingPage
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '0.1'
  dateOfLastChange: '2026-11-09'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/common-core/landingPage/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/common-core/landingPage/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "oa": "http://www.w3.org/ns/oa#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dct": "http://purl.org/dc/terms/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/v1/schemas/common-core/landingPage/context.jsonld)

## Sources

* [OGC API Features - Part 1 - Core corrigendum](https://docs.ogc.org/is/17-069r4/17-069r4.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/v1/schemas/common-core/landingPage`

