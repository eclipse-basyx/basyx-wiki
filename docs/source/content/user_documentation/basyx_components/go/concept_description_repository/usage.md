# Using the Concept Description Repository

This walkthrough creates, reads, lists, replaces, and deletes a Concept Description and introduces the Repository's filters, structured queries, and recent-changes API.

## Before You Start

Start the [Compose setup](setup), then check the service:

```bash
curl -i http://localhost:8086/health
```

Continue after HTTP `200`. The examples use an empty context path and the unsecured local setup. In Windows PowerShell, use `curl.exe` instead of the `curl` alias.

## Create a Concept Description

Save this minimal payload as `concept-description.json`:

```json
{
  "modelType": "ConceptDescription",
  "id": "urn:example:cd:motor-speed",
  "idShort": "MotorSpeed"
}
```

Create it:

```bash
curl -i -X POST http://localhost:8086/concept-descriptions -H 'Content-Type: application/json' --data-binary '@concept-description.json'
```

Expect `201 Created`. Repeating POST with the same identifier returns `409 Conflict`.

## Retrieve It by Identifier

Path identifiers use the Base64URL encoding of the identifier's UTF-8 bytes. BaSyx Go accepts valid padded and unpadded Base64URL values. The examples below use the unpadded form. Identifiers in JSON request bodies remain unencoded:

| Original identifier | Path value |
| --- | --- |
| `urn:example:cd:motor-speed` | `dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ` |

```bash
curl -i http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
```

Expect `200 OK` and the stored object. For another identifier, Base64URL-encode its UTF-8 bytes using either a valid padded or unpadded form.

## List and Filter Concept Descriptions

```bash
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'limit=10'
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'idShort=MotorSpeed'
```

The collection response contains a `result` array and `paging_metadata`. If `paging_metadata.cursor` is present, pass it unchanged as the `cursor` parameter of the next request. See [Pagination](../common/pagination).

The `idShort` filter is plain text. The optional `isCaseOf` and `dataSpecificationRef` filters are Base64URL-encoded reference values. Valid padded and unpadded forms are accepted. Consult the running Swagger UI for their schemas instead of guessing an encoding.

`createdFrom` and `updatedFrom` are inclusive RFC 3339 lower-bound filters for the Concept Description's `administration.createdAt` and `administration.updatedAt` values. They are not repository POST or PUT timestamps, and the Repository does not generate or advance these fields when it writes a resource. If both filters are provided, a Concept Description matches when either `createdAt >= createdFrom` or `updatedAt >= updatedFrom`. A missing or invalid timestamp does not satisfy its comparison.

### Structured Queries

Use `POST /query/concept-descriptions` when the predefined collection filters are not sufficient. The endpoint accepts the shared BaSyx query language and returns matching Concept Descriptions with `limit` and cursor-based pagination.

See the shared [Query Language](../common/query_language) for conditions, operators, `$cd` fields, and fragment filters. Use the running Swagger UI for the operation contract.

### Recent Changes

Use `GET /concept-descriptions/$recent-changes` to list current Concept Description identifiers together with their administration timestamps:

```bash
curl -i -G 'http://localhost:8086/concept-descriptions/$recent-changes' --data-urlencode 'limit=10'
```

The response contains a `result` array whose entries have `id`, `createdAt`, and `updatedAt`, plus `paging_metadata` for cursor-based pagination. The endpoint supports `createdFrom`, `updatedFrom`, `limit`, and `cursor`; the timestamp filters have the same inclusive and OR behavior described above.

This endpoint reads the `administration.createdAt` and `administration.updatedAt` values stored in each current Concept Description. It is not a repository mutation log and does not report deleted resources or the time at which BaSyx received a POST or PUT. Concept Descriptions without both valid administration timestamps are omitted, including the minimal example created above. Omitted entries can make a page shorter than its requested `limit`. If the response contains a cursor, continue with that cursor even when the page contains fewer results than requested.

## Replace the Concept Description

Change `idShort` in `concept-description.json` to `MotorSpeedUpdated`, leaving `id` unchanged, then send the complete replacement:

```bash
curl -i -X PUT http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ -H 'Content-Type: application/json' --data-binary '@concept-description.json'
```

Expect `204 No Content` for an existing resource. PUT creates a missing resource with `201 Created`. The body `id` must equal the decoded path identifier, and fields omitted from a replacement are not retained.

When authorization relies on ReBAC, creating a Concept Description that is missing when authorization is checked requires repository `creator` or `admin` access; one that already exists requires update permission.

## Delete the Example

```{note}
Deleting a Concept Description does not remove or update references to its identifier in AAS or Submodel content.
```

```bash
curl -i -X DELETE http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
curl -i http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
```

The DELETE returns `204 No Content`; the following GET returns `404 Not Found`.
