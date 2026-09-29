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

The URL uses the Base64URL encoding of the Concept Description identifier, without padding:

| Original identifier | Path value |
| --- | --- |
| `urn:example:cd:motor-speed` | `dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ` |

```bash
curl -i http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
```

Expect `200 OK` and the stored object. Keep the identifier in JSON unencoded; encode only the path value. For another identifier, encode its UTF-8 bytes with Base64URL without padding.

## List and Filter Concept Descriptions

```bash
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'limit=10'
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'idShort=MotorSpeed'
```

The collection response contains a `result` array and `paging_metadata`. If `paging_metadata.cursor` is present, pass it unchanged as the `cursor` parameter of the next request. See [Pagination](../common/pagination).

The `idShort` filter is plain text. The optional `isCaseOf` and `dataSpecificationRef` filters are Base64URL-encoded reference values. Consult the running Swagger UI for their schemas instead of guessing an encoding.

`createdFrom` and `updatedFrom` are inclusive RFC 3339 lower-bound filters for the Concept Description's `administration.createdAt` and `administration.updatedAt` values. They are not repository POST or PUT timestamps, and the Repository does not generate or advance these fields when it writes a resource. If both filters are provided, a Concept Description matches when either `createdAt >= createdFrom` or `updatedAt >= updatedFrom`. A missing or invalid timestamp does not satisfy its comparison.

### Structured Queries

Use `POST /query/concept-descriptions` when the predefined collection filters are not sufficient. The endpoint accepts the shared BaSyx query language and returns matching Concept Descriptions with `limit` and cursor-based pagination.

See the release-matched [Query Language examples](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/docu/query_language/examples.md) and the running Swagger UI for supported conditions, fragment filters, and request structure.

### Recent Changes

Use `GET /concept-descriptions/$recent-changes` to list current Concept Description identifiers together with their administration timestamps:

```bash
curl -i -G 'http://localhost:8086/concept-descriptions/$recent-changes' --data-urlencode 'limit=10'
```

The response contains a `result` array whose entries have `id`, `createdAt`, and `updatedAt`, plus `paging_metadata` for cursor-based pagination. The endpoint supports `createdFrom`, `updatedFrom`, `limit`, and `cursor`; the timestamp filters have the same inclusive and OR behavior described above.

This endpoint reads the `administration.createdAt` and `administration.updatedAt` values stored in each current Concept Description. It is not a repository mutation log and does not report deleted resources or the time at which BaSyx received a POST or PUT. Concept Descriptions without both valid administration timestamps are omitted, including the minimal example created above. Continue following a returned cursor even when omitted entries make a page shorter than its requested limit.

## Replace the Concept Description

Change `idShort` in `concept-description.json` to `MotorSpeedUpdated`, leaving `id` unchanged, then send the complete replacement:

```bash
curl -i -X PUT http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ -H 'Content-Type: application/json' --data-binary '@concept-description.json'
```

Expect `204 No Content` for an existing resource. PUT creates a missing resource with `201 Created`. The body `id` must equal the decoded path identifier, and fields omitted from a replacement are not retained.

## Delete the Example

```{note}
Deleting a Concept Description does not remove or update references to its identifier in AAS or Submodel content.
```

```bash
curl -i -X DELETE http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
curl -i http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
```

The DELETE returns `204 No Content`; the following GET returns `404 Not Found`.
