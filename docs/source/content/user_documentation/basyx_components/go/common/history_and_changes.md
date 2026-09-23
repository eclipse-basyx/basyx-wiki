# History, Timestamps, and Signed Reads

The features on this page serve different purposes. Recent-change APIs find current resources by their stored timestamps, history reconstructs earlier recorded states, and signed reads and mutation evidence support verification of returned or retained data.

## Availability

| Component | Current changes | Historical reads | Signed reads |
| --- | --- | --- | --- |
| AAS Repository | `/shells/$recent-changes` | `/shells/{aasIdentifier}/$history` | `/shells/{aasIdentifier}/$signed` |
| Submodel Repository | `/submodels/$recent-changes` | `/submodels/{submodelIdentifier}/$history` | `/submodels/{submodelIdentifier}/$signed`; also `$value/$signed` |
| Concept Description Repository | `/concept-descriptions/$recent-changes` | None | None |
| AAS Registry / Digital Twin Registry | `createdFrom` and `updatedFrom` on `/shell-descriptors` | None | None |
| Submodel Registry | `createdFrom` and `updatedFrom` on `/submodel-descriptors` | None | None |
| AAS Environment | `/shells/$recent-changes`; `/submodels/$recent-changes`; `/concept-descriptions/$recent-changes`; descriptor collections use `createdFrom` and `updatedFrom` | `/shells/{aasIdentifier}/$history`; `/submodels/{submodelIdentifier}/$history` | Corresponding AAS and Submodel signed reads |

Paths are relative to the service base URL, including any configured context path. See the component API documentation for the endpoints available in your installed BaSyx version.

## Current Changes and Client Timestamps

Recent-change endpoints read current resources with valid `administration.createdAt` and `administration.updatedAt` timestamps. BaSyx does not generate or update these fields automatically. The client that creates or updates the resource must supply and maintain them, for example:

```json
{
  "createdAt": "2026-09-01T10:00:00Z",
  "updatedAt": "2026-09-02T10:00:00Z"
}
```

Include these fields in the resource's `administration` object. After creating or updating timestamped AAS resources:

```bash
curl -i -G 'http://localhost:8084/shells/$recent-changes' \
  --data-urlencode 'updatedFrom=2026-09-02T00:00:00Z'
```

