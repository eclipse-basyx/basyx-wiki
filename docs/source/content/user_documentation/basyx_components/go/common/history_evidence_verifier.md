# History Evidence Verifier

`historyevidenceverifier` is an operator CLI for checking BaSyx history and evidence artifacts. It can verify PostgreSQL history ranges, separately retained mutation-evidence artifacts, and the ReBAC administration audit trail. For history-range evidence, it can also export a recovery catalog and reconstruct verified history rows as JSON.

The verifier does not restore PostgreSQL. A successful run confirms only the selected evidence and trust inputs. It does not prove that the business data is correct, that evidence outside the selected range exists, that backups can be restored, or that a deployment meets a legal or regulatory requirement.

## Build and Configure the CLI

BaSyx Go v1.1.0 includes the command source but no dedicated `historyevidenceverifier` container image or release binary. Build it from the matching source tag:

Building BaSyx Go v1.1.0 requires Go 1.27.1 or a compatible newer Go toolchain.

```bash
git checkout v1.1.0
go build -o historyevidenceverifier ./cmd/historyevidenceverifier
```

The examples below use `./historyevidenceverifier`. From a v1.1.0 source checkout, `go run ./cmd/historyevidenceverifier` is equivalent.

Use `-config` to supply a normal BaSyx YAML configuration. Depending on the selected operation or verification target, the CLI reads:

- the PostgreSQL writer connection;
- `history.evidence` S3 endpoint, bucket, prefix, credentials, and Object Lock settings;
- `history.evidence.signing.publicKeyPath` for signed-manifest verification;
- `history.evidence.signing.privateKeyPath` when `-write` signs a manifest,
  falling back to `jws.privateKeyPath` when the history-specific path is empty.

The CLI validates the BaSyx database schema before database-backed operations. Recovery from an exported catalog is the exception: it does not connect to PostgreSQL, but still needs the configured S3 evidence store. See [General Configuration](configuration) for the configuration keys and [History and Changes](history_and_changes) for the history modes.

## Evidence and Trust Boundaries

The CLI supports three distinct checks:

| Check | What is checked | Independent input |
| --- | --- | --- |
| History range | PostgreSQL row hashes and chains, `history_event` receipts, optional stored objects, and an optional range manifest | A separately retained manifest object hash, and optionally a trusted manifest public key |
| Mutation evidence | PostgreSQL mutation-evidence metadata, the per-resource `mutation_event` sequence and hash chain, immutable objects, reconstructed content, live retention, and referenced binary evidence | The expected terminal event hash for the requested sequence |
| ReBAC audit | The ReBAC administration audit chain currently present and, when S3 is configured, archived audit objects | An optional expected audit head hash |

Mutation evidence artifacts are retained separately from the ordinary PostgreSQL history tables. In v1.1.0, however, normal mutation verification still uses PostgreSQL mutation-evidence metadata to locate and verify the corresponding immutable objects. It cannot run after PostgreSQL has been lost.

PostgreSQL supplies object locations and receipts for normal history and mutation verification, so it is not an independent trust source by itself. Keep expected terminal hashes and manifest hashes outside the database under verification. A value read only from that database immediately before a check cannot detect an attacker who removed both a chain tail and its catalog rows.

## Operations and Verification Targets

`-write`, `-recover`, and `-catalog-export` select mutually exclusive operations. With none of them, the CLI verifies evidence. `-mutation` and `-rebac-audit` select a different verification target rather than another operation in that group.

| Selection | Required input | Result |
| --- | --- | --- |
| Default history verification | `-table`, `-from`, `-to`; `-identifier` is optional | Verifies a PostgreSQL `history_id` range and its `history_event` receipts. |
| `-write` | Same history range | Verifies the PostgreSQL range, then publishes event, checkpoint, and manifest artifacts and records their receipts. |
| `-catalog-export` | Same history range | Exports recovery metadata from PostgreSQL. |
| `-recover` | Same history range, or `-recovery-catalog` | Verifies and reconstructs `history_event` artifacts as JSON. |
| `-mutation` target | `-table`, `-identifier`, `-from`, `-to`, `-expected-head-hash` | Verifies and reconstructs one mutation-evidence chain. |
| `-rebac-audit` target | No history table or range | Verifies the ReBAC administration audit chain currently present. An expected head is optional. |

