# Using the AAS Registry

This walkthrough uses the unsecured [Docker Compose setup](setup) at `http://localhost:8082` with an empty context path. Run the examples in order against an example database. Save the JSON files in your working directory. The curl commands are single-line commands usable in Bash. In Windows PowerShell, invoke `curl.exe` instead of `curl`.

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

Path identifiers use the unpadded Base64URL encoding of the identifier's UTF-8 bytes. The AAS identifier in `aas-descriptor.json` therefore becomes:

```text
urn:example:aas:1 -> dXJuOmV4YW1wbGU6YWFzOjE
```

Identifiers in JSON bodies remain unencoded. Apply the same UTF-8 Base64URL rule, without padding, when substituting another path identifier.

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK` and the descriptor. To update it, change `idShort` in `aas-descriptor.json` to `MotorAASUpdated` and set `administration.updatedAt` to `2026-09-02T10:00:00Z`. Keep the original `id` and creation timestamp, then submit the complete descriptor:

```bash
curl -i -X PUT http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE -H 'Content-Type: application/json' --data-binary '@aas-descriptor.json'
```

Expect `204 No Content` for replacement. GET the descriptor again to check the update. PUT creates a missing descriptor with `201 Created`. The body `id` must equal the decoded path identifier in either case, otherwise the request returns `400 Bad Request`.

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

The parent AAS Descriptor must already exist. Register the child, then list the Submodel Descriptors associated with the parent AAS:

```bash
curl -i -X POST http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors
```

Expect `201 Created` and then `200 OK`. The collection response contains the registered descriptor in `result` and pagination information in `paging_metadata`.

To replace this child, change its `idShort` in `submodel-descriptor.json` to `MotorNameplateUpdated`, keep the original `id`, and use PUT on its individual URL. The encoded Submodel identifier `dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ` represents `urn:example:submodel:1`. Replacing the existing child returns `204 No Content`:

```bash
curl -i -X PUT http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors
```

The second collection request shows the updated child. Submodel Descriptors are scoped to the parent AAS Descriptor, so an individual child route includes both the encoded AAS identifier and the encoded Submodel identifier.

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

Find the example descriptor by asset kind and type:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'assetKind=Instance' --data-urlencode 'assetType=TW90b3I'
```

`TW90b3I` is the unpadded Base64URL encoding of the descriptor's plain `assetType` value, `Motor`.

The `assetIds` filter expects a Base64URL-encoded `SpecificAssetId` JSON object. For the descriptor registered above, encode the compact UTF-8 JSON `{"name":"serialNumber","value":"SN-001"}`. The resulting unpadded value is `eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDEifQ`:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'assetIds=eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDEifQ'
```

Compact JSON makes the encoded value reproducible. The service parses the decoded JSON rather than comparing its whitespace. For a global asset identifier, encode `{"name":"globalAssetId","value":"urn:example:asset:1"}` instead. Repeat `assetIds` for multiple identifiers. A descriptor matches if at least one supplied asset identifier matches. Other supplied filters further restrict the result.

Find the descriptor using the update timestamp set earlier:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'updatedFrom=2026-09-02T10:00:00Z'
```

`createdFrom` and `updatedFrom` compare the payload's `administration.createdAt` and `administration.updatedAt` using inclusive lower bounds. When both are supplied, either timestamp condition can match. The Registry does not generate or overwrite those fields. A descriptor with no matching timestamp will not appear in a timestamp-filtered result, even if it was just written.

Expect `200 OK` with matching AAS Descriptors in `result`.

### Follow a Pagination Cursor

Pagination needs more than one matching entry to demonstrate a continuation cursor. Save a second, minimal descriptor as `aas-descriptor-2.json`:

```json
{
  "id": "urn:example:aas:2",
  "idShort": "PaginationExample"
}
```

Register it, then request only one descriptor in the first page:

```bash
curl -i -X POST http://localhost:8082/shell-descriptors -H 'Content-Type: application/json' --data-binary '@aas-descriptor-2.json'
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'limit=1'
```

Expect `201 Created` for the registration and `200 OK` for the collection request. The first collection response contains one descriptor in `result` and a continuation value in `paging_metadata.cursor`. Copy that value without the surrounding JSON quotes into the next request:

```bash
curl -i -G http://localhost:8082/shell-descriptors --data-urlencode 'limit=1' --data-urlencode 'cursor=RETURNED_CURSOR'
```

Replace `RETURNED_CURSOR` with the value returned by the first page. The cursor is opaque. Do not decode or modify it. Continue until `paging_metadata.cursor` is absent or empty. When filters are used, repeat the same filters on every page. See [Pagination](../common/pagination) for the shared response structure and cursor rules.

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
curl -i -X POST http://localhost:8082/query/shell-descriptors -H 'Content-Type: application/json' --data-binary '@query.json'
```

Expect `200 OK` with a paged descriptor result. String values in the query JSON are unencoded. For subsequent pages, repeat the same query body and page size while supplying the returned cursor; see [Pagination](../common/pagination). See the release-pinned [query language examples](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/query_language/examples.md) for combinations and nested descriptor filters, and the running Swagger UI for the installed version's contract.

## Bulk Operations

The bulk routes accept non-empty JSON arrays:

See [Asynchronous API Operations](../common/asynchronous_requests) for the shared polling workflow, temporary handles, and retry considerations. The examples below use this Registry's endpoints.

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

While running, the response is `200 OK` with `executionState: Running` and a `Retry-After` header. Wait for the number of seconds returned by the service before polling again. When processing has finished, status returns `302 Found` with `Location: /bulk/result/<handleId>`. Fetch that result explicitly:

```bash
curl -i http://localhost:8082/bulk/result/HANDLE_ID
```

Success returns `204 No Content`. A descriptor-operation failure returns `400` with failure details. Execution failures can return another error status. Completion alone does not indicate success. Bulk descriptor mutations are atomic: if an operation fails, all descriptor changes in that job are rolled back.

Retrieving a completed result consumes the handle, including for failed jobs. Save the response if it is needed later; subsequent status/result requests return `404`. Fetching a result while the job is still running returns `400` and does not consume the running handle. Do not automatically follow the status redirect unless you intend to consume the result.

Asynchronous execution capacity is bounded. A submission can return `429 Too Many Requests` when no execution slot is available. If that is the case, retry the submission later.

## Delete the Example Registrations

Delete the nested descriptor, its parent, and the second descriptor created for the pagination example:

```bash
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjI
```

Expect `204 No Content` for each existing registration. The final path identifier represents `urn:example:aas:2`. Subsequent GET requests return `404 Not Found`. Deleting a parent also removes its nested descriptor registrations, so deleting each child first is optional. Repository content is unaffected.

To remove the bulk examples, save `["urn:example:aas:bulk:1", "urn:example:aas:bulk:2"]` as `bulk-identifiers.json`, submit the request below, and follow the same status/result sequence:

```bash
curl -i -X DELETE http://localhost:8082/bulk/shell-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-identifiers.json'
```

## Shared API Guidance

See [Validation](../common/validation) and [History, Timestamps, and Signed Reads](../common/history_and_changes). For bulk status polling and result handling, see [Asynchronous API Operations](../common/asynchronous_requests). Component-specific requests and lifecycle behavior are documented above.
