# Response Representations

BaSyx Go Repository APIs expose different views of the same model content through distinct endpoints. A normal read uses the resource endpoint without a representation suffix. The other representations append `/$value`, `/$metadata`, `/$reference`, or `/$path`. Query parameters such as `level` and `extent` modify supported responses but do not select a representation.

## Representation Overview

| Representation | What you get |
| --- | --- |
| Normal | Complete model JSON for the resource, including metadata and values. |
| `$value` | ValueOnly content: a scalar for a simple Property and structured JSON for complex elements. |
| `$metadata` | Model structure and metadata with runtime values omitted according to the metadata rules. |
| `$reference` | An AAS Reference identifying the resource instead of the resource itself. |
| `$path` | An array of paths addressing the resource and its contained elements. |

The standalone Submodel Repository exposes these representations for Submodels and Submodel Elements, on both collection and single-resource operations where defined by its API. The AAS Repository exposes the same Submodel behavior through AAS-scoped routes, and the AAS Environment exposes both AAS-scoped and `/submodels` route forms. An AAS itself has normal and `$reference` reads, not every Submodel representation. Registry descriptors do not use these Repository representation routes.

Representation support depends on the operation and resource type. Check the deployed component's [Swagger UI](swagger) before adding a suffix to an endpoint.

## One Resource in Different Representations

The following examples use Submodel `urn:example:submodel:1`, whose Base64URL path value is `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ`. It contains this small `Nameplate` collection:

```json
{
  "modelType": "SubmodelElementCollection",
  "idShort": "Nameplate",
  "value": [
    {
      "modelType": "Property",
      "idShort": "SerialNumber",
      "valueType": "xs:string",
      "value": "SN-12345"
    },
    {
      "modelType": "Property",
      "idShort": "ManufacturerName",
      "valueType": "xs:string",
      "value": "Example Motors"
    }
  ]
}
```

Set `${BASE_URL}` to the root URL of a Submodel Repository or AAS Environment that exposes the `/submodels` routes. For an AAS-scoped route, insert `/shells/{aasIdentifier}` before `/submodels`.

### Normal Representation

```text
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber
```

The normal response is the complete Property model:

```json
{
  "idShort": "SerialNumber",
  "modelType": "Property",
  "valueType": "xs:string",
  "value": "SN-12345"
}
```

### `$value`

```text
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value
```

For this Property, the ValueOnly response is a JSON string:

```json
"SN-12345"
```

`$value` reduces the AAS model structure and focuses on values. It is not always a scalar: collections, lists, ranges, files, blobs, and other complex elements have structured ValueOnly JSON.

#### ValueOnly Types and Validation

Property values and Range bounds use the JSON types defined by their stored `valueType`:

| Stored type or value | ValueOnly JSON |
| --- | --- |
| Numeric XSD type, such as `xs:integer` or `xs:double` | Number, for example `42` or `21.5`. All stored digits are retained. |
| `xs:boolean` | Boolean, for example `true`. |
| Other XSD types, including `xs:string` and date/time types | String. |
| Property without a value, addressed directly or as a list member | `null`. |
| `INF`, `-INF`, `NaN`, or a stored value inconsistent with its `valueType` | String, because it has no valid JSON number/boolean representation. |

Normal model JSON uses lexical strings: an `xs:integer` Property with `"value": "42"` reads as `42` through `$value`. Preserve numeric precision when parsing large numbers.

Elements and optional fields without a value are omitted instead of being returned as `null` or empty values. This applies to members of Submodels, collections, Entity statements, and annotations, to the Submodel Element listing, to Operation result arguments, and to fields such as an unset Range bound or a Blob's `contentType`. `SubmodelElementList` members are always kept so that indices match the normal representation. Operations and Capabilities have no ValueOnly form: they are omitted, and a list that contains them is omitted as a whole.

A `$value` PATCH validates the complete payload against the **stored element types** before writing. Numeric and boolean types also accept valid lexical strings such as `"42"` or `"true"`. Other types require strings. Invalid values, incompatible JSON types, and unsupported fields in an element's ValueOnly object return `400 Bad Request`. Nonexistent elements return `404 Not Found`. Use creation routes to add them.

Omitted members remain unchanged. `null` clears a Property value, a Range bound, or the reference of a ReferenceElement. For an existing numeric Range, `{"min": null, "max": 42}` clears its lower bound and sets its upper bound.

### `$metadata`

```text
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$metadata
```

