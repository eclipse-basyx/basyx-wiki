# History, Timestamps, and Signed Reads

These features answer different questions: which current resources carry recent timestamps, what a resource looked like at an earlier time, and whether a returned payload or retained mutation artifact can be verified.

## Availability

| Component | Current changes | Historical reads | Signed reads |
| --- | --- | --- | --- |
| AAS Repository | `/shells/$recent-changes` | `/shells/{aasIdentifier}/$history` | `/shells/{aasIdentifier}/$signed` |
| Submodel Repository | `/submodels/$recent-changes` | `/submodels/{submodelIdentifier}/$history` | `/submodels/{submodelIdentifier}/$signed`; also `$value/$signed` |
| Concept Description Repository | `/concept-descriptions/$recent-changes` | None | None |
| AAS Registry / Digital Twin Registry | `createdFrom` and `updatedFrom` on `/shell-descriptors` | None | None |
| Submodel Registry | `createdFrom` and `updatedFrom` on `/submodel-descriptors` | None | None |
| AAS Environment | `/shells/$recent-changes`; `/submodels/$recent-changes`; `/concept-descriptions/$recent-changes`; descriptor collections use `createdFrom` and `updatedFrom` | `/shells/{aasIdentifier}/$history`; `/submodels/{submodelIdentifier}/$history` | Corresponding AAS and Submodel signed reads |

Paths are relative to the service base URL, including any context path. Check the installed version's [Swagger contract](swagger).

Only the AAS and Submodel routes shown above are public `$history` APIs in the stable release. Concept Description and descriptor mutations can still be recorded internally when history is active, but that does not create a public history-read route for those resource types.

## Current Changes and Client Timestamps

Recent-change endpoints read current resources with valid `administration.createdAt` and `administration.updatedAt` timestamps. BaSyx does not generate or overwrite those fields. Your producer must supply and maintain them, for example:

```json
{
  "createdAt": "2026-09-01T10:00:00Z",
  "updatedAt": "2026-09-02T10:00:00Z"
}
```

Include these fields in the resource's `administration` object. After creating or updating timestamped AAS resources:

```bash
curl -i -G 'http://localhost:8084/shells/$recent-changes' --data-urlencode 'updatedFrom=2026-09-02T00:00:00Z'
```

Expect a paged result with identifiers and timestamps, plus resource-specific identifying fields. Follow [Pagination](pagination) for additional pages.

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

### What History Records

History is associated with the identifiable resource that owns the changed content:

- AAS create, update, delete, asset-information, thumbnail, and Submodel-reference mutations update the AAS history.
- Submodel create, update, and delete mutations update the Submodel history.
- Submodel Element and File attachment mutations update the history of their owning Submodel; they do not create independent element or attachment timelines.
- Concept Description mutations update Concept Description history.
- AAS Descriptor mutations, including changes to embedded Submodel Descriptors, update the owning AAS Descriptor history.
- Standalone Submodel Descriptor mutations update Submodel Descriptor history.

