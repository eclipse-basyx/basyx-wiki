# History, Timestamps, and Signed Reads

These features answer different questions: which current resources carry recent timestamps, what a resource looked like at an earlier time, and whether a returned payload or retained mutation artifact can be verified.

## Availability

| Component | Current changes | Historical reads | Signed reads |
| --- | --- | --- | --- |
| AAS Repository | `/shells/$recent-changes` | `/shells/{aasIdentifier}/$history` | `/shells/{aasIdentifier}/$signed` |
| Submodel Repository | `/submodels/$recent-changes` | `/submodels/{submodelIdentifier}/$history` | `/submodels/{submodelIdentifier}/$signed`; also `$value/$signed` |
| Concept Description Repository | `/concept-descriptions/$recent-changes` | Not included in this guide's supported history routes. | Not included in this guide's supported signing routes. |
| AAS Registry / Digital Twin Registry | `createdFrom` and `updatedFrom` on `/shell-descriptors` | No corresponding descriptor history route documented here. | No corresponding descriptor signing route documented here. |
| Submodel Registry | `createdFrom` and `updatedFrom` on `/submodel-descriptors` | No corresponding descriptor history route documented here. | No corresponding descriptor signing route documented here. |
| AAS Environment | Corresponding composed-service routes | AAS and Submodel history | AAS and Submodel signed reads |

Paths are relative to the service base URL, including any context path. Check the installed version's [Swagger contract](swagger).

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

Expect a paged result with identifiers and timestamps, plus resource-specific identifying fields. Follow [Pagination](pagination) for additional pages. Keep dollar-sign paths in single quotes and use `curl.exe` in PowerShell.

Resources without valid administrative timestamps are excluded. Deleted resources are absent. This is a view of current rows, not a complete mutation log or a deletion feed. Registry timestamp filters likewise use the timestamps persisted in descriptor payloads.

## Enable Historical Reads

Merge this into the Repository configuration before making changes, then restart:

```yaml
history:
  mode: api
  retentionDays: 0
  fullSnapshotInterval: 1
```

| Mode | Behavior |
| --- | --- |
| `off` (default) | Skip new PostgreSQL history writes; existing history remains readable. |
| `api` | Record supported mutations for historical reconstruction. |
| `audit` | The same runtime snapshot writes, intended for deployments that configure additional audit controls explicitly. |

Create an AAS using [AAS Repository Usage](../aas_repository/usage). Record a UTC time after its creation and before a later update. Replace `RECORDED_UTC_TIME` with that actual RFC 3339 timestamp:

```bash
curl -i -G 'http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/$history' --data-urlencode 'date=RECORDED_UTC_TIME'
```

The response reconstructs the version valid at that time. At an exact update boundary, the newer version is selected. A time before deletion can resolve the old version; a time after deletion returns not found. History is recorded from supported mutations while enabled; it is not inferred from client administrative timestamps.

Submodel Element changes belong to the owning Submodel's history. Adding or deleting an element produces an `Updated` Submodel snapshot, not an independent element history stream. An element-only change through an AAS-scoped route does not itself change the AAS history.

Historical reads are authorized at the route level. They do not apply current-resource ABAC filters or field redaction to stored snapshots. Grant access to `$history` only to callers permitted to read the complete retained snapshots; current-resource filtering does not restrict their contents. See the [implementation authorization notes](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/user/aas_api_v3_2.md#security).

History increases storage use. `fullSnapshotInterval: 1` stores complete snapshots; larger intervals allow checkpoints and diffs while reads still reconstruct complete resources. Automatic history cleanup is not implemented, so `retentionDays` must remain `0`. See [General Configuration](configuration.md#history) for supported settings.

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
