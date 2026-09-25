# Using the Submodel Registry

This walkthrough uses the unsecured [Docker Compose setup](setup) at `http://localhost:8083` with an empty context path. Run the examples in order against an example database. Save JSON files in your working directory. The curl commands work in Bash; in Windows PowerShell, invoke `curl.exe` instead of `curl`.

If you configure `server.contextPath`, prefix each API path with that value. The descriptor endpoints below use `example.com` as placeholders. Replace them with Submodel URLs reachable by the clients that will use the descriptors.

This walkthrough registers standalone descriptors by calling the Submodel Registry API directly. If the [Submodel Repository Registry integration](../submodel_repository/registry_integration) is enabled, Repository mutations can maintain the standalone descriptor and applicable embedded descriptors in existing AAS Descriptors automatically.

## Register a Submodel Descriptor

Save this as `submodel-descriptor.json`:

```json
{
  "id": "urn:example:submodel:1",
  "idShort": "MotorNameplate",
  "administration": {
    "createdAt": "2026-09-01T10:00:00Z",
    "updatedAt": "2026-09-01T10:00:00Z"
  },
  "semanticId": {
    "type": "ExternalReference",
    "keys": [
      { "type": "GlobalReference", "value": "urn:example:semantic:nameplate" }
    ]
  },
  "supplementalSemanticIds": [
    {
      "type": "ExternalReference",
      "keys": [
        { "type": "GlobalReference", "value": "urn:example:semantic:motor-nameplate" }
      ]
    }
  ],
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

```bash
curl -i -X POST http://localhost:8083/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
```

Expect `201 Created` and the registered descriptor. Posting another standalone descriptor with the same `id` returns `409 Conflict`. This request registers metadata. It does not create a Submodel in a Repository or start a service at the advertised endpoint.

## Retrieve and Update the Descriptor

Path identifiers use the unpadded Base64URL encoding of the identifier's UTF-8 bytes. The Submodel identifier in `submodel-descriptor.json` therefore becomes:

```text
urn:example:submodel:1 -> dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Identifiers in JSON bodies remain unencoded. Apply the same UTF-8 Base64URL rule, without padding, when substituting another path identifier.