Recording a resource type internally does not imply that the component exposes a public `$history` route for it. The stable public IDTA history-read API is limited to AAS and Submodels as shown in [Availability](#availability).

### Audit Context and Separate Integrity Controls

`history.mode: audit` does not automatically enable `history.immutability: postgres_guarded` or WORM mutation evidence. Both `api` and `audit` use the same PostgreSQL history mechanism. Audit identity capture is selected separately with `history.auditIdentityMode` and is stored when a history or evidence record is written:

| Audit identity mode | Recorded request context |
| --- | --- |
| `none` (default) | No request or caller identity metadata. |
| `minimal` | Request and correlation identifiers, method and route, available OIDC subject/issuer/client identity, and the authorization result. |
| `extended` | The minimal fields plus available source IP, user agent, policy identifier or hash, and matched rule identifiers. |

These modes record available context; they do not turn anonymous requests into authenticated identities and do not store bearer tokens.

Create an AAS using [AAS Repository Usage](../aas_repository/usage). Record a UTC time after its creation and before a later update. Replace `RECORDED_UTC_TIME` with that actual RFC 3339 timestamp:

```bash
curl -i -G 'http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/$history' --data-urlencode 'date=RECORDED_UTC_TIME'
```

The response reconstructs the version valid at that time. At an exact update boundary, the newer version is selected. A time before deletion can resolve the old version; a time after deletion returns not found. History is recorded from supported mutations while enabled; it is not inferred from client administrative timestamps.

Submodel Element changes belong to the owning Submodel's history. Adding or deleting an element produces an `Updated` Submodel snapshot, not an independent element history stream. An element-only change through an AAS-scoped route does not itself change the AAS history.

Historical reads are authorized at the route level. They do not apply current-resource ABAC filters or field redaction to stored snapshots. Grant access to `$history` only to callers permitted to read the complete retained snapshots; current-resource filtering does not restrict their contents. See the [implementation authorization notes](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/user/aas_api_v3_2.md#security).

History increases storage use. `fullSnapshotInterval: 1` stores complete snapshots; larger intervals allow checkpoints and diffs while reads still reconstruct complete resources. Automatic history cleanup is not implemented, so `retentionDays` must remain `0`. See [General Configuration](configuration.md#history) for supported settings.

### Integrity Checks During Historical Reads

PostgreSQL history entries are hash-chained per identifiable resource. When reconstructing a historical AAS or Submodel, BaSyx verifies the stored snapshot or diff payload hash, the reconstructed content hash, each loaded row hash, and the links between the loaded rows. If a required payload is missing or an integrity check fails, the `$history` request fails instead of returning an unverified reconstruction.

These checks detect inconsistent or altered stored history, but the hashes and their chain are held in the same PostgreSQL trust boundary. They do not by themselves prevent a sufficiently privileged database operator from rewriting the data and its integrity metadata. Use the database guard and independent mutation evidence according to the threat model described below.

## Database-wide History Guard

`history.immutability: postgres_guarded` is a database compatibility decision,
not a process-local switch. A service establishes the guard only when history
is active (`api` or `audit`) and immutability is `postgres_guarded`. Setting
that immutability value while `history.mode` is `off` does not enable it.

The enabled state is stored in PostgreSQL and affects every participating
process that uses the same BaSyx database. It is intentionally sticky: a later
startup configured with `history.mode: off` or `history.immutability: none`
does not downgrade an enabled database guard. Instead, the incompatible
process can fail at startup. This remains true after restarting or replacing a
container because the state belongs to the database.

`postgres_guarded` blocks normal application-level and database-user updates,
deletes, and truncation of the history data, but it is not an absolute WORM
boundary. A PostgreSQL superuser or another sufficiently privileged operator
can alter or remove the trigger and function mechanisms that enforce the
guard. Use independent WORM mutation evidence when protection from
database-level modification is required.

When diagnosing a guard conflict, inspect both sides:

- the process's effective `history.mode` and `history.immutability`, including
  environment-variable overrides; and
- the guard state already persisted in the target PostgreSQL database, along
  with which other services share that database.

Align all processes with the intended guarded mode and take a verified backup
before maintenance or upgrade work. Do not delete guard rows, disable database
triggers, or reset the database as routine recovery; those actions can defeat
the immutability guarantee or destroy retained history. See the
[configuration caveat](configuration.md#history), [version scope](deployment.md#version-scope),
and [upgrading an existing database](../configuration_service/operations.md#upgrading-an-existing-database).

Implementation reference: [database history guard](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/common/history/guard.go).

## Mutation Evidence

External evidence is independent of PostgreSQL history. With `history.evidence.enabled: true`, it can record mutation artifacts in S3-compatible WORM storage even when `history.mode: off`. Required evidence writes are synchronous: if evidence cannot be stored, the mutation fails.

Enabling evidence requires a configured backend, bucket, and retention settings; setting the enable flag alone is insufficient. Evidence may contain snapshots or diffs and is intended for verification and recovery workflows. It does not enable the PostgreSQL historical-read API by itself. Preserve the receipt catalog as part of backup and recovery.

Independent verification uses the evidence sequence and hash chain. To detect removal of the same tail from both PostgreSQL catalog records and object listings, retain the last verified sequence and event hash outside the BaSyx database and supply that expected head to later verification runs. The first externally retained value is a trust-on-first-use baseline.

Use the [evidence configuration reference](configuration.md#historyevidence) and the upstream [history and evidence guide](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/user/aas_api_v3_2.md) for backend setup, verification, and recovery commands.

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

Missing signing configuration produces an error rather than an unsigned fallback. Use a JWS verification library with a trusted public key or validated certificate chain to verify the signature before using the payload. Decoding the JWS alone does not verify it. A signed read attests the returned payload; mutation evidence records changes over time and is configured separately.

Source: [AAS API v3.2 user guide](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/user/aas_api_v3_2.md).