The response is paged and contains the matching resource identifiers together with their creation and update timestamps. See [AAS Repository Usage](../aas_repository/usage.md#find-recently-changed-aass) for a complete request and response example, and [Pagination](pagination) for handling additional pages.

Resources without valid administrative timestamps are excluded. Deleted resources are absent. This is a view of current rows, not a complete mutation log or a deletion feed.

Repositories and registries expose recent changes differently. The AAS, Submodel, and Concept Description Repository APIs provide dedicated `/$recent-changes` operations. Registry APIs do not define a `/$recent-changes` route. Instead, filter the normal descriptor collection with `createdFrom` and/or `updatedFrom`, for example `GET /shell-descriptors?updatedFrom=...` or `GET /submodel-descriptors?updatedFrom=...`. This distinction follows the IDTA V3.2 API design and is not a missing BaSyx endpoint. Registry timestamp filters use the timestamps persisted in descriptor payloads.

## Enable History Recording

History recording is disabled by default. To record new AAS and Submodel versions for historical reads, configure:

```yaml
history:
  mode: api
```

Restart the service after changing the configuration. Enable history before performing changes that you want to retain historically.

| Mode | Behavior |
| --- | --- |
| `off` (default) | Do not record new PostgreSQL history. Existing history remains readable. |
| `api` | Record supported mutations so earlier resource states can be reconstructed through `$history`. |
| `audit` | Record the same historical states as `api`, intended for audit-oriented deployments. Audit identity, database guarding, and external mutation evidence are configured separately. |

History is not backfilled when it is enabled. Existing resources do not automatically receive historical versions, so states from before activation cannot be retrieved through `$history`.

For an existing resource without history, the first supported mutation creates its first recorded state or deletion marker. It does not preserve the resource's earlier state from before history recording was enabled.

History increases storage use. Automatic history cleanup is not implemented, so `history.retentionDays` must remain `0`. See [General Configuration](configuration.md#history) for the storage settings.

### What History Records

History is recorded for the identifiable resource that owns the changed content:

- AAS changes are recorded in the AAS history.
- Submodel, Submodel Element, and File attachment changes are recorded in the owning Submodel's history.
- Concept Description changes are recorded in Concept Description history.
- AAS Descriptor changes, including embedded Submodel Descriptor changes, are recorded in the owning AAS Descriptor history.
- Standalone Submodel Descriptor changes are recorded in Submodel Descriptor history.

Submodel Elements and attachments do not have independent history timelines.

Recording history internally does not imply that a public `$history` endpoint exists for that resource type. In the current stable release, public `$history` reads are available for AAS and Submodels, as shown in [Availability](#availability).

### Read a Historical State

Use `$history` with the `date` query parameter to retrieve the AAS or Submodel state that was valid at a specific time. For example, create an AAS using [AAS Repository Usage](../aas_repository/usage), then record a UTC time after its creation and before a later update. Replace `RECORDED_UTC_TIME` with that actual RFC 3339 timestamp:

```bash
curl -i -G 'http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/$history' \
  --data-urlencode 'date=RECORDED_UTC_TIME'
```

The response reconstructs the version valid at that time. The requested time follows the recorded mutation timeline, not `administration.createdAt` or `administration.updatedAt`. At an exact update boundary, the newer version is selected. A time before a recorded deletion can resolve the earlier version; a time after the deletion returns not found.

Historical reads are authorized at the route level. They do not apply current-resource ABAC filters or field redaction to stored snapshots. Grant access to `$history` only to callers permitted to read the complete retained snapshots; current-resource filtering does not restrict their contents.

### Audit Context

`history.mode: audit` records the same historical resource states as `api`. Additional request and caller context can be recorded with `history.auditIdentityMode`, which supports `none`, `minimal`, and `extended`.

Audit identity capture, PostgreSQL guarding, and external mutation evidence are separate controls; selecting `audit` does not enable them automatically. See [General Configuration](configuration.md#history) for the audit identity settings.

### Integrity Checks During Historical Reads

BaSyx verifies the integrity of stored PostgreSQL history while reconstructing a historical state. If the required history is incomplete or its integrity checks fail, the `$history` request fails instead of returning an unverified result.

These checks detect inconsistent or modified history, but the history and its integrity metadata share the same PostgreSQL trust boundary. Use `postgres_guarded` or independent mutation evidence when stronger protection is required.

## Database-wide History Guard

`history.immutability: postgres_guarded` protects PostgreSQL history against normal modification and deletion. The guard is established only while history recording is active (`api` or `audit`); selecting it while `history.mode` is `off` does not establish the guard.

The guard belongs to the PostgreSQL database, not to an individual BaSyx process, and remains enabled once established. Services that share the database must therefore use compatible history-guard settings; an unguarded service can fail to start against an already guarded database.

`postgres_guarded` is not an absolute WORM boundary. A sufficiently privileged PostgreSQL administrator can alter or remove the database mechanisms that enforce it. Use independent mutation evidence when the database administrator must not be the sole trust boundary.

See the [configuration caveat](configuration.md#history) and [upgrading an existing database](../configuration_service/operations.md#upgrading-an-existing-database) for operational guidance.

## Mutation Evidence

Mutation evidence is independent of PostgreSQL history. When `history.evidence.enabled: true`, BaSyx records mutation evidence in supported S3-compatible WORM storage. Evidence can be enabled even when `history.mode: off`.

Required evidence writes are synchronous: if the configured evidence cannot be stored, the mutation fails. Evidence requires an S3-compatible provider, bucket, and Object Lock retention settings.

Mutation evidence does not enable the `$history` API. PostgreSQL history and external evidence can be used independently or together.

See the [evidence configuration reference](configuration.md#historyevidence) and the stable [history and evidence guide](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/docu/user/aas_api_v3_2.md) for storage setup, verification, backup, and recovery procedures.

## Signed Reads

A signed read returns a compact JWS for the requested AAS or Submodel. Configure a mounted RSA private key using `jws.privateKeyPath`; `jws.certificateChainPath` can supply the certificate chain. Restart the service after configuring its signing material.

```yaml
jws:
  privateKeyPath: /keys/signing-private.pem
  certificateChainPath: /keys/signing-chain.pem
```

After creating the example AAS:

```bash
curl --fail-with-body -sS 'http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/$signed' -o aas.jws
```

Missing signing configuration produces an error rather than an unsigned fallback. Use a JWS verification library with a trusted public key or validated certificate chain to verify the signature before using the payload. Decoding the JWS alone does not verify it.

A signed read signs the payload returned by the current read request. It does not create history or sign the sequence of historical mutations; mutation evidence is a separate feature.