The metadata response retains the Property's model information but omits its runtime value:

```json
{
  "idShort": "SerialNumber",
  "modelType": "Property",
  "valueType": "xs:string"
}
```

A Submodel Element's metadata contains only the fields of the Part 2 metadata schema for its type. Child elements of collections, lists, Entities, and annotated relationships are not included, and neither are value fields such as `valueId`, `contentType`, `first`, `second`, `observed`, `entityType`, `globalAssetId`, `specificAssetIds`, or Operation variables. `GET .../submodel-elements/$metadata` therefore returns only top-level elements.

### `$reference`

```text
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$reference
```

The response is a ModelReference to the Property, including the containing Submodel and collection:

```json
{
  "type": "ModelReference",
  "keys": [
    {
      "type": "Submodel",
      "value": "urn:example:submodel:1"
    },
    {
      "type": "SubmodelElementCollection",
      "value": "Nameplate"
    },
    {
      "type": "Property",
      "value": "SerialNumber"
    }
  ]
}
```

Each key uses the model type of the element it refers to. The key of a `SubmodelElementList` member therefore has the member's type, such as `Property` or `SubmodelElementCollection`, and its index as value.

### `$path`

Use `level=deep` on the collection to include its descendants:

```text
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate/$path?level=deep
```

The response is an array of addressable `idShort` paths. It includes the requested collection itself, followed by its descendants in path order:

```json
[
  "Nameplate",
  "Nameplate.ManufacturerName",
  "Nameplate.SerialNumber"
]
```

These entries identify elements. They are not AAS model objects or References. With `level=core`, the response contains the path of the requested element and of its direct children.

## Depth and Blob Content

Where the read operation exposes them:

| Modifier | Effect |
| --- | --- |
| `level=deep` | Include nested content. |
| `level=core` | Include only direct children. A Submodel or list of Submodels contains its top-level elements without their children; in `$value`, those collections and lists are returned as `{}` and `[]`. |
| `extent=withoutBlobValue` | Omit Blob payload values. |
| `extent=withBlobValue` | Include Blob payload values. |

These modifiers change the response, not the stored resource. `extent` only controls inline `Blob` values. It does not include the binary content referenced by a `File` element. Retrieve that content through the corresponding `/attachment` endpoint.

Encode a Blob’s binary content as a standard Base64 string in the JSON value field when creating or updating it.

## Writing Representations

For Submodel and Submodel Element operations, the request body format depends on the endpoint you call.

| Representation | Write operations | Request body |
| --- | --- | --- |
| Normal | `POST`, `PUT`, `PATCH` | Normal Submodel or Submodel Element representation |
| `$metadata` | `PATCH` | Submodel or Submodel Element metadata representation |
| `$value` | `PATCH` | Submodel or Submodel Element ValueOnly representation |
| `$reference` | None | Read-only |
| `$path` | None | Read-only |

Normal `POST` endpoints create resources. On the Submodel and Submodel Element by-identifier or by-path endpoints, `PUT` uses the complete normal representation and creates a missing resource or replaces an existing one. A `$value` or `$metadata` response is not a complete request body for a normal `PUT`.

`PATCH` performs a partial update using the representation of its endpoint. The normal endpoint accepts fields from the normal model representation, `/$metadata` accepts the metadata representation, and `/$value` accepts ValueOnly content. For example, these Submodel Element routes have different request schemas:

```text
PATCH .../submodel-elements/{idShortPath}
PATCH .../submodel-elements/{idShortPath}/$metadata
PATCH .../submodel-elements/{idShortPath}/$value
```

For a normal Submodel Element `PATCH`, supplying a container's child-bearing field replaces its stored children rather than merging them. This applies to `value` for `SubmodelElementCollection` and `SubmodelElementList`, `statements` for `Entity`, and `annotations` for `AnnotatedRelationshipElement`: omitted children are removed, and an empty array removes all children. If the request omits the child-bearing field, existing children remain unchanged. A `$metadata` PATCH does not replace child content.

BaSyx Submodel `PATCH` endpoints use partial AAS representations, not RFC 6902 JSON Patch documents. Send the fields to update in the representation expected by the endpoint instead of an array of `op`, `path`, and `value` operations.

Write support and field-level restrictions are operation-specific. Check the running [Swagger UI](swagger) for the exact request schema and see [Submodel Repository Usage](../submodel_repository/usage.md#representations-and-partial-updates) for concrete PATCH examples.
