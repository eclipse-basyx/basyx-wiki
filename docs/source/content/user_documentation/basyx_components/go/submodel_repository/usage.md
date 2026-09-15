# Using the Submodel Repository

This walkthrough creates a motor nameplate Submodel, changes its metadata and element values, and lists Submodels with filters and pagination. You will then remove the example data.

You need only the Submodel Repository and the database services from [Setup](setup). A separate AAS Repository or Registry is not required for these examples.

## Before You Start

Start the [Compose setup](setup), then check the connection:

```bash
curl -i http://localhost:8085/health
```

Continue when the response is HTTP `200` with `{"status":"UP"}`. The examples use port `8085` and an empty context path. If your configuration differs, replace `http://localhost:8085` throughout; include any context path, for example `http://localhost:8085/api/v3`. You can also inspect requests in [Swagger UI](http://localhost:8085/swagger).

Run commands from one working directory and save each JSON file there before the command that uses it. Use the filenames shown, including the `.json` extension, and save as UTF-8. No additional scripts or JSON command-line tools are needed.

- **Bash:** copy the commands as shown.
- **Windows PowerShell:** replace `curl` with `curl.exe`; this avoids the PowerShell alias.
- **Request files:** `--data-binary '@submodel.json'` reads the file from the current directory and sends it as the request body.
- **Responses:** `-i` displays HTTP headers and the body. A successful `204 No Content` response intentionally has no JSON body; use GET to check the new state.

The commands assume the unsecured example setup. For an existing secured deployment, use credentials and permissions appropriate to that deployment. Run the walkthrough on example data: it creates and later deletes `urn:example:submodel:1` and `urn:example:submodel:2`.

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

```bash
curl -i -X POST http://localhost:8085/submodels -H 'Content-Type: application/json' --data-binary '@submodel.json'
```

Expect `201 Created` and a JSON body containing `id: "urn:example:submodel:1"` and `idShort: "MotorNameplate"`. The Submodel is now stored in the Repository. Generating a Registry descriptor requires [Registry Integration](registry_integration) or explicit registration; neither is needed to continue here.

If you repeat this step, `409 Conflict` means the visible identifier already exists. Continue with that resource only if it is your earlier example, or use different identifiers consistently throughout the walkthrough. The AAS Repository walkthrough uses the same Submodel identifier, so its content may already exist if both services share a database.

## Retrieve and Replace the Submodel

The request URL uses the encoded **Submodel identifier**, not its `idShort` or semantic identifier:

| Original identifier | Base64URL path value |
| --- | --- |
| `urn:example:submodel:1` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ` |
| `urn:example:submodel:2` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6Mg` |

These values are already substituted into every example URL. Keep identifiers in JSON bodies unencoded. For your own identifiers, see [Encoding Your Own Identifiers](#encoding-your-own-identifiers).

```bash
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `200 OK` and the Submodel. Change `idShort` in `submodel.json` to `MotorNameplateUpdated`, then submit the complete document:

```bash
curl -i -X PUT http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel.json'
```

Expect `204 No Content` for replacement. Verify it:

```bash
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

The response should now contain `"idShort": "MotorNameplateUpdated"` and the original elements. PUT creates a missing Submodel with `201 Created`. The body's `id` must match the decoded path identifier; a mismatch returns `400 Bad Request`.

PUT replaces the complete Submodel. Later in this walkthrough you will change elements through separate API calls. Those calls do not update your local `submodel.json`. Before replacing the Submodel again, retrieve its current state and preserve the elements, values, and metadata you want to keep. Reusing the initial file would undo those later changes.

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

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

### Create a Second Submodel

Add a second Submodel so you can try pagination with two resources. Save this as `second-submodel.json`:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:2",
  "idShort": "PumpNameplate"
}
```

```bash
curl -i -X POST http://localhost:8085/submodels -H 'Content-Type: application/json' --data-binary '@second-submodel.json'
```

Expect `201 Created`. Your example database now contains `MotorNameplateUpdated` and `PumpNameplate`.

### Read One Submodel per Page

Request the collection without filters so both Submodels are eligible. Set `limit=1` to return at most one Submodel in each response:

```bash
curl -i -G http://localhost:8085/submodels --data-urlencode 'limit=1'
```

Expect `200 OK`. The body contains one Submodel in `result` and a non-empty `paging_metadata.cursor` indicating that another page is available. Copy that cursor string into the next request:

```bash
curl -i -G http://localhost:8085/submodels --data-urlencode 'limit=1' --data-urlencode 'cursor=RETURNED_CURSOR'
```

Replace `RETURNED_CURSOR` with the value from the first response, without its surrounding JSON quotes. In a database containing only these two Submodels, the second response contains the other Submodel and has no next cursor. If additional Submodels exist, keep following the returned cursor until none is supplied.

See [Limit and Cursor](../common/pagination.md#limit-and-cursor) for the general rules when adapting this example.

### Filter the Collection

Now select only the motor nameplate Submodel by its short name:

```bash
curl -i -G http://localhost:8085/submodels --data-urlencode 'idShort=MotorNameplateUpdated'
```

Expect `200 OK` with only `MotorNameplateUpdated` in `result`. `PumpNameplate` does not match the filter. There is no need to force pagination for this single match.

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

## Delete the Example Content

Once you have finished, delete both example Submodels. If continuing with the [AAS Repository walkthrough](../aas_repository/usage), postpone deleting the motor nameplate until you finish using it. Consider every AAS/client that uses the same identifier before deleting shared content.

```bash
curl -i -X DELETE http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6Mg
```

Expect `204 No Content` for each existing Submodel. Deleting a Submodel also deletes its contained elements. Verify the motor nameplate is no longer available:

```bash
curl -i http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

The expected `404 Not Found` confirms deletion. The example identifiers can now be used for a fresh walkthrough.

## Encoding Your Own Identifiers

Use the shared [Identifiers and Encoding](../common/encoding) guide for Bash and PowerShell commands. For resource URLs, encode the Submodel's `id`; keep element `idShortPath` values unencoded. For this implementation's `semanticId` filter, encode the semantic key-value string, such as `urn:example:semantic:nameplate`, rather than the complete reference JSON. Keep identifiers and reference key values in JSON bodies unencoded.

## Shared API Guidance

See [Identifiers and Encoding](../common/encoding), [Validation](../common/validation), [API Errors](../common/api_errors), and [History, Timestamps, and Signed Reads](../common/history_and_changes). For available model views, see [Response Representations](../common/representations). Component-specific requests and lifecycle behavior are documented above.
