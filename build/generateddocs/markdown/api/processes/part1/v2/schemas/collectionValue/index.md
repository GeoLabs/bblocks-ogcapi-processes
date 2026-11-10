
# collectionValue (Schema)

`ogc.api.processes.part1.v2.schemas.collectionValue` *v2.0*

None

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
allOf:
- $ref: https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/format/schema.yaml
- type: object
  required:
  - collection
  properties:
    collection:
      description: 'The URI of the OGC API collection that should be accessed to provide

        input values from the corresponding process input.  The server

        offering this collection is referred to as the "value source server".'
      anyOf:
      - type: string
        description: 'Collection identifier for a collection available at `{root}/collections/{collectionID}`,
          where `{root}` represents the landing page

          of the process using the collection as an input (for the top-level process,
          that is the landing page of the process execution endpoint

          to which the execution request is posted), or the landing page of the document
          being retrieved in the case of an output.

          If the `collection` string includes a `/`, it must be interpreted as a URI
          reference rather than as a collection ID.'
      - type: string
        description: "The URI of an OGC API collection.\nIf a relative URI reference
          is used, the Base URI is defined as such:\n- For a Collection value received
          as input to a process, the Base URI is defined as the URI of the description\n
          \ (`{root}/processes/{processId}`) of that process, with the receiving process
          object understood as the Encapsulating Entity as per\n  [RFC 3986 Section
          5.1.2](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.2).\n-
          For a Collection Output value, the Base URI is defined from the Retrieval
          URI as as per\n  [RFC 3986 Section 5.1.3](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.3),\n
          \ for example, `/jobs/{jobId}/results`, `/jobs/{jobId}/results/{outputID}`
          or `/jobs/{jobId}/results/{outputID}/{N}` depending on the\n  resource being
          retrieved.\nIf a collection string does not contain any `/`, it must not
          be interpreted as a URI reference, and must instead be resolved as a\ncollection
          identifier. For example, `countries` would resolve to `{root}/collections/countries`
          rather than `{root}/processes/countries`."
        format: uri-reference
    bbox:
      description: "Only resources that have a geometry that intersects the bounding
        box\nare selected.  The bounding box is provided as four or six numbers,\ndepending
        on whether the coordinate reference system includes a\nvertical axis (height
        or depth):\n\n* Lower left corner, coordinate axis 1\n* Lower left corner,
        coordinate axis 2\n* Minimum value, coordinate axis 3 (optional)\n* Upper
        right corner, coordinate axis 1\n* Upper right corner, coordinate axis 2\n*
        Maximum value, coordinate axis 3 (optional)\n\nIf the value consists of four
        numbers, the coordinate reference\nsystem is WGS84 longitude/latitude\n  (http://www.opengis.net/def/crs/OGC/1.3/CRS84)\nunless
        a different coordinate reference system is specified in the\nparameter `bboxCrs`.\n\nIf
        the value consists of six numbers, the coordinate reference system\nis WGS84
        (http://www.opengis.net/def/crs/OGC/0/CRS84h) longitude/\nlatitude/ ellipsoidal
        height unless a different coordinate reference\nsystem is specified in the
        parameter `bboxCrs`.\n\nFor WGS84 longitude/latitude the values are in most
        cases the sequence\nof minimum longitude, minimum latitude, maximum longitude
        and maximum\nlatitude.  However, in cases where the box spans the antimeridian
        the\nfirst value (west-most box edge) is larger than the third value\n(east-most
        box edge).\n\nIf the vertical axis is included, the third and the sixth number
        are\nthe bottom and the top of the 3-dimensional bounding box.\n\nIf a resource
        has multiple spatial geometry properties, it is the\ndecision of the server
        whether only a single spatial geometry property\nis used to determine the
        extent or all relevant geometries."
      type: array
      oneOf:
      - minItems: 4
        maxItems: 4
      - minItems: 6
        maxItems: 6
      items:
        type: number
    bboxCrs:
      description: "Asserts the CRS used for the coordinate values of the `bbox`\nparameter.
        \ The default is WGS 84 or WGS84h depending on whether\nellipsoidal height
        is included or not:\n  * WGS 84 longitude/latitude [4 numbers]\n    (http://www.opengis.net/def/crs/OGC/1.3/CRS84)\n
        \ * WGS 84h longitude/latitude/ellipsoidal height [6 numbers]\n    (http://www.opengis.net/def/crs/OGC/0/CRS84h_"
      type: string
      format: uri
    geometry:
      description: 'Only resources that have a geometry that intersects the geometry

        specified using the `geometry` parameter are selected.  The value of

        the `geometry` parameter can be specified using WKT or GeoJSON.

        If a resource has multiple spatial geometry properties, it is the

        decision of the server whether only a single spatial geometry property

        is used to determine the extent or all relevant geometries.'
      oneOf:
      - type: string
      - $ref: https://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/geometryGeoJSON.yaml
    geometryCrs:
      description: "Asserts the CRS used for the coordinate values of the `geometry`\nparameter.
        \ The default is WGS 84 or WGS84h depending on whether\nellipsoidal height
        is included or not:\n  * WGS 84 longitude/latitude [4 numbers]\n    (http://www.opengis.net/def/crs/OGC/1.3/CRS84)\n
        \ * WGS 84h longitude/latitude/ellipsoidal height [6 numbers]\n    (http://www.opengis.net/def/crs/OGC/0/CRS84h_"
      type: string
    datetime:
      description: "Either a date-time or an interval, half-bounded or bounded. Date
        and\ntime expressions adhere to RFC 3339. Half-bounded intervals are\nexpressed
        using double-dots.\n\nExamples:\n  * A date-time:\n    \"2018-02-12T23:20:50Z\"\n
        \ * A bounded interval:\n    \"2018-02-12T00:00:00Z/2018-03-18T12:31:12Z\"\n
        \ * Half-bounded intervals:\n    \"2018-02-12T00:00:00Z/..\" or \"../2018-03-18T12:31:12Z\"\n\nOnly
        resources that have a temporal property that intersects the\nvalue of `datetime`
        are selected.\n\nIf a resource has multiple temporal properties, it is the
        decision of\nthe server whether only a single temporal property is used to\ndetermine
        the extent or all relevant temporal properties."
      type: string
    limit:
      description: 'The optional limit parameter limits the number of items that are

        presented in the response document.

        Only items are counted that are on the first level of the collection

        in the response document.  Nested objects contained within the

        explicitly requested items shall not be counted.'
      type: integer
      minimum: 1
      maximum: 10000
      default: 10
    crs:
      description: 'If the parameter is specified, then the coordinates of all

        geometry-valued properties in the response document are in

        the requested CRS. Otherwise the coordinates are in the default CRS,

        that is http://www.opengis.net/def/crs/OGC/1.3/CRS84 for coordinates

        without height and http://www.opengis.net/def/crs/OGC/0/CRS84h for

        coordinates with ellipsoidal height.'
      type: string
      format: uri
    filter:
      description: 'A search or filter condition.  This condition determines which

        resources from the OGC API collection are included in the result

        set and are thus passed as values to the corresponding process input.

        The `filter` parameter can be a string where the search condition is

        encoded in some text-based query langauge (e.g. cql2-text) or a

        CQL2 JSON object that encodes the search condition using JSON.'
      oneOf:
      - type: string
      - $ref: https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi/schemas/cql2/cql2.yaml
    filterCrs:
      description: "Asserts the CRS used for the coordinate values of the `filter`\nparameter.
        \ The default is WGS 84 or WGS 84h depending on whether\nellispoidal jeight
        is included with the coordinates or not:\n  * WGS 84 longitude/latitude\n
        \   (http://www.opengis.net/def/crs/OGC/1.3/CRS84)\n  * WGS 84h longitude/latitude/ellipsoidal
        height\n    (http://www.opengis.net/def/crs/OGC/0/CRS84h_"
      type: string
      format: uri-reference
    filterLang:
      description: 'Indicates the language used to encode a filter expression specified

        using the `filter` parameter. Query languages can include CQL2 text,

        CQL 2 JSON or OGC Filter Encoding (XML).'
      type: string
      enum:
      - cql2-text
      - cql2-json
      - fes-xml
    subset:
      description: 'Retrieve only part of the data by slicing or trimming along one
        or

        more axis. For trimming: {axisAbbrev}({low}:{high}) (preserves

        dimensionality). An asterisk (`*`) can be used instead of {low} or

        {high} to indicate the minimum/maximum value. For slicing:

        {axisAbbrev}({value}) (reduces dimensionality).'
      type: array
      items:
        type: string
    subsetCrs:
      description: "Asserts the CRS used for the coordinate values of the `subset`\nparameter.
        \ The default is WGS 84 or WGS 84h depending on whether\nellispoidal height
        in included with the coordinates or not:\n  * WGS 84 longitude/latitude\n
        \   (http://www.opengis.net/def/crs/OGC/1.3/CRS84)\n  * WGS 84h longitude/latitude/ellipsoidal
        height\n    (http://www.opengis.net/def/crs/OGC/0/CRS84h_"
      type: string
    ids:
      description: 'The optional ids parameter allows a specific list of resources,

        indicated by their identifiers, to be fetched from the OGC API

        collection. Only resources whose identifier matches one of the

        values listed for this parameter shall appear in the result set.'
      type: array
      items:
        type: string
    q:
      description: 'The optional q parameter supports keyword searching.  Only resources

        whose text fields contain one or more of the specified search terms

        are selected.  The specific set of text keys/fields/properties of a

        resource to which the q operator is applied is up to the discretion

        of the server.   Implementations should, however, apply the q

        operator to the title, description and keywords keys/fields/properties

        if they exist in the resource.'
      type: array
      items:
        type: string
    assets:
      description: A list of STAC asset tags.
      type: array
      items:
        type: string
    properties:
      description: 'A filter that selects resource properties to be included in a

        response document.  The elements in the `properties` parameter can

        be the names of resource properties, aliases for resources properties

        or synthetic properties.  Synthetic properties are properties that

        are computed on the fly and can reference resource property names

        or aliases for resource properties.'
      type: array
      items:
        type: string
    aliases:
      description: 'A dictionary of aliases that can be used as values for the

        `properties` parameter.  Aliases can be alternative names for

        resource properties or synthetic properties.  Synthetic properties

        are named expressions that are computed at run-time.  Expressions

        for synthetic properties are encoded using some expression language

        and can include references to resource property names or aliases

        for resource properties..'
      type: object
      additionalProperties:
        oneOf:
        - type: string
        - type: object
          properties:
            expressionLang:
              type: string
              enum:
              - cql2-text
              - cql2-json
            expression:
              oneOf:
              - type: string
              - $ref: https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi/schemas/cql2/cql2.yaml
    passThroughParameters:
      description: 'Parameters specified in this object are passed through to the
        value

        source server for processing on that server.  The keys used in this

        object should be identical to query parameters that the value source

        server would recognize.  In the case where the OAProc server supports

        local filtering, the `passThroughParameters` property provides a

        mechanism to force filtering to happen on the value source server.'
      type: object
x-bblocks-metadata:
  itemIdentifier: ogc.api.processes.part1.v2.schemas.collectionValue
  register: https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json
  version: '2.0'
  dateOfLastChange: '2026-11-10'

```

Links to the schema:

* YAML version: [schema.yaml](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/collectionValue/schema.json)
* JSON version: [schema.json](https://geolabs.github.io/bblocks-ogcapi-processes/build/annotated/api/processes/part1/v2/schemas/collectionValue/schema.yaml)

## Sources

* [OGC API - Processes - Part 1: Core](https://docs.ogc.org/is/18-062r2/18-062r2.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/GeoLabs/bblocks-ogcapi-processes](https://github.com/GeoLabs/bblocks-ogcapi-processes)
* Path: `_sources/part1/v2/schemas/collectionValue`

