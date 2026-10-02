# Using the Digital Product Passport API

This walkthrough creates one passport, reads both representations, looks it up by product identifier, updates one element and the passport, retrieves an earlier recorded state, performs a bulk lookup, and deletes the passport.

Start the [Compose setup](setup) and wait for `http://localhost:8088/health` to return HTTP `200`. The example identifiers must not already exist in the database. The examples use Bourne-shell syntax. In Windows PowerShell, use `curl.exe` and supply the recorded timestamp explicitly.

JSON request bodies for DPP creation, whole-DPP `PATCH`, element `PATCH`, and bulk product-ID lookup are limited to 10 MiB. A larger body returns `413 Request Entity Too Large`.

## Create a Passport

Save the following compressed DPP document as `dpp.json`:

```json
{
  "digitalProductPassportId": "https://example.org/dpp/1",
  "uniqueProductIdentifier": "https://example.org/product/1",
  "granularity": "Item",
  "dppSchemaVersion": "1.0.0",
  "dppStatus": "active",
  "lastUpdate": "2026-01-02T03:04:05Z",
  "economicOperatorId": "operator-1",
  "contentSpecificationIds": [
    "urn:example:technical-data"
  ],
  "urn:example:technical-data": {
    "manufacturerName": "Acme GmbH",
    "energyClass": "A"
  }
}
```

Create the passport:

```bash
curl -i -X POST http://localhost:8088/v1/dpps -H 'Content-Type: application/json' --data-binary '@dpp.json'
```

Expect `201 Created` and:

```json
{
  "digitalProductPassportId": "https://example.org/dpp/1"
}
```

Creation is atomic. A duplicate DPP identifier returns `409 Conflict`. The request must use the compressed representation. `POST /v1/dpps?representation=full` returns `501 Not Implemented`.

The required `granularity` values are `Item`, `Model`, and `Batch`. `lastUpdate` must be an RFC 3339 timestamp. `facilityId` and `contentSpecificationIds` are optional. Each submitted content section must be a JSON object and is persisted as a content Submodel. `contentSpecificationIds` selects which matching content Submodels are included in the composed DPP representation. If the list is omitted or empty, DPP reads contain only the header metadata even though submitted content sections are still persisted as Submodels.

Name each compressed top-level content section after the corresponding entry in `contentSpecificationIds`. This keeps the relationship unambiguous when a passport uses several content specifications.

## Encode Path Identifiers

DPP and product identifiers are placed directly in URL path parameters after percent-encoding their UTF-8 form exactly once. The examples use:

| Identifier | Encoded path value |
| --- | --- |
| `https://example.org/dpp/1` | `https%3A%2F%2Fexample.org%2Fdpp%2F1` |
| `https://example.org/product/1` | `https%3A%2F%2Fexample.org%2Fproduct%2F1` |

Do not Base64URL-encode these DPP API identifiers. A literal percent escape that is part of an identifier must itself be percent-encoded.

## Read Compressed and Full Representations

Read the default compressed representation:

```bash
curl -i 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1'
```

The response has the same general shape as the create body: DPP header fields and named content sections with compressed JSON values.

Request the expanded full representation:

```bash
curl -i 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1?representation=full'
```

The full response keeps the header fields and returns content in an `elements` array with DPP element types and metadata. It is read-only in v1.1.0. If stored AAS content cannot be converted to a supported full DPP element, a full passport read returns `422 Unprocessable Entity`. The compressed representation may still be readable.

Read by unique product identifier:

```bash
curl -i 'http://localhost:8088/v1/dppsByProductId/https%3A%2F%2Fexample.org%2Fproduct%2F1'
```

This returns `404 Not Found` when no passport has that product identifier and `409 Conflict` when more than one does. Product identifiers are therefore lookup keys, not unique DPP identifiers.

### Compressed Value Mapping

BaSyx maps compressed JSON content to AAS Submodel Elements as follows:

| JSON value | Persisted AAS element |
| --- | --- |
| String, Boolean, or number | `Property` |
| Object containing string `url` and `contentType` values | `File`; compressed reads return the resource object, while full reads represent it as `RelatedResource` |
| Other object | `SubmodelElementCollection` |
| Non-empty array of compatible values | `SubmodelElementList` |
| Array of `{ "language": "...", "value": "..." }` objects | `MultiLanguageProperty` |

Empty arrays are rejected because their element type cannot be inferred. Arrays containing incompatible element types are also rejected. In v1.1.0, a JSON `null` content value is stored as an empty-string `Property` and does not round-trip as JSON `null`, although the OpenAPI schema permits null compressed values. In a whole-DPP JSON Merge Patch, `null` instead retains its deletion meaning described below.

