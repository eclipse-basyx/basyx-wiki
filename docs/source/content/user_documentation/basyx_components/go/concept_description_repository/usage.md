# Using the Concept Description Repository

This walkthrough creates, reads, lists, replaces, and deletes one Concept Description through the standalone Repository.

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

Expect `200 OK` and the stored object. Keep the identifier in JSON unencoded; encode only the path value. See [Identifiers and Encoding](../common/encoding) for commands that encode another identifier.

## List and Filter Concept Descriptions

```bash
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'limit=10'
curl -i -G http://localhost:8086/concept-descriptions --data-urlencode 'idShort=MotorSpeed'
```

The collection response contains a `result` array and `paging_metadata`. If `paging_metadata.cursor` is present, pass it unchanged as the `cursor` parameter of the next request. See [Pagination](../common/pagination).

The `idShort` filter is plain text. The optional `isCaseOf` and `dataSpecificationRef` filters are Base64URL-encoded reference values. The collection also supports the RFC 3339 lower-bound filters `createdFrom` and `updatedFrom`. Consult the running Swagger UI for their schemas instead of guessing an encoding.

## Replace the Concept Description

Change `idShort` in `concept-description.json` to `MotorSpeedUpdated`, leaving `id` unchanged, then send the complete replacement:

```bash
curl -i -X PUT http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ -H 'Content-Type: application/json' --data-binary '@concept-description.json'
```

Expect `204 No Content` for an existing resource. PUT creates a missing resource with `201 Created`. The body `id` must equal the decoded path identifier, and fields omitted from a replacement are not retained.

## Delete the Example

```bash
curl -i -X DELETE http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
curl -i http://localhost:8086/concept-descriptions/dXJuOmV4YW1wbGU6Y2Q6bW90b3Itc3BlZWQ
```

The DELETE returns `204 No Content`; the following GET returns `404 Not Found`.

## Further Operations

The service also exposes structured queries at `POST /query/concept-descriptions`, recent changes at `GET /concept-descriptions/$recent-changes`, and serialization at `GET /serialization`. Use the running [Swagger UI](http://localhost:8086/swagger) for the request and response schemas supported by the installed release. For secured deployments, add a valid bearer token and ensure its subject has permission for the requested operation.
