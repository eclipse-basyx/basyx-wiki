# Using the Submodel Repository

This walkthrough uses the unsecured [Compose setup](setup) at `http://localhost:8085`, with an empty context path. Run the examples in order against an example database. Save the JSON files as UTF-8 in your working directory. In PowerShell, use `curl.exe` instead of `curl`. Prefix API paths with `server.contextPath` when configured.

## Create a Submodel

Save this as `submodel.json`:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:1",
  "idShort": "MotorNameplate",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [
      { "type": "GlobalReference", "value": "urn:example:semantic:nameplate" }
    ]
  },
  "submodelElements": [
    {
      "modelType": "Property",
      "idShort": "ManufacturerName",
      "valueType": "xs:string",
      "value": "Example Motors"
    },
    {
      "modelType": "SubmodelElementCollection",
      "idShort": "Nameplate",
      "value": [
        {
          "modelType": "Property",
          "idShort": "SerialNumber",
          "valueType": "xs:string",
          "value": "SN-001"
        }
      ]
    }
  ]
}
```

| Field | Purpose |
| --- | --- |
| `id` | Globally unique Submodel identifier used for resource addressing. |
| `idShort` | Short name used for recognition and list filtering. |
| `semanticId` | Reference to the definition of the Submodel's meaning; the example uses an illustrative identifier. |
| `submodelElements` | The actual content: Properties, collections, lists, and other element types. |
| `modelType` | Identifies the concrete type in normal JSON serialization. |
| Property `valueType` | XML Schema datatype of the Property's value. |

```bash
curl -i -X POST http://localhost:8085/submodels -H 'Content-Type: application/json' --data-binary '@submodel.json'
```

Expect `201 Created` and the created Submodel. Repeating POST with the same visible identifier returns `409 Conflict`. This stores Submodel content; [Registry Integration](registry_integration) is a separate, optional feature for generating its descriptor.

## Identifier Encoding

The identifier `urn:example:submodel:1` becomes `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ` when encoded as unpadded UTF-8 Base64URL. Keep the original identifier in JSON bodies.

Use [Identifiers and Encoding](../common/encoding) for Bash and PowerShell commands.

## Retrieve and Replace the Submodel

```bash
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `200 OK` and the Submodel. Change `idShort` in `submodel.json` to `MotorNameplateUpdated`, then submit the complete document:

```bash
curl -i -X PUT http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel.json'
```

Expect `204 No Content` for replacement. PUT creates a missing Submodel with `201 Created`. The body's `id` must match the decoded path identifier; a mismatch returns `400 Bad Request`. Include every element and metadata field that should remain. GET again to inspect the result.

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

```bash
curl -i -G http://localhost:8085/submodels --data-urlencode 'idShort=MotorNameplateUpdated' --data-urlencode 'limit=10'
```