```bash
curl -i http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `200 OK` and the descriptor. To update it, change `idShort` in `submodel-descriptor.json` to `MotorNameplateUpdated` and set `administration.updatedAt` to `2026-09-02T10:00:00Z`. Keep the original `id`, creation timestamp, and other fields, then submit the complete descriptor:

```bash
curl -i -X PUT http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@submodel-descriptor.json'
```

Expect `204 No Content` for replacement. GET the descriptor again to see the updated values. PUT creates a missing descriptor with `201 Created`. The body `id` must equal the decoded path identifier; a mismatch returns `400 Bad Request`.

PUT replaces the complete descriptor. Include the endpoints, semantic references, and other metadata that should remain. Replacing a descriptor does not update the actual Submodel in its Repository.

## Filtering and Pagination

See [Pagination](../common/pagination) for `limit`, cursor handling, and the shared response structure. The examples below show this component's requests and filters.

List descriptors:

```bash
curl -i http://localhost:8083/submodel-descriptors
```

The list endpoint supports these query parameters:

| Parameter | Use |
| --- | --- |
| `limit` | Requested maximum page size, a positive integer. |
| `cursor` | Cursor returned for the next page. |
| `createdFrom` | Inclusive lower bound for `administration.createdAt`, as an ISO 8601 date-time. |
| `updatedFrom` | Inclusive lower bound for `administration.updatedAt`, as an ISO 8601 date-time. |

Find the example using the update timestamp set earlier:

```bash
curl -i -G http://localhost:8083/submodel-descriptors --data-urlencode 'updatedFrom=2026-09-02T10:00:00Z'
```

Expect `200 OK` with matching Submodel Descriptors in `result`.

When both timestamp filters are supplied, a descriptor matches if either bound is satisfied:

```bash
curl -i -G http://localhost:8083/submodel-descriptors --data-urlencode 'createdFrom=2026-09-01T10:00:00Z' --data-urlencode 'updatedFrom=2026-09-02T10:00:00Z'
```

These filters use the administrative timestamps supplied in the descriptor payload. The Registry does not generate or overwrite them when a descriptor is created or replaced. A descriptor without a matching administrative timestamp is excluded from a timestamp-filtered result, even if it was just written.

### Follow a Pagination Cursor

Pagination needs more than one entry to produce a continuation cursor. Save a second descriptor as `submodel-descriptor-2.json`:

```json
{
  "id": "urn:example:submodel:2",
  "idShort": "PaginationExample",
  "endpoints": [
    {
      "interface": "SUBMODEL-3.2",
      "protocolInformation": {
        "href": "https://example.com/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6Mg",
        "endpointProtocol": "https"
      }
    }
  ]
}
```

Register it, then request only one descriptor in the first page:

```bash
curl -i -X POST http://localhost:8083/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@submodel-descriptor-2.json'
curl -i -G http://localhost:8083/submodel-descriptors --data-urlencode 'limit=1'
```

Expect `201 Created` for the registration and `200 OK` for the collection request. The first collection response contains one descriptor in `result` and a continuation value in `paging_metadata.cursor`. Copy that value without its surrounding JSON quotes into the next request:

```bash
curl -i -G http://localhost:8083/submodel-descriptors --data-urlencode 'limit=1' --data-urlencode 'cursor=RETURNED_CURSOR'
```

Replace `RETURNED_CURSOR` with the value returned by the first page. Treat the cursor as opaque: do not decode or modify it. Continue until `paging_metadata.cursor` is absent or empty. When filters are used, repeat the same filters on every page. See [Pagination](../common/pagination) for the shared response structure and cursor rules.

## Structured Queries

Use `POST /query/submodel-descriptors` to search fields that are not ordinary list-query parameters. For example, to find descriptors whose semantic reference contains the nameplate key value, save this as `query.json`:

```json
{
  "$condition": {
    "$eq": [
      { "$field": "$smdesc#semanticId.keys[].value" },
      { "$strVal": "urn:example:semantic:nameplate" }
    ]
  }
}
```

```bash
curl -i -X POST http://localhost:8083/query/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@query.json'
```

Expect `200 OK` with a paged descriptor result. This query matches a key value rather than asserting equality of an entire multi-key reference. Query string values inside JSON are unencoded. If the query result spans multiple pages, repeat the same request body and `limit` while supplying the returned cursor; see [Pagination](../common/pagination).

See the release-pinned [query language examples](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/docu/query_language/examples.md) for combinations, result-fragment filters, and supplemental semantic ID queries. Use the running Swagger UI for the installed version's operation contract.

## Bulk Operations

The bulk routes accept non-empty JSON arrays:

See [Asynchronous API Operations](../common/asynchronous_requests) for the shared polling workflow, temporary handles, and retry considerations. The examples below use this Registry's endpoints.

| Method and path | Body |
| --- | --- |
| `POST /bulk/submodel-descriptors` | Array of new Submodel Descriptors. |
| `PUT /bulk/submodel-descriptors` | Array of complete Submodel Descriptors to create or replace. |
| `DELETE /bulk/submodel-descriptors` | Array of original, unencoded Submodel identifier strings. |

Save this as `bulk-descriptors.json` to create two additional registrations:

```json
[
  {
    "id": "urn:example:submodel:bulk:1",
    "idShort": "BulkNameplateTwo",
    "endpoints": [
      {
        "interface": "SUBMODEL-3.2",
        "protocolInformation": {
          "href": "https://example.com/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6YnVsazox",
          "endpointProtocol": "https"
        }
      }
    ]
  },
  {
    "id": "urn:example:submodel:bulk:2",
    "idShort": "BulkNameplateThree",
    "endpoints": [
      {
        "interface": "SUBMODEL-3.2",
        "protocolInformation": {
          "href": "https://example.com/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6YnVsazoy",
          "endpointProtocol": "https"
        }
      }
    ]
  }
]
```

```bash
curl -i -X POST http://localhost:8083/bulk/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-descriptors.json'
```

Expect `202 Accepted` with a `Location: /bulk/status/<handleId>` header. Acceptance does not mean the changes have been committed. Replace `HANDLE_ID` below with the returned handle:

```bash
curl -i http://localhost:8083/bulk/status/HANDLE_ID
```

While running, status returns `200 OK`, an `executionState` of `Running`, and a `Retry-After` header. Wait for the number of seconds returned by the service before polling again. Once processing has finished, status returns `302 Found` with `Location: /bulk/result/<handleId>`. Fetch the result explicitly:

```bash
curl -i http://localhost:8083/bulk/result/HANDLE_ID
```

Success returns `204 No Content`. A descriptor-operation failure returns `400` with failure details; execution failures can return another error status. Completion does not itself mean success. Bulk descriptor mutations are atomic: if an operation fails, all descriptor changes in that job are rolled back.

Retrieving a completed result consumes its handle, including for failed jobs. Save the response if it is needed later; subsequent status/result requests return `404`. Fetching the result while a job is still running returns `400` without consuming the running handle. Avoid automatically following the status redirect, for example with `curl -L`, unless you intend to retrieve and consume the result.

Asynchronous execution capacity is bounded. A submission can return `429 Too Many Requests` when no execution slot is available. Retry the submission later rather than polling for a handle that was not created.

After the creation job succeeds, change the two `idShort` values in `bulk-descriptors.json` and submit the complete descriptors for replacement:

```bash
curl -i -X PUT http://localhost:8083/bulk/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-descriptors.json'
```

Use the new handle to repeat the status/result sequence. Bulk PUT also creates missing descriptors. Keep each descriptor's endpoints and other required metadata in the submitted array.

## Delete the Example Registrations

Delete the first descriptor and the second descriptor created for the pagination example:

```bash
curl -i -X DELETE http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i -X DELETE http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6Mg
```

Expect `204 No Content` for each existing descriptor. A subsequent GET returns `404 Not Found`. The Submodel content in the Repository is unaffected.

To remove the bulk examples, save this as `bulk-identifiers.json`:

```json
["urn:example:submodel:bulk:1", "urn:example:submodel:bulk:2"]
```

```bash
curl -i -X DELETE http://localhost:8083/bulk/submodel-descriptors -H 'Content-Type: application/json' --data-binary '@bulk-identifiers.json'
```

Follow the same status/result sequence with the new handle and expect `204 No Content` on successful result retrieval.

## Shared API Guidance

See [Validation](../common/validation), [Pagination](../common/pagination), and [Recent Changes, History, and Signed Reads](../common/history_and_changes). For bulk status polling and result handling, see [Asynchronous API Operations](../common/asynchronous_requests). Component-specific requests and lifecycle behavior are documented above.
