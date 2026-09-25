# Using the AAS Repository

This walkthrough creates a motor AAS, changes its asset information, and stores a nameplate Submodel through the Go AAS Repository. You will then read the Submodel through the AAS, manage its reference, and remove the example data.

You need only the AAS Repository and the database services from [Setup](setup). A separate Registry or Submodel Repository service is not required for these examples.

## Before You Start

Start the [Compose setup](setup), then check the connection:

```bash
curl -i http://localhost:8084/health
```

Continue when the response is HTTP `200` with `{"status":"UP"}`. The examples use port `8084` and an empty context path. If your configuration differs, replace `http://localhost:8084` throughout. Include any context path, for example `http://localhost:8084/api/v3`. You can also inspect requests in [Swagger UI](http://localhost:8084/swagger).

Run commands from one working directory and save each JSON file there before the command that uses it. Use the filenames shown, including the `.json` extension. No additional scripts or JSON command-line tools are needed.

- **Bash:** copy the commands as shown.
- **Windows PowerShell:** replace `curl` with `curl.exe`; this avoids the PowerShell alias.
- **Request files:** `--data-binary '@aas.json'` reads the file from the current directory and sends it as the request body.
- **Responses:** `-i` displays HTTP headers and the body. A successful `204 No Content` response intentionally has no JSON body; use GET to check the new state.

The commands assume the unsecured example setup. For an existing secured deployment, use credentials and permissions appropriate to that deployment. Run the walkthrough on example data: it creates and later deletes `urn:example:aas:1`, `urn:example:aas:2`, `urn:example:aas:history`, and `urn:example:submodel:1`.

## Create an AAS

Save this as `aas.json`:

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:1",
  "idShort": "MotorAAS",
  "administration": {
    "createdAt": "2026-09-01T10:00:00Z",
    "updatedAt": "2026-09-02T10:00:00Z"
  },
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

```bash
curl -i -X POST http://localhost:8084/shells -H 'Content-Type: application/json' --data-binary '@aas.json'
```

Expect `201 Created` and a JSON body containing `id: "urn:example:aas:1"` and `idShort: "MotorAAS"`. The AAS is now stored in the Repository. Generating a Registry descriptor requires [Registry Integration](registry_integration) or explicit registration; neither is needed to continue here.

If you need to import an AAS together with referenced Submodels and Concept Descriptions from JSON, XML, or AASX instead of creating resources individually, use the combined [AAS Environment import workflow](../aas_environment/usage.md#import-an-environment).

If you repeat this step, `409 Conflict` means the visible identifier already exists. Continue with that resource only if it is your earlier example, or use different identifiers consistently throughout the walkthrough.

## Retrieve and Replace the AAS

The request URL uses the encoded **AAS identifier**, not the asset identifier or `idShort`:

| Original identifier | Base64URL path value |
| --- | --- |
| `urn:example:aas:1` | `dXJuOmV4YW1wbGU6YWFzOjE` |
| `urn:example:aas:history` | `dXJuOmV4YW1wbGU6YWFzOmhpc3Rvcnk` |
| `urn:example:submodel:1` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ` |

These values are already substituted into every example URL. Keep identifiers in JSON bodies unencoded.

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

The response should now contain `"idShort": "MotorAASUpdated"` and the original asset information. PUT creates a missing AAS with `201 Created`. The body `id` must match the decoded path identifier.

PUT replaces the complete AAS. Later in this walkthrough you will add a Submodel reference through a separate API call. This call does not update your local `aas.json`. Before replacing the AAS again, retrieve its current state and preserve the references and metadata you want to keep. Reusing the initial file would omit the new reference. Omitting a previously referenced Submodel removes that reference from the AAS, but does not delete or garbage-collect the separately stored Submodel content.

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

Submodel storage is shared by Submodel ID. This route does not create a Submodel copy owned by the parent AAS. If two AASs reference `urn:example:submodel:1`, replacing it through either AAS updates the same stored content, and reads through both references return the updated Submodel.

The Submodel's serial number deliberately matches the asset information in this example. These are separate stored values: updating one does not automatically update the other.

The standalone AAS Repository uses local database-backed Submodel storage for these routes. It does not follow a Registry endpoint to fetch a remote Submodel.

Individual element operations are available below the AAS-scoped path as well:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber
```

Expect `200 OK` with a Property containing `idShort: "SerialNumber"`, `valueType: "xs:string"`, and `value: "SN-002"`. `Nameplate.SerialNumber` is a dot-separated `idShortPath` and is not Base64URL-encoded.

See the [Submodel Element walkthrough](../submodel_repository/usage.md#submodel-element-paths) when you need additional element operations. Replace its `/submodels/{submodelIdentifier}` prefix with the AAS-scoped prefix when using these routes.

Unlike removing a reference, DELETE on `/shells/{aasIdentifier}/submodels/{submodelIdentifier}` removes the reference from the addressed AAS and deletes the shared Submodel content. It does not remove references from other AASs.

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

## Resource Lifecycle

Submodel references and Submodel content have separate lifecycles:

| Operation | Endpoint | Effect |
| --- | --- | --- |
| Delete a Submodel reference | `DELETE /shells/{aasIdentifier}/submodel-refs/{submodelIdentifier}` | Removes only the relationship from the addressed AAS. Shared Submodel content remains stored. |
| Delete an AAS-scoped Submodel | `DELETE /shells/{aasIdentifier}/submodels/{submodelIdentifier}` | Removes the reference from the addressed AAS and deletes the shared Submodel content. References in other AASs are not removed. |
| Delete an AAS | `DELETE /shells/{aasIdentifier}` | Deletes the AAS and all of its Submodel references. Referenced Submodel content remains stored. |
| Replace a complete AAS | `PUT /shells/{aasIdentifier}` | Replaces the AAS and its reference set. Omitted references are removed, but their Submodel content remains stored. |

```{warning}
Suppose AAS A and AAS B both reference Submodel X. Deleting X through AAS A deletes the single shared Submodel X and removes AAS A's reference. AAS B can retain its reference to X, but an AAS-scoped read through B then has no Submodel content to return. Remove or reconcile such remaining references explicitly.
```

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

### Find Recently Changed AASs

The motor AAS created earlier contains client-supplied `administration.createdAt` and `administration.updatedAt` values. Query the dedicated recent-changes endpoint for AASs updated at or after the given RFC 3339 time:

```bash
curl -i -G 'http://localhost:8084/shells/$recent-changes' \
  --data-urlencode 'updatedFrom=2026-09-02T00:00:00Z'
```

Expect `200 OK`. On a database containing only the walkthrough resources, the response is:

```json
{
  "paging_metadata": {},
  "result": [
    {
      "createdAt": "2026-09-01T10:00:00Z",
      "updatedAt": "2026-09-02T10:00:00Z",
      "id": "urn:example:aas:1",
      "globalAssetId": "urn:example:asset:1",
      "specificAssetIds": [
        {
          "name": "serialNumber",
          "value": "SN-002"
        }
      ]
    }
  ]
}
```

The response contains summary entries, not complete AAS resources. `id`, `createdAt`, and `updatedAt` are required in each entry; asset identifiers are included when present on the AAS. An empty `paging_metadata` object means there is no next page. When another page is available, it contains a `cursor` to pass in the next request.

Resources without valid administrative timestamps are excluded, and deleted resources are not returned. This endpoint is a timestamp-filtered view of current resources, not a mutation history or deletion feed.

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

Expect your AAS in `result`. Searching for `SN-001` after changing it to `SN-002` would return no match. For your own asset filters, encode the complete JSON object's UTF-8 bytes with Base64URL. Use `{"name":"globalAssetId","value":"urn:example:asset:1"}` for the global asset identifier. Normal URL escaping is separate from Base64URL encoding; `--data-urlencode` handles it here.

Timestamp filters use administrative timestamps supplied in the AAS payload. Writes do not automatically generate or overwrite `administration.createdAt` and `administration.updatedAt`; see [Find Recently Changed AASs](#find-recently-changed-aass) for a complete example. Current-resource lists do not report deletions. Ordinary list parameters select supported attributes; structured query expressions belong to `POST /query/shells` and are not arbitrary additional list parameters. Consult the running Swagger UI for the query schema in your component version.

### Query AAS Data

`POST /query/shells` accepts structured AAS queries. Save this AAS-level query as `query.json`:

```json
{
  "$condition": {
    "$eq": [
      { "$field": "$aas#idShort" },
      { "$strVal": "MotorAASUpdated" }
    ]
  }
}
```

Send it to the query endpoint:

```bash
curl -i -X POST http://localhost:8084/query/shells -H 'Content-Type: application/json' --data-binary '@query.json'
```

Expect `200 OK` with `MotorAASUpdated` in the `result` array. `limit` and `cursor` can be supplied as query parameters for pagination.

The standalone AAS Repository supports structured queries over AAS data only. Expressions that use `$sm` or `$sme` to traverse into referenced Submodels or Submodel Elements return `400 Bad Request`; use the [AAS Environment Service](../aas_environment/index) for those hierarchy-spanning queries.

## Read a Historical AAS State

History recording must be enabled before the mutations you want to retrieve are performed. For the Compose setup, add `BASYX_HISTORY_MODE=api` to the `aas_repository` service environment and recreate that service:

```yaml
environment:
  - BASYX_HISTORY_MODE=api
```

```bash
docker compose up -d --force-recreate aas_repository
```

For native deployments, set `history.mode: api` in `config.yaml` and restart the Repository. See [History, Timestamps, and Signed Reads](../common/history_and_changes.md#enable-history-recording) for the available modes. Enabling history does not backfill states created before it was active.

Save the initial state as `historical-aas.json`. It deliberately has no administrative timestamps: historical lookup uses the recorded mutation time instead.

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:history",
  "idShort": "HistoricalMotorV1",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:history",
    "assetType": "Motor"
  }
}
```

Create the AAS:

```bash
curl -i -X POST http://localhost:8084/shells -H 'Content-Type: application/json' --data-binary '@historical-aas.json'
```

Expect `201 Created`. Next, record a UTC timestamp after creation. The one-second delay ensures that the whole-second timestamp is later than the recorded creation time.

```bash
# Bash
sleep 1
RECORDED_UTC_TIME=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
```

```powershell
# Windows PowerShell
Start-Sleep -Seconds 1
$RECORDED_UTC_TIME = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd'T'HH:mm:ss'Z'")
```

Save the replacement as `historical-aas-updated.json`:

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:history",
  "idShort": "HistoricalMotorV2",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:history",
    "assetType": "UpdatedMotor"
  }
}
```

Replace the current AAS:

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOmhpc3Rvcnk -H 'Content-Type: application/json' --data-binary '@historical-aas-updated.json'
```

Expect `204 No Content`. Request the state that was valid at the recorded time:

```bash
curl -i -G 'http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOmhpc3Rvcnk/$history' \
  --data-urlencode "date=$RECORDED_UTC_TIME"
```

Expect `200 OK` and the earlier AAS state:

```json
{
  "idShort": "HistoricalMotorV1",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:history",
    "assetType": "Motor"
  },
  "id": "urn:example:aas:history",
  "modelType": "AssetAdministrationShell"
}
```

The current AAS remains `HistoricalMotorV2`. `$history` returns the complete AAS representation recorded for the requested time. At an exact update boundary the newer state is selected. A timestamp before the first recorded state or after a recorded deletion returns `404 Not Found`. A timestamp before deletion can still retrieve the earlier state.

## Asset Thumbnail

Place an existing PNG image named `thumbnail.png` in your working directory. Upload it using multipart form fields `fileName` and `file`:

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

Once you have finished, delete the example Submodel through the motor AAS, then delete all three AASs. The reference must still be present, so restore it first if you stopped partway through the reference-management section. The pump and historical AASs have no Submodels to clean up. Review [Resource Lifecycle](#resource-lifecycle) before adapting these destructive requests to shared Submodels.

The commands below intentionally use the second operation:

```bash
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjI
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOmhpc3Rvcnk
```

Expect `204 No Content` for each existing resource. Subsequent GET requests return `404`. Perform this cleanup after completing any Submodel Repository examples that share the same database and identifier.

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

The expected `404` confirms the AAS is no longer available. The example identifiers can now be used for a fresh walkthrough.

## Shared API Guidance

See [Validation](../common/validation) and [History, Timestamps, and Signed Reads](../common/history_and_changes). For available model views, see [Response Representations](../common/representations). Component-specific encoding examples, requests, errors, and lifecycle behavior are documented above and in the running Swagger UI.
