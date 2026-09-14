# Using the AAS Repository

This walkthrough creates a motor AAS, changes its asset information, and stores a nameplate Submodel through the Go AAS Repository. You will then read the Submodel through the AAS, manage its reference, and remove the example data.

You need only the AAS Repository and the database services from [Setup](setup). A separate Registry or Submodel Repository service is not required for these examples.

## Before You Start

Start the [Compose setup](setup), then check the connection:

```bash
curl -i http://localhost:8084/health
```

Continue when the response is HTTP `200` with `{"status":"UP"}`. The examples use port `8084` and an empty context path. If your configuration differs, replace `http://localhost:8084` throughout; include any context path, for example `http://localhost:8084/api/v3`. You can also inspect requests in [Swagger UI](http://localhost:8084/swagger).

Run commands from one working directory and save each JSON file there before the command that uses it. Use the filenames shown, including the `.json` extension, and save as UTF-8. No additional scripts or JSON command-line tools are needed.

- **Bash:** copy the commands as shown.
- **Windows PowerShell:** replace `curl` with `curl.exe`; this avoids the PowerShell alias.
- **Request files:** `--data-binary '@aas.json'` reads the file from the current directory and sends it as the request body.
- **Responses:** `-i` displays HTTP headers and the body. A successful `204 No Content` response intentionally has no JSON body; use GET to check the new state.

The commands assume the unsecured example setup. For an existing secured deployment, use credentials and permissions appropriate to that deployment. Run the walkthrough on example data: it creates and later deletes `urn:example:aas:1`, `urn:example:aas:2`, and `urn:example:submodel:1`.

## Create an AAS

Save this as `aas.json`:

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:1",
  "idShort": "MotorAAS",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:1",
    "assetType": "Motor",
    "specificAssetIds": [
      { "name": "serialNumber", "value": "SN-001" }
    ]
  }
}
```

| Field | Purpose |
| --- | --- |
| `id` | Globally unique AAS identifier, used to address the AAS. |
| `idShort` | Optional short name, useful for recognition and filtering. |
| `assetInformation` | Required information about the represented asset. |
| `assetKind` | Kind of asset, here a particular `Instance`. |
| `globalAssetId` | Global identifier of the asset; distinct from the AAS identifier. |
| `specificAssetIds` | Additional asset identifiers, such as a serial number. |
| `submodels` | Optional array of model references to Submodels, added later in this walkthrough. |

```bash
curl -i -X POST http://localhost:8084/shells -H 'Content-Type: application/json' --data-binary '@aas.json'
```

Expect `201 Created` and a JSON body containing `id: "urn:example:aas:1"` and `idShort: "MotorAAS"`. The AAS is now stored in the Repository. Generating a Registry descriptor requires [Registry Integration](registry_integration) or explicit registration; neither is needed to continue here.

If you repeat this step, `409 Conflict` means the visible identifier already exists. Continue with that resource only if it is your earlier example, or use different identifiers consistently throughout the walkthrough.

## Retrieve and Replace the AAS

The request URL uses the encoded **AAS identifier**, not the asset identifier or `idShort`:

| Original identifier | Base64URL path value |
| --- | --- |
| `urn:example:aas:1` | `dXJuOmV4YW1wbGU6YWFzOjE` |
| `urn:example:submodel:1` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ` |