The supported history table/entity names are:

- `aas_history`
- `submodel_history`
- `concept_description_history`
- `descriptor_history` for AAS Descriptors
- `submodel_descriptor_history`

For ordinary history operations, `-from` and `-to` are inclusive `history_id` bounds. An optional `-identifier` restricts the selected rows to one resource. In mutation mode, `-table` identifies the entity type using the same names, while `-from` and `-to` are inclusive per-resource evidence sequence numbers.

`-out <file>` writes the formatted JSON result to that file instead of standard output. On platforms that support Unix-style permissions, newly created files use mode `0600`. An existing file keeps its current permissions. Operational logs and errors go to standard error.

## Verify History-Range Evidence

The default mode verifies each selected PostgreSQL history chain from the nearest required snapshot through the end of the selected range. It calculates the range digest and checks that every selected row has a matching `history_event` receipt with retention metadata. When an S3 evidence store is configured, it also verifies the referenced object version and hash and checks the current Object Lock retention and legal-hold state against the receipt.

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -table aas_history \
  -from 100 \
  -to 150
```

This mode is for ranges that already have `history_event` receipts, for example evidence previously published with `-write`. It does not use an expected terminal hash and cannot by itself prove that rows after the selected range were not removed.

### Verify a Stored Manifest

Supply the immutable manifest object key and an expected SHA-256 value together. `-manifest-version-id` selects a specific S3 object version. Without it, the configured store resolves the object by key.

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -table submodel_history \
  -identifier 'https://example.com/submodels/1' \
  -from 1 \
  -to 25 \
  -manifest-object-key '<object-key-from-receipt>' \
  -manifest-version-id '<immutable-version-id>' \
  -manifest-sha256 '<independently-retained-sha256>' \
  -require-signed-manifest
```

The manifest is checked against the requested table, identifier, range, row count, boundary hashes, and range digest. A signed manifest is an RS256 compact JWS over the manifest payload. Signed artifacts require the PEM-encoded RSA public key configured through `history.evidence.signing.publicKeyPath`. `-require-signed-manifest`, or `history.evidence.signing.required: true`, rejects a missing or unsigned manifest. An invalid signature also fails verification.

The public key must itself be distributed through a trusted process. A valid signature does not establish that an untrusted replacement key is legitimate.

`-signer-key-id` is not a verification constraint. It records the optional key identifier when `-write` creates a signed manifest.

### Publish History-Range Evidence

`-write` requires `history.evidence.enabled: true` and the S3 evidence provider. It first verifies the selected PostgreSQL history data, then writes per-row `history_event` objects, snapshot checkpoints, and a manifest and records the returned receipts in PostgreSQL:

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -table submodel_history \
  -identifier 'https://example.com/submodels/1' \
  -from 1 \
  -to 25 \
  -write
