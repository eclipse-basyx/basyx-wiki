# Response Representations

BaSyx Go Repository APIs expose different views of the same model content through distinct endpoints. A normal read uses the resource endpoint without a representation suffix; the other representations append `/$value`, `/$metadata`, `/$reference`, or `/$path`. Query parameters such as `level` and `extent` modify supported responses but do not select a representation.

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

```http
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

```http
GET ${BASE_URL}/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value
```

For this Property, the ValueOnly response is a JSON string:

```json
"SN-12345"
```

`$value` reduces the AAS model structure and focuses on values. It is not always a scalar: collections, lists, ranges, files, blobs, and other complex elements have structured ValueOnly JSON.

### `$metadata`

```http
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

For structured elements, the metadata representation retains the nested model hierarchy while removing values according to each element type's metadata rules.

### `$reference`

```http
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

### `$path`

Use `level=deep` on the collection to include its descendants:

```http
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

These entries identify elements; they are not AAS model objects or References.

When using curl, quote URLs containing a dollar-sign suffix so the shell does not expand it. In PowerShell, use `curl.exe` when following curl examples.

## Depth and Blob Content

Where the read operation exposes them:

| Modifier | Effect |
| --- | --- |
| `level=deep` | Include nested content. |
| `level=core` | Limit the representation to its core level. |
| `extent=withoutBlobValue` | Omit Blob payload values. |
| `extent=withBlobValue` | Include Blob payload values. |

These modifiers change the response, not the stored resource. They do not download a File element's attachment. Use the component's attachment endpoint for that.

## Writing a Representation

Use the request schema of the specific write endpoint. A `$value` response is not a complete resource body for a normal PUT. Submodel PATCH routes expect their corresponding normal, metadata, or value representation, rather than an RFC 6902 JSON Patch array. Keep resource-specific PATCH examples in [Submodel Repository Usage](../submodel_repository/usage).

For Submodel Element `$metadata` PATCH requests, this implementation accepts common metadata fields such as `description`, but rejects `valueType`. The existing Property datatype is retained. See the [metadata PATCH example](../submodel_repository/usage.md#representations-and-partial-updates).

Operation invocation has separate normal and `$value` endpoints. In the stable release, delegated asynchronous Operation invocation through the `$value` endpoint is not supported; see [Asynchronous Operation Invocation](asynchronous_requests.md#asynchronous-operation-invocation).

Full Environment import/export is a separate capability; representation suffixes do not imply support for `/serialization` in a standalone service.
