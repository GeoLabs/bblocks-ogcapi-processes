
# outputDescription (Schema)

`ogc.api.processes.part1.v1.schemas.outputDescription` *v1.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/descriptionType/schema.yaml
- type: object
  required:
  - schema
  properties:
    schema:
      $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/schema/schema.yaml
      x-jsonld-id: https://w3id.org/ogc/api/processes/schema
x-jsonld-extra-terms:
  title: http://purl.org/dc/terms/title
  description: http://purl.org/dc/terms/description
  keywords: https://w3id.org/ogc/api/processes/keywords
  nullable: https://w3id.org/ogc/api/processes/nullable
  type: https://w3id.org/ogc/api/processes/type
  $ref:
    x-jsonld-id: https://w3id.org/ogc/api/processes/ref
    x-jsonld-type: '@id'
  default:
    x-jsonld-id: https://w3id.org/ogc/api/processes/default
    x-jsonld-type: '@json'
  minOccurs: https://w3id.org/ogc/api/processes/minOccurs
  maxOccurs: https://w3id.org/ogc/api/processes/maxOccurs
  enum:
    x-jsonld-id: https://w3id.org/ogc/api/processes/enum
    x-jsonld-container: '@set'
x-jsonld-vocab: https://w3id.org/ogc/api/processes/
x-jsonld-prefixes:
  dct: http://purl.org/dc/terms/
  proc: https://w3id.org/ogc/api/processes/
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v1.schemas.outputDescription
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '1.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/outputDescription/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/outputDescription/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "@vocab": "https://w3id.org/ogc/api/processes/",
    "schema": {
      "@context": {
        "@vocab": "https://w3id.org/ogc/api/schema/"
      },
      "@id": "proc:schema"
    },
    "title": "dct:title",
    "description": "dct:description",
    "keywords": "proc:keywords",
    "nullable": "proc:nullable",
    "type": "proc:type",
    "$ref": {
      "@id": "proc:ref",
      "@type": "@id"
    },
    "default": {
      "@id": "proc:default",
      "@type": "@json"
    },
    "minOccurs": "proc:minOccurs",
    "maxOccurs": "proc:maxOccurs",
    "enum": {
      "@id": "proc:enum",
      "@container": "@set"
    },
    "dct": "http://purl.org/dc/terms/",
    "proc": "https://w3id.org/ogc/api/processes/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v1/schemas/outputDescription/context.jsonld)

## Sources

* [OGC API - Processes - Part 1: Core (version 1.0, OGC 18-062r2)](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v1/schemas/outputDescription`