```

The output includes the manifest, receipts, catalog identifier, and the PostgreSQL preflight verification report. The command does not perform a second independent verification of the newly written artifacts. It also cannot retroactively create the separate `mutation_event` chain used by `-mutation`.

Publication spans PostgreSQL and object storage rather than one cross-system transaction. A failure after an object write can leave an unreferenced immutable object. Investigate failed runs before retrying or deleting any recoverable metadata.

## Verify Mutation Evidence

Mutation-evidence artifacts are stored separately from ordinary PostgreSQL history when `history.evidence.enabled` was active for the mutation. Verification nevertheless requires the PostgreSQL mutation-evidence metadata, S3 evidence configuration, an identifier, a valid sequence range, and the independently retained SHA-256 event hash for the requested terminal sequence.

### Establish an External Mutation Head

The expected sequence and event hash form the input trust anchor for mutation verification. BaSyx Go v1.1.0 has no dedicated CLI operation for exporting or advancing that anchor. The current sequence and head are maintained in PostgreSQL mutation-evidence state. While the system is known to be trustworthy, obtain a known-good pair through controlled operational access and protect it outside the BaSyx database and evidence infrastructure being checked. This establishes an initial trust-on-first-use baseline. Reading a later value from the same database does not independently authenticate that later head.

For verification, use the retained sequence as `-to` and its hash as `-expected-head-hash`. For example, a retained pair for sequence 42 verifies a range ending at sequence 42. That hash cannot be used with `-to 50`; a run ending at sequence 50 requires an independently authenticated hash for sequence 50 as input. The verifier confirms that the evidence chain ends in the supplied hash. It does not authenticate a newer head. To move the trust anchor to a later sequence, obtain or authenticate that later sequence/hash pair through a trusted process outside the database being verified, then verify it in the same way:

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -mutation \
  -table submodel_history \
  -identifier 'https://example.com/submodels/1' \
  -from 1 \
  -to 42 \
  -expected-head-hash '<64-character-sha256-for-sequence-42>'
```

The verifier locates the nearest snapshot checkpoint at or before `-from`, verifies the sequence and predecessor hashes through `-to`, reconstructs snapshots and diffs, and compares the terminal event hash with `-expected-head-hash`. A missing requested terminal event or a different terminal hash is an error, so the externally retained sequence/hash pair detects removal or alteration that prevents the chain from reaching that trusted terminal state

For each event, the CLI checks the immutable object hash, event and payload hashes, reconstructed content hash, receipt retention metadata, and the current Object Lock retention and legal-hold state. When a mutation declares internal attachment or thumbnail evidence, it also checks the binary-reference object, its binding to the mutation, the referenced immutable binary receipt and bytes, digest and size, and live retention.

The JSON report includes the reconstructed terminal `snapshot`, `event_hash`, change and deletion state, operation time, audit context, and any findings. `-mutation -recover` is accepted in v1.1.0, but follows this same verification path and produces the same report. It is not a separate restore or export operation. `-mutation` cannot be combined with `-write`, `-catalog-export`, or `-recovery-catalog`.

## Recover History-Range Evidence

Ordinary `-recover` reconstructs verified history rows from stored `history_event` objects and emits a JSON report containing `recovered_rows`. It never writes to PostgreSQL. Importing those rows or restoring an application database remains part of the operator's disaster-recovery procedure.

Recovery starts at the nearest cataloged full snapshot required by the selected range and replays subsequent diff artifacts. Consequently, recoverability depends on the checkpoint and every required diff still being available. With `history.fullSnapshotInterval: 1`, each row is a full snapshot. Larger values trade smaller evidence for bounded diff replay.

### Export a Recovery Catalog

Before PostgreSQL is unavailable, export the selected rows and their receipt metadata:

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -table submodel_history \
  -identifier 'https://example.com/submodels/1' \
  -from 1 \
  -to 25 \
  -catalog-export \
  -out ./submodel-history-catalog.json
```

The catalog contains the requested range, the expected PostgreSQL row and content hashes, and the object locations, immutable version identifiers, digests, and receipt metadata needed for recovery. It can include an earlier checkpoint and intervening diffs required to reconstruct the requested rows.

The catalog is not recovered history data and is not an independently signed completeness proof. Protect and back it up separately: omitting or altering its expected-row metadata can change what a later catalog-only operation attempts to recover.

### Recover with an Exported Catalog

An exported catalog avoids live PostgreSQL receipt discovery:

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -recover \
  -recovery-catalog ./submodel-history-catalog.json \
  -out ./submodel-history-recovered.json
```

This path does not connect to PostgreSQL. It still requires the configured S3 store and credentials, fetches the cataloged object versions, verifies their hashes and embedded row metadata, replays snapshots and diffs, and exports the selected reconstructed rows. Optional `-table`, `-identifier`, `-from`, and `-to` selectors must match the catalog exactly when supplied.