Expect `200 OK` with matching Submodels in `result`. The single example normally fits on one page; for larger collections, follow the [next-cursor procedure](../common/pagination#follow-the-next-cursor) with the same filters.

| Parameter | Meaning |
| --- | --- |
| `idShort` | Plain short-name filter. |
| `semanticId` | Base64URL-encoded semantic key-value string matched against `semanticId.keys[].value` by this implementation. |
| `limit`, `cursor` | Page size and continuation cursor. |
| `createdFrom`, `updatedFrom` | RFC 3339 lower bounds on administrative creation/update timestamps. |
| `level`, `extent` | Representation controls described below. |

For the example's semantic identifier, encode the string `urn:example:semantic:nameplate`, not the complete reference JSON:

```bash
curl -i -G http://localhost:8085/submodels --data-urlencode 'semanticId=dXJuOmV4YW1wbGU6c2VtYW50aWM6bmFtZXBsYXRl'
```

The decoded value is compared with semantic reference key values; this is not an equality comparison of an entire multi-key reference. This describes the current Go implementation; use the runtime contract when comparing it with the standardized semantic-reference parameter.

Timestamp filters use `administration.createdAt` and `administration.updatedAt` supplied in the resource payload, rather than automatically recording each write. The example does not supply them. Maintain those fields if using timestamp-filtered lists; current-resource lists do not provide deletion notifications.

Ordinary filters select resources by these defined parameters. Structured queries can express combinations and conditions on element values; see the running API documentation for `/query/submodels`. Adding arbitrary field names as list query parameters does not create a structured query.

## Submodel Element Paths

The Submodel identifier is encoded; `idShortPath` is not. Use dot-separated names to address nested elements:

| Path | Target |
| --- | --- |
| `ManufacturerName` | Top-level Property in this example. |
| `Nameplate` | Top-level collection. |
| `Nameplate.SerialNumber` | Property inside that collection. |
| `Measurements[0]` | First member of a list named `Measurements`, if such a list exists. |

List indices are zero-based and can change when list content changes. List members are addressed by index rather than their own `idShort`. Apply normal URL escaping to path characters when constructing requests. With curl, use `--globoff` when a URL contains list brackets so curl does not interpret them as a URL range.

```bash
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber
```

Expect `200 OK` and the Property, including `modelType`, `idShort`, `valueType`, and `value`.

## Create, Replace, and Delete an Element

Save this as `property.json`:

```json
{
  "modelType": "Property",
  "idShort": "ProductCode",
  "valueType": "xs:string",
  "value": "MOTOR-100"
}
```

Add it at the top level:

```bash
curl -i -X POST http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements -H 'Content-Type: application/json' --data-binary '@property.json'
```

Expect `201 Created` and the element. To add a child to an existing collection instead, POST to the collection's path, for example `/submodel-elements/Nameplate`, with a child element body.

Change `value` in `property.json` to `MOTOR-200` and replace the top-level Property:

```bash
curl -i -X PUT http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/ProductCode -H 'Content-Type: application/json' --data-binary '@property.json'
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/ProductCode
```

Expect `204 No Content` for replacement, then `200 OK` with the new value. Preserve the addressed element's `idShort` and supply the complete element. PUT can create a missing element when its parent exists; use POST to the parent when adding a new child explicitly.

```bash
curl -i -X DELETE http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/ProductCode
```

Expect `204 No Content`; a subsequent GET of that element returns `404`. Other elements remain available.

## Representations and Partial Updates

See [Response Representations](../common/representations) for the meaning of each suffix and the supported depth and Blob modifiers. The following examples show the Submodel-specific request and response shapes.

These representations have distinct schemas. Do not send a normal Property object to a value-only endpoint. For example:

```bash
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value'
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/$metadata'
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/$reference'
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/$path'
```

The first request returns the JSON string `"SN-001"`. Save the new value as `serial-value.json`:

```json
"SN-002"
```

```bash
curl -i -X PATCH 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value' -H 'Content-Type: application/json' --data-binary '@serial-value.json'
```

Expect `204 No Content`. GET the normal Property again: `value` is now `SN-002`, while `idShort` and `valueType` are retained. This changes the existing value without replacing the collection or Submodel.

To update metadata, save this as `serial-metadata.json`:

```json
{
  "modelType": "Property",
  "idShort": "SerialNumber",
  "description": [
    { "language": "en", "text": "Manufacturer-assigned serial number" }
  ]
}
```

```bash
curl -i -X PATCH 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$metadata' -H 'Content-Type: application/json' --data-binary '@serial-metadata.json'
```

Expect `204 No Content`. The normal Property now includes the description and retains the previously stored `SN-002` value and `xs:string` datatype. This implementation accepts common metadata fields in a Submodel Element `$metadata` PATCH, but rejects `valueType`; omit it from this payload.

PATCH on normal, metadata, and value endpoints expects the corresponding representation, not an RFC 6902 array of `op`/`path` instructions. Use element creation routes to add elements, complete PUT bodies to replace resources, and the relevant PATCH representation to update existing content. A `$metadata` update changes metadata while retaining values; follow its schema in Swagger rather than including value fields in that payload.

See [Response Representations](../common/representations) for the shared meaning of `level` and `extent`. For example:

```bash
curl -i -G http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ --data-urlencode 'level=deep' --data-urlencode 'extent=withoutBlobValue'
```

Keep URLs containing `$value`, `$metadata`, `$reference`, or `$path` in single quotes so the shell does not expand the dollar sign.

## Delete the Example Submodel

If continuing with the [AAS Repository walkthrough](../aas_repository/usage), postpone this cleanup until you finish using the Submodel.

```bash
curl -i -X DELETE http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `204 No Content`; the Submodel and its contained elements are deleted. Subsequent retrieval returns `404`. Consider every AAS/client that uses the same identifier before deleting shared content.

## Shared API Guidance

See [Identifiers and Encoding](../common/encoding), [Validation](../common/validation), [API Errors](../common/api_errors), and [History, Timestamps, and Signed Reads](../common/history_and_changes). For available model views, see [Response Representations](../common/representations). Component-specific requests and lifecycle behavior are documented above.