These values are already substituted into every example URL. Keep identifiers in JSON bodies unencoded. For your own identifiers, use UTF-8 and the URL-safe Base64 alphabet; see [Encoding Your Own Identifiers](#encoding-your-own-identifiers).

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK`. Change `idShort` in `aas.json` to `MotorAASUpdated` and PUT the complete document:

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE -H 'Content-Type: application/json' --data-binary '@aas.json'
```

Expect `204 No Content` for replacement. Verify it:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

The response should now contain `"idShort": "MotorAASUpdated"` and the original asset information. PUT creates a missing AAS with `201 Created`; the body `id` must match the decoded path identifier.

PUT replaces the complete AAS. Later in this walkthrough you will add a Submodel reference through a separate API call; that call does not update your local `aas.json`. Before replacing the AAS again, retrieve its current state and preserve the references and metadata you want to keep. Reusing the initial file would omit the new reference.

## Asset Information

Read asset information independently of the AAS:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information
```

Expect `200 OK` with the asset information object. Save a replacement as `asset-information.json`:

```json
{
  "assetKind": "Instance",
  "globalAssetId": "urn:example:asset:1",
  "assetType": "Motor",
  "specificAssetIds": [
    { "name": "serialNumber", "value": "SN-002" }
  ]
}
```

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information -H 'Content-Type: application/json' --data-binary '@asset-information.json'
```

Expect `204 No Content`. The serial number changes while the AAS identifier, short name, and references are retained. This replaces asset information, so include its fields that should remain.

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information
```

Check that `specificAssetIds` now contains `serialNumber` with value `SN-002`. Use this smaller endpoint when only asset information needs to change; you do not need to resubmit the complete AAS.

## AAS-scoped Submodel Access

Next, add a small nameplate Submodel. Save this complete example as `submodel.json` in the same directory:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:1",
  "idShort": "MotorNameplate",
  "submodelElements": [
    {
      "modelType": "SubmodelElementCollection",
      "idShort": "Nameplate",
      "value": [
        {
          "modelType": "Property",
          "idShort": "SerialNumber",
          "valueType": "xs:string",
          "value": "SN-002"
        }
      ]
    }
  ]
}
```

Store it through the AAS Repository:

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel.json'
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

The parent AAS must exist. PUT stores the Submodel and ensures its reference exists in that AAS in one transaction. Expect `201 Created` on a fresh example database, or `204 No Content` if that Submodel already exists. GET returns `200 OK` with `idShort: "MotorNameplate"` and the nameplate collection. You do not need to POST a reference separately after this PUT.

The Submodel's serial number deliberately matches the asset information in this example. These are separate stored values: updating one does not automatically update the other.

The standalone AAS Repository uses local database-backed Submodel storage for these routes. It does not follow a Registry endpoint to fetch a remote Submodel.

Individual element operations are available below the AAS-scoped path as well:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber
```

Expect `200 OK` with a Property containing `idShort: "SerialNumber"`, `valueType: "xs:string"`, and `value: "SN-002"`. `Nameplate.SerialNumber` is a dot-separated `idShortPath` and is not Base64URL-encoded.

See the [Submodel Element walkthrough](../submodel_repository/usage.md#submodel-element-paths) when you need additional element operations. Replace its `/submodels/{submodelIdentifier}` prefix with the AAS-scoped prefix when using these routes.

Unlike removing a reference, DELETE on `/shells/{aasIdentifier}/submodels/{submodelIdentifier}` removes the reference and the Submodel content. Be careful because other AASs may use that same content.

## Submodel References

The previous Submodel PUT also linked the Submodel to the AAS. Check that reference first:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodel-refs
```

Expect `200 OK` with a reference whose key has `type: "Submodel"` and `value: "urn:example:submodel:1"` in the `result` array. The reference identifies the Submodel. It contains neither the Submodel content nor an endpoint URL.

To unlink it without deleting its stored content:

```bash
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodel-refs/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodel-refs
```

The DELETE returns `204 No Content`; for this example the reference list is now empty. AAS-scoped GET of the Submodel will return `404` while the reference is absent, even though the content remains stored.

Restore the link by saving this as `submodel-reference.json`:

```json
{
  "type": "ModelReference",
  "keys": [
    { "type": "Submodel", "value": "urn:example:submodel:1" }
  ]
}
```

```bash
curl -i -X POST http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodel-refs -H 'Content-Type: application/json' --data-binary '@submodel-reference.json'
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodel-refs
```

Expect `201 Created` for the restored reference, then `200 OK` with it in the list. This is also the operation to use when you only want to link an existing Submodel. It does not upload content or fetch a remote Submodel.

Read the Submodel again using the AAS-scoped GET from the previous section. It is accessible again without re-uploading its content.

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

### Create a Second AAS

Pagination is useful when a collection contains more entries than one response should return. Add a second AAS so you can try this with two resources. Save the following as `second-aas.json`:

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:2",
  "idShort": "PumpAAS",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:2",
    "assetType": "Pump"
  }
}
```

```bash
curl -i -X POST http://localhost:8084/shells -H 'Content-Type: application/json' --data-binary '@second-aas.json'
```

Expect `201 Created`. Your example database now contains `MotorAASUpdated` and `PumpAAS`.

### Read One AAS per Page

Request the collection without an `idShort` filter so both AASs are eligible. Set `limit=1` to return at most one AAS in each response:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'limit=1'
```