## Read and Replace One Element

An element path is an RFC 9535 Normalized Path selecting exactly one node. It must start with `$`, use single-quoted member selectors or non-negative array indices, and select a content section and an element below it. Wildcards and other selectors that can match several nodes are rejected.

For this passport, the path is:

```text
$['urn:example:technical-data']['manufacturerName']
```

Percent-encode the complete path exactly once as one URL segment:

```bash
curl -i 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1/elements/%24%5B%27urn%3Aexample%3Atechnical-data%27%5D%5B%27manufacturerName%27%5D'
```

The compressed response is the raw element value:

```json
"Acme GmbH"
```

Add `?representation=full` to return the selected element as an expanded object with its DPP element type and metadata.

Replace it by sending another raw compressed JSON value, not a DPP element wrapper:

```bash
curl -i -X PATCH 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1/elements/%24%5B%27urn%3Aexample%3Atechnical-data%27%5D%5B%27manufacturerName%27%5D' -H 'Content-Type: application/json' --data '"Acme Updated GmbH"'
```

The replacement and automatic update of the DPP `lastUpdate` field occur in one transaction. The replacement must be compatible with the stored element type. Element writes with `representation=full` return `501 Not Implemented`.

## Partially Update the Passport

Record a time after the element update and before the next change:

```bash
sleep 1; HISTORY_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ); sleep 1
```

Apply an RFC 7396 JSON Merge Patch:

```bash
curl -i -X PATCH 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1' -H 'Content-Type: application/merge-patch+json' --data '{"dppStatus":"archived"}'
```

Omitted properties remain unchanged. Setting an optional property such as `facilityId` or `contentSpecificationIds` to `null` removes it. Required header fields cannot be removed. The path DPP identifier remains authoritative, and the service generates a new `lastUpdate` value. `uniqueProductIdentifier` can be changed. Subsequent product lookup uses the replacement value.

Arrays use JSON Merge Patch replacement semantics. Setting `contentSpecificationIds` changes which retained content Submodels are included in the DPP. It does not delete excluded Submodels. Setting a content-section property to `null` likewise detaches that section from the passport without deleting its Submodel.

## Read a Historical Passport

Retrieve the state recorded at the saved time:

```bash
curl -i -G 'http://localhost:8088/v1/dppsByIdAndDate/https%3A%2F%2Fexample.org%2Fdpp%2F1' --data-urlencode "date=${HISTORY_DATE}" --data-urlencode 'representation=compressed'
```

The response shows the state before the status patch. The service selects the newest recorded DPP state valid at or before the requested RFC 3339 timestamp. At an exact change boundary, the newer state is selected. A timestamp before creation or at or after a recorded deletion returns `404 Not Found`.

Historical DPP reads compose the owning AAS and every referenced Submodel at the same point in time. They require history to have been enabled before the relevant mutations. History is not backfilled when enabled later. See [Recent Changes, History, and Signed Reads](../common/history_and_changes) for shared history behavior and security considerations.

## Bulk Lookup by Product Identifiers

Find DPP identifiers matching any supplied product identifier:

```bash
curl -i -X POST 'http://localhost:8088/v1/dppsByProductIds?limit=10' -H 'Content-Type: application/json' --data '{"productIds":["https://example.org/product/1","https://example.org/product/unknown"]}'
```

Expect a paged response such as:

```json
{
  "items": [
    "https://example.org/dpp/1"
  ]
}
```

The request accepts between 1 and 100 non-empty product identifiers. Unknown values are omitted, duplicate DPP identifiers are removed, and results are sorted by DPP identifier. The default `limit` is 100. v1.1.0 requires a positive value but does not impose a separate maximum. If the response contains a `cursor`, repeat the same request body and `limit` with that cursor to retrieve the next page. See [Pagination](../common/pagination) for opaque-cursor guidance.

## Delete the Passport

Delete the current passport:

```bash
curl -i -X DELETE 'http://localhost:8088/v1/dpps/https%3A%2F%2Fexample.org%2Fdpp%2F1'
```

Expect `204 No Content`. Current reads by DPP or product identifier now return `404 Not Found`.

Deletion removes the owning AAS and DPP metadata Submodel. Content Submodels and their attachments remain stored. When Registry synchronization is enabled, the corresponding DPP-owned AAS and metadata descriptors are also removed; retained content Submodels are not. If history recorded the earlier states, a historical request for a time before deletion remains available.
