# Using the AAS Registry

This walkthrough uses the unsecured [Docker Compose setup](setup) at `http://localhost:8082` with an empty context path. Run the examples in order against an example database. Save the JSON files as UTF-8 in your working directory. The curl commands are single-line commands usable in Bash; in Windows PowerShell, invoke `curl.exe` instead of `curl`.

The descriptor endpoints below use `example.com` as placeholders. Replace them with Repository URLs reachable by the clients that will use the descriptors.

## Register an AAS Descriptor

Save this as `aas-descriptor.json`:

```json
{
  "id": "urn:example:aas:1",
  "idShort": "MotorAAS",
  "assetKind": "Instance",
  "assetType": "Motor",
  "globalAssetId": "urn:example:asset:1",
  "specificAssetIds": [
    { "name": "serialNumber", "value": "SN-001" }
  ],
  "administration": {
    "createdAt": "2026-09-01T10:00:00Z",
    "updatedAt": "2026-09-01T10:00:00Z"
  },
  "endpoints": [
    {
      "interface": "AAS-3.2",
      "protocolInformation": {
        "href": "https://example.com/shells/dXJuOmV4YW1wbGU6YWFzOjE",
        "endpointProtocol": "https"
      }
    }
  ]
}
```

```bash
curl -i -X POST http://localhost:8082/shell-descriptors -H 'Content-Type: application/json' --data-binary '@aas-descriptor.json'
```

Expect `201 Created` and the registered descriptor. Posting the same visible identifier again returns `409 Conflict`. In this walkthrough you register the descriptor explicitly.  In a scenario where you use the [AAS Repository](../aas_repository/index) or the AAS Environment with the [Registry integration](../common/registry_integration) feature turned on, the AAS Descriptors can be created, updated, and deleted automatically.

## Retrieve and Update the Descriptor

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK` and the descriptor. To update it, change `idShort` in `aas-descriptor.json` to `MotorAASUpdated` and set `administration.updatedAt` to `2026-09-02T10:00:00Z`. Keep the original `id` and creation timestamp, then submit the complete descriptor:

```bash
curl -i -X PUT http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE -H 'Content-Type: application/json' --data-binary '@aas-descriptor.json'
```

Expect `204 No Content` for replacement. GET the descriptor again to check the update. PUT creates a missing descriptor with `201 Created`; the body `id` must equal the decoded path identifier in either case, otherwise the request returns `400 Bad Request`.

PUT is a replacement, not a partial update. Include all fields and nested `submodelDescriptors` that should remain. Omitting nested descriptors when replacing their parent removes those registrations. Use the nested routes below when changing only one Submodel Descriptor.

## Manage an AAS-scoped Submodel Descriptor

Save this as `submodel-descriptor.json`:

```json
{
  "id": "urn:example:submodel:1",
  "idShort": "MotorNameplate",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [
      { "type": "GlobalReference", "value": "urn:example:semantic:nameplate" }
    ]
  },
  "endpoints": [
    {
      "interface": "SUBMODEL-3.2",
      "protocolInformation": {
        "href": "https://example.com/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ",
        "endpointProtocol": "https"
      }
    }
  ]
}
```

The parent AAS Descriptor must already exist. Register and retrieve the child:

```bash
curl -i -X POST http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `201 Created` and then `200 OK`. Both path identifiers are encoded. To replace this child, edit its JSON file and use PUT on its individual URL. For an existing child this returns `204 No Content`:

```bash
curl -i -X PUT http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
```

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

Find the example descriptor by asset kind and type:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'assetKind=Instance' --data-urlencode 'assetType=TW90b3I' --data-urlencode 'limit=10'
```

To search by serial number, encode the complete JSON value `{"name":"serialNumber","value":"SN-001"}` using the [shared encoding commands](../common/encoding.md#encode-your-own-identifier), then replace `ENCODED_SPECIFIC_ASSET_ID`:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'assetIds=ENCODED_SPECIFIC_ASSET_ID'
```

For a global asset identifier, encode `{"name":"globalAssetId","value":"urn:example:asset:1"}` instead. Repeat `assetIds` for multiple identifiers; a descriptor matches if at least one supplied asset identifier matches. Other supplied filters further restrict the result.