Without `-recovery-catalog`, `-recover` obtains the catalog from live PostgreSQL and therefore requires the ordinary table and range flags.

## Verify the ReBAC Audit Trail

`-rebac-audit` verifies the hash chain of the ReBAC administration audit events currently present. It is separate from AAS, Submodel, and descriptor history:

```bash
./historyevidenceverifier \
  -config ./config.yaml \
  -rebac-audit \
  -expected-head-hash '<independently-retained-64-character-sha256>'
```

The expected head is optional, but an independently retained expected head is required to detect removal of a locally consistent tail. The report contains `headHash` and `lastId`. Retain that pair independently after a successful check.

When an S3 evidence store is configured, the command verifies archived audit objects referenced by the events. An event without archived evidence increments `evidenceMissing` but does not invalidate an otherwise valid audit chain. Inspect `evidenceVerified` and `evidenceMissing` as well as `valid` when archived evidence is required by your operating policy.

This target cannot be combined with `-write`, `-recover`, `-catalog-export`, `-mutation`, or `-table`. Do not pass `-identifier`, `-from`, `-to`, or manifest/signing selectors with `-rebac-audit`. v1.1.0 does not use them for ReBAC audit verification. See [Relationship-Based Access Control](rebac) for the ReBAC audit-trail model.

## Results, Exit Status, and Scheduling

Results are formatted JSON. History, mutation, and recovery reports use `valid` and an optional `findings` array. Findings emitted by v1.1.0 have `severity: "error"`. Any finding makes the report invalid. ReBAC reports use `valid` and `reason`, together with the verified head and evidence counts.

| Exit code | Meaning |
| --- | --- |
| `0` | The operation completed successfully; a verification/recovery report is valid. Help also exits with `0`. |
| `1` | Option validation, configuration, connectivity, operation, recovery, or integrity verification failed. An invalid report is written before this exit where one is available. |
| `2` | Command-line flag parsing failed, for example because a flag is unknown or malformed. |

`SIGINT` and `SIGTERM` cancel in-progress database or object-store work and result in a failed operation. Do not treat interrupted output or a failed `-write` as a completed verification cycle.

Run the verifier from cron, a Kubernetes CronJob, or another operator scheduler at a frequency appropriate to the deployment's evidence-retention and recovery objectives. Alert on non-zero exit status and on invalid JSON reports. Keep expected heads outside the system being verified and use only independently authenticated sequence/hash pairs as new mutation trust anchors.

## Limits and Security Considerations

- Evidence and recovery cover only mutations for which the required history/evidence artifacts were created. Enabling evidence later does not create a mutation chain for earlier changes.
- Recovery is bounded by available receipt/catalog metadata and retained checkpoint, diff, binary-reference, and binary objects. Object Lock expiry permits later deletion. It does not delete an object by itself.
- Ordinary catalog recovery checks object bytes and reconstruction but does not restore a database or prove that the catalog contains every event that ever existed.
- The CLI does not verify the separate WORM artifact created for an activated ABAC policy version. Its evidence modes cover history-range, mutation, and ReBAC audit evidence only. See [ABAC Policy Management](abac_policy_management) for that policy lifecycle.
- Protect PostgreSQL and object-store credentials, the manifest verification key, independently retained hashes, exported catalogs, and recovered JSON. Recovered history and audit context can contain sensitive data.
- Use least-privilege read credentials for verification and recovery where the deployment permits them. `-write` additionally needs object-write and PostgreSQL catalog-write access.

BaSyx evidence features can support integrity, traceability, and recovery controls. Their use does not by itself establish regulatory compliance or replace backups and tested disaster-recovery procedures.

## See Also

- [Recent Changes, History, and Signed Reads](history_and_changes)
- [General Configuration](configuration)
- [ABAC Policy Management](abac_policy_management)
- [Relationship-Based Access Control](rebac)