Expect `200 OK`. The body contains a `result` array with one AAS and a non-empty `paging_metadata.cursor` indicating that another page is available. Inspect the returned AAS's `id`, then copy the cursor string into the next request:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'limit=1' --data-urlencode 'cursor=RETURNED_CURSOR'
```

Replace `RETURNED_CURSOR` with the value from the first response, without the surrounding JSON quotes. The second response contains the other AAS. In a database containing only these two AASs, it has no next cursor: you have reached the end of the collection. If your database has additional AASs, keep following each returned cursor until none is supplied.

See [Limit and Cursor](../common/pagination.md#limit-and-cursor) for the general rules when adapting this example.

### Filter the Collection

Now select only the motor AAS by its short name:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'idShort=MotorAASUpdated'
```

Expect `200 OK` with only `MotorAASUpdated` in `result`. `PumpAAS` does not match the filter. There is no need to force pagination for this single match.

| Parameter | Meaning |
| --- | --- |
| `idShort` | Plain short-name filter. |
| `assetIds` | Asset identifier filter; each value is Base64URL-encoded JSON for a `SpecificAssetId`. |
| `limit`, `cursor` | Page size and continuation cursor. |
| `createdFrom`, `updatedFrom` | RFC 3339 lower bounds on administrative creation/update timestamps. |

After the asset-information step above, the serial number is `SN-002`. The following ready-to-run request searches for that value. Its `assetIds` value is the Base64URL encoding of `{"name":"serialNumber","value":"SN-002"}`:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'assetIds=eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDIifQ'
```

Expect your AAS in `result`. Searching for `SN-001` after changing it to `SN-002` would return no match. For your own asset filters, encode the complete JSON object using the [encoding commands](#encoding-your-own-identifiers). Use `{"name":"globalAssetId","value":"urn:example:asset:1"}` for the global asset identifier. Normal URL escaping is separate from Base64URL encoding; `--data-urlencode` handles it here.

Timestamp filters use administrative timestamps supplied in the AAS payload. Writes do not automatically generate or overwrite `administration.createdAt` and `administration.updatedAt`; the example does not supply them. Current-resource lists do not report deletions. Ordinary list parameters select supported attributes; structured query expressions belong to `POST /query/shells` and are not arbitrary additional list parameters. Consult the running Swagger UI for the query schema in your component version.

## Asset Thumbnail

This section is optional. If you want to try it, place an existing PNG image named `thumbnail.png` in your working directory. Upload it using multipart form fields `fileName` and `file`:

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information/thumbnail -F 'fileName=thumbnail.png' -F 'file=@thumbnail.png;type=image/png'
```

Expect `204 No Content`. Let curl set the multipart boundary; do not set an application/json header for this request. Download the thumbnail and save response headers separately:

```bash
curl -D thumbnail-headers.txt -o downloaded-thumbnail.png http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information/thumbnail
```

A stored thumbnail returns `200 OK` with binary content and its response content type. Open `downloaded-thumbnail.png` to verify the result; HTTP headers are in `thumbnail-headers.txt`. Repeat PUT with another image to replace it. When asset information points to an external HTTP(S) thumbnail, GET can instead return `302` with the external location.

```bash
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/asset-information/thumbnail
```

Expect `204 No Content`. Deleting the thumbnail does not delete the AAS.

## Delete the Example Content

Once you have finished, delete the example Submodel through the motor AAS, then delete both AASs. The reference must still be present, so restore it first if you stopped partway through the reference-management section. The pump AAS added for pagination has no Submodel to clean up.

| Request | What it removes |
| --- | --- |
| DELETE the `/submodel-refs/{submodelIdentifier}` route | Only the link from this AAS. |
| DELETE the `/submodels/{submodelIdentifier}` route below the AAS | The link and the stored Submodel content. |

The commands below intentionally use the second operation:

```bash
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjI
```

Expect `204 No Content` for each existing resource. Subsequent GET requests return `404`. Perform this cleanup after completing any Submodel Repository examples that share the same database and identifier.

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

The expected `404` confirms the AAS is no longer available. The example identifiers can now be used for a fresh walkthrough.

## Encoding Your Own Identifiers

Use the shared [Identifiers and Encoding](../common/encoding) guide for Bash and PowerShell commands. For this walkthrough, encode the AAS `id`, not its asset identifier. For `assetIds`, encode the complete JSON object, such as `{"name":"serialNumber","value":"SN-002"}`. Keep identifiers in request bodies and reference key values unencoded.

## Shared API Guidance

See [Identifiers and Encoding](../common/encoding), [Validation](../common/validation), [API Errors](../common/api_errors), and [History, Timestamps, and Signed Reads](../common/history_and_changes). For available model views, see [Response Representations](../common/representations). Component-specific requests and lifecycle behavior are documented above.
