# Conditional Requests

Use conditional requests to avoid overwriting another client's changes and to reuse cached responses. BaSyx identifies a resource's current version with an `ETag` response header. Clients send that tag with a later request to check whether the resource has changed.

Conditional headers are optional by default. Writes without them remain allowed unless `server.conditionalRequests.requireIfMatch` is enabled.

## Protect a Write

1. GET the resource and copy its complete `ETag` header value, including the quotation marks.
2. Send that value in `If-Match` when updating or deleting the resource.
3. If the resource has changed, BaSyx returns `412 Precondition Failed` without applying the write. Read the current content, reconcile your changes, and retry with the new tag.

For example, after creating the Submodel in the [usage walkthrough](../submodel_repository/usage), read its SerialNumber Property:

```bash
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value'
```

Replace `ETAG_FROM_GET` below with the complete quoted ETag from the response:

```bash
curl -i -X PATCH \
  'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value' \
  -H 'Content-Type: application/json' \
  -H 'If-Match: ETAG_FROM_GET' \
  --data '"SN-003"'
```

For example, the header argument becomes `-H 'If-Match: "8123-5c1e7a0d-91d2c3a4b5c6d7e8"'`. Use the returned tag unchanged. Read the resource again after an update to obtain a fresh tag.

`PUT`, `PATCH`, `DELETE`, and `POST` below an existing resource support this check. `If-Match: *` checks only that the addressed resource or part exists. It does not protect against another client's changes.

## Revalidate a Read

To check whether a cached response is still current, send its GET ETag in `If-None-Match` on another GET of the same representation:

```bash
curl -i \
  'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value' \
  -H 'If-None-Match: ETAG_FROM_GET'
```

Replace `ETAG_FROM_GET` with the cached response's complete quoted ETag. If it still matches, BaSyx returns `304 Not Modified` without a body; reuse the cached content. Otherwise, a successful read returns the current content and a new ETag. Keep cached content and tags specific to the representation and caller.

## Create Only If Absent

Add `If-None-Match: *` to a `PUT` request to create a resource or part only if it does not exist. If it already exists, BaSyx returns `412 Precondition Failed` without replacing it. Supply the request body required by that PUT endpoint.

## Require Protected Writes

To require `If-Match` on covered writes to existing resources, configure:

```yaml
server:
  conditionalRequests:
    requireIfMatch: true
```

The equivalent environment variable is `SERVER_CONDITIONALREQUESTS_REQUIREIFMATCH=true`. The default is `false`. When enabled, a missing `If-Match` header returns `428 Precondition Required`. Creation, including create-only PUT, requires no `If-Match`. The wildcard `If-Match: *` satisfies the header requirement but does not prevent concurrent overwrites.

## Resource Revisions

A resource and its parts can share one revision. A tag read from a part can therefore protect a write to the owning resource or another part:

| Resource | Revision also covers |
| --- | --- |
| AAS | Asset information, thumbnail, and Submodel references. AAS-scoped Submodel content uses the Submodel's revision. |
| Submodel | All contained elements, representations, element lists, and File attachments. |
| AAS Descriptor | Embedded Submodel Descriptors; Discovery asset-link changes also change the descriptor's revision. |
| Concept Description, standalone Submodel Descriptor, Discovery mapping, AASX package, Company Descriptor | The addressed resource. |
| DPP (`/v1/dpps/{dppId}` and its elements) | Its owning AAS and all referenced Submodels, including changes made through Repository APIs. |

The AAS Environment uses the same revisions as standalone services sharing its database. Changes to any covered part invalidate the earlier revision, including changes to content hidden from the caller.

## Availability and Limitations

- ETags are available on single-resource GET responses. Collections, queries, bulk operations, `/description`, `/serialization`, `/upload`, `$signed`, `$history`, `$recent-changes`, Operation status/results, and historical DPP reads provide no ETag.
- JSON responses larger than 16 MiB provide no ETag. Where available, read a smaller representation of the same resource, such as `$metadata`, to obtain a tag for a write.
- Use GET to obtain a tag; `HEAD` is not supported.
- For Operation invocation, the Submodel's tag is checked before calling the delegated service. This does not protect or roll back changes made by that external service.

CORS allows `If-Match` and `If-None-Match` and exposes `ETag` to browser clients automatically.
