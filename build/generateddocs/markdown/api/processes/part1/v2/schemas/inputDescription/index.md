
# inputDescription (Schema)

`ogc.api.processes.part1.v2.schemas.inputDescription` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Complex object described using the official v2 schema subset
The official pinned v2 schema requires type and properties in an input schema. The former reference-only example is retained as a negative regression fixture in tests/legacy-schema-ref-fail.json.
#### json
```json
{
  "@context": {
    "op": "http://test-data/cafe-walk/observables/"
  },
  "@id": "op:areaOfInterest",
  "title": "BBOX",
  "description": "BBOX via schema ref",
  "minOccurs": 1,
  "schema": {
    "type": "object",
    "properties": {
      "bbox": {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 4,
        "maxItems": 4
      }
    }
  }
}
```

#### jsonld
```jsonld
{
  "@context": [
    "https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/inputDescription/context.jsonld",
    {
      "op": "http://test-data/cafe-walk/observables/"
    }
  ],
  "@id": "op:areaOfInterest",
  "title": "BBOX",
  "description": "BBOX via schema ref",
  "minOccurs": 1,
  "schema": {
    "type": "object",
    "properties": {
      "bbox": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "minItems": 4,
        "maxItems": 4
      }
    }
  }
}
```

#### ttl
```ttl
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ns1: <https://w3id.org/ogc/api/schema/> .
@prefix op: <http://test-data/cafe-walk/observables/> .
@prefix proc: <https://w3id.org/ogc/api/processes/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

op:areaOfInterest dct:description "BBOX via schema ref" ;
    dct:title "BBOX" ;
    proc:minOccurs 1 ;
    proc:schema [ proc:type "object" ;
            ns1:properties [ ns1:bbox [ proc:type "array" ;
                            ns1:items [ proc:type "number" ] ;
                            ns1:maxItems 4 ;
                            ns1:minItems 4 ] ] ] .


```

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/descriptionType/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/dataClasses/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/dataAccessAPIs/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/executionUnitRequirements/schema.yaml
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/processes-core/schemaAndOccurrences/schema.yaml
- type: object
  properties:
    valuePassing:
      type: array
      items:
        type: string
        enum:
        - byValue
        - byReference
      default:
      - byValue
      - byReference
x-jsonld-extra-terms:
  title: http://purl.org/dc/terms/title
  description: http://purl.org/dc/terms/description
  schema: https://w3id.org/ogc/api/processes/schema
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
  itemIdentifier: ogc.api.processes.part1.v2.schemas.inputDescription
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/inputDescription/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/inputDescription/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "@vocab": "https://w3id.org/ogc/api/processes/",
    "schema": {
      "@context": {
        "@vocab": "https://w3id.org/ogc/api/schema/"
      }
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
[context.jsonld](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/inputDescription/context.jsonld)

## Sources

* [OGC API - Processes - Part 1: Core (2.0 draft, OGC 18-062r3)](https://docs.ogc.org/DRAFTS/18-062r3.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/inputDescription`