Find the descriptor using the update timestamp set earlier:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'updatedFrom=2026-09-02T10:00:00Z' --data-urlencode 'limit=10'
```

`createdFrom` and `updatedFrom` compare the payload's `administration.createdAt` and `administration.updatedAt` using inclusive lower bounds. When both are supplied, either timestamp condition can match. The Registry does not generate or overwrite those fields. A descriptor with no matching timestamp will not appear in a timestamp-filtered result, even if it was just written.

Expect `200 OK` with matching AAS Descriptors in `result`. The single example descriptor normally fits on one page; for larger collections, follow the [next-cursor procedure](../common/pagination.md#follow-the-next-cursor) using the same filters.

## Structured Queries

Use `POST /query/shell-descriptors` for structured searches. Save this query as `query.json` to select the example descriptor by asset type:

```json
{
  "$condition": {
    "$eq": [
      { "$field": "$aasdesc#assetType" },
      { "$strVal": "Motor" }
    ]
  }
}
```

```bash
curl -i -X POST 'http://localhost:8082/query/shell-descriptors?limit=10' -H 'Content-Type: application/json' --data-binary '@query.json'
```

Expect `200 OK` with a paged descriptor result. String values in the query JSON are unencoded. For subsequent pages, follow [pagination for query requests](../common/pagination.md#keep-the-same-search). See the [query language examples](https://github.com/eclipse-basyx/basyx-go-components/blob/main/docu/query_language/examples.md) for combinations and nested descriptor filters, and the running Swagger UI for the installed version's contract.

## Bulk Operations

The bulk routes accept non-empty JSON arrays:

See [Asynchronous Requests](../common/asynchronous_requests) for the shared polling workflow, temporary handles, and retry considerations. The examples below use this Registry's endpoints.

| Method and path | Body |
| --- | --- |
| `POST /bulk/shell-descriptors` | Array of new AAS Descriptors. |
| `PUT /bulk/shell-descriptors` | Array of complete AAS Descriptors to create or replace. |
| `DELETE /bulk/shell-descriptors` | Array of original, unencoded AAS identifier strings. |

To try bulk creation without modifying the earlier example, save this as `bulk-descriptors.json`:

```json
[
  { "id": "urn:example:aas:bulk:1", "idShort": "BulkExampleOne" },
  { "id": "urn:example:aas:bulk:2", "idShort": "BulkExampleTwo" }
]
```

These minimal descriptors demonstrate job processing. Submit the job:

```bash
curl -i -X POST http://localhost:8082/bulk/shell-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-descriptors.json'
```

Expect `202 Accepted` and a `Location: /bulk/status/<handleId>` header. Acceptance does not mean the descriptors have been committed. Replace `HANDLE_ID` below with the returned handle:

```bash
curl -i http://localhost:8082/bulk/status/HANDLE_ID
```

While running, the response is `200 OK` with `executionState: Running` and `Retry-After: 2`. Wait for that interval before polling again. When processing has finished, status returns `302 Found` with `Location: /bulk/result/<handleId>`. Fetch that result explicitly:

```bash
curl -i http://localhost:8082/bulk/result/HANDLE_ID
```

Success returns `204 No Content`. A descriptor-operation failure returns `400` with failure details; execution failures can return another error status. Completion alone does not indicate success. Bulk descriptor mutations are atomic: if an operation fails, all descriptor changes in that job are rolled back.

Retrieving a completed result consumes the handle, including for failed jobs. Save the response if it is needed later; subsequent status/result requests return `404`. Fetching a result while the job is still running returns `400` and does not consume the running handle.

## Delete the Example Registrations

Delete the nested descriptor and then its parent:

```bash
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `204 No Content` for each existing registration. Subsequent GET requests return `404 Not Found`. Deleting a parent also removes its nested descriptor registrations, so deleting each child first is optional. Repository content is unaffected.

To remove the bulk examples, save `["urn:example:aas:bulk:1", "urn:example:aas:bulk:2"]` as `bulk-identifiers.json`, submit the request below, and follow the same status/result sequence:

```bash
curl -i -X DELETE http://localhost:8082/bulk/shell-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-identifiers.json'
```

## Shared API Guidance

See [Identifiers and Encoding](../common/encoding), [Validation](../common/validation), [API Errors](../common/api_errors), and [History, Timestamps, and Signed Reads](../common/history_and_changes). For bulk status polling and result handling, see [Asynchronous Requests](../common/asynchronous_requests). Component-specific requests and lifecycle behavior are documented above.
