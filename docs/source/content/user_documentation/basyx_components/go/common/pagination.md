# Pagination

Many BaSyx Go collection endpoints return results in pages using `limit` and `cursor`. This page explains the shared request pattern for endpoints returning `result` and `paging_metadata`. The component's documentation and runtime Swagger UI define which operations support pagination, their filters, and their page-size defaults and restrictions.

## Limit and Cursor

| Parameter | Meaning |
| --- | --- |
| `limit` | Maximum number of entries requested in one page. It does not limit the total number of matches across all pages. |
| `cursor` | Server-provided continuation value for the next page. Omit it on the first request. |

A cursor is not a page number or offset. Treat it as an opaque string: do not construct, decode, increment, or Base64-encode it. Normal URL escaping still applies when placing it in a query string.

There is no single page-size default or maximum documented here for every component. Use a positive `limit` supported by the operation and consult its API contract for omitted-value behavior and restrictions.

## Read the First Page

Choose the component's collection endpoint and send a request without a cursor. For example, after creating the two AASs in the [AAS Repository walkthrough](../aas_repository/usage#filtering-and-pagination):

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'limit=1'
```

Use `curl.exe` in PowerShell. Adjust the base URL and context path for your service.

Successful collection responses contain:

- `result`: The entries on this page. Depending on the endpoint, these may be resources, descriptors, references, or identifiers.
- `paging_metadata`: Information about continuation. A non-empty `cursor` identifies the next page.

For illustration, a first-page response can look like this; only the AAS identifier is shown, and `CURSOR_FROM_SERVER` represents the actual cursor returned by the service:

```json
{
  "paging_metadata": {
    "cursor": "CURSOR_FROM_SERVER"
  },
  "result": [
    { "id": "urn:example:aas:1" }
  ]
}
```

## Follow the Next Cursor

Copy the returned cursor string into the next request, without its surrounding JSON quotes:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'limit=1' --data-urlencode 'cursor=RETURNED_CURSOR'
```

Replace `RETURNED_CURSOR` with the real value from the preceding response. `--data-urlencode` performs URL escaping without changing the logical cursor value.

Process that page's `result`, then use its next cursor. Stop when `paging_metadata.cursor` is absent or empty. Do not decide whether to continue solely from the number of entries: a full page can be the last page, and a short page is not a substitute for inspecting the cursor.

An empty collection response can look like this:

```json
{
  "paging_metadata": {},
  "result": []
}
```

This is a successful result with no matches, not a missing-resource error.

## Keep the Same Search

While following a cursor, retain the endpoint, filters, representation parameters, and caller identity used for the first request. Keep the page size unchanged for a predictable sequence. To change the search, start again without a cursor; do not reuse a cursor from another endpoint or filter combination.

For paginated POST query operations, submit the same query body on each page and pass the returned cursor through the operation's cursor parameter. A pagination cursor is separate from an asynchronous operation handle.

Pagination alone does not guarantee a snapshot across separate requests while other clients modify data. Consult the component's consistency guarantees when using paginated reads for synchronization.

## Component Examples

- [AAS Repository: two AASs, one per page](../aas_repository/usage#filtering-and-pagination)
- [Submodel Repository: list filters](../submodel_repository/usage#filtering-and-pagination)
- [AAS Registry: descriptor filters](../aas_registry/usage#filtering-and-pagination)
- [Submodel Registry: descriptor filters](../submodel_registry/usage#filtering-and-pagination)
- [Company Lookup: page-size default and company filters](../company_lookup/index#listing-and-pagination)
