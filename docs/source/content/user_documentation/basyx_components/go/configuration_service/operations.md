# Operational Considerations

## Logging

The service logs each sequence before execution and logs completion status. Errors include BaSyx-style error codes such as `BASYXCFG-DB-CONNECT`, `BASYXCFG-SCHEMA-EXECUTE`, or `BASYXCFG-PATCH-EXECUTE`.

Representative log messages and fields include:

```text
msg="initialization step started" step=1 description="[Step 1] Connecting to Database"
msg="database connection established" step=1
msg="initialization step started" step=4 description="[Step 4] Applying schema patch v1.0.1 (/app/patches/1_0_1.sql)"
msg="schema patch applied" step=4 patch.version=v1.0.1
...
msg="BaSyx configuration completed successfully"
```

The exact rendering also includes fields added by the configured logging format.

## Failure Behavior

If a sequence fails, the service stops immediately and exits with a non-zero status code. Dependent containers should not start when Docker Compose uses `service_completed_successfully`.

Applying a required patch is transactional. The service executes the patch SQL and records the target schema version and `clean` state in the same transaction. If patch SQL execution or the metadata update fails, the service rolls back and then attempts to mark the database `dirty`. A commit failure also triggers that dirty-state attempt; because the commit outcome can be ambiguous after a connection failure, verify the actual database state before recovery. DB-backed BaSyx services check this state during startup and refuse to start while the database is dirty.

Failures before the patch transaction begins, such as an unreadable required patch file, do not enter this dirty-state handling. A failure while recording `dirty` is reported separately, so operators must inspect both the error and the actual database state.

Common failure categories include:

- Database connection failure.
- Missing or unreadable base-schema or registered-patch files when those files are required for the current database schema version.
- SQL execution errors.
- Invalid or unreadable schema-version metadata.

### Dirty Schema State

`basyxsystem.state` can be `clean` or `dirty`. Each successfully applied patch records `clean` together with its target schema version.

If a BaSyx service fails with `DB-CHECKVER-DIRTYSTATE`, stop DB-backed runtime services and investigate the failed migration and actual database state. Do not change the state to `clean` without verifying that the schema is complete and consistent.

Rerunning the Configuration Service does not always clear `dirty`. If the recorded schema version is already equal to or newer than every registered patch target, those patches are skipped and leave the state unchanged. In particular, investigate ambiguous connection or commit failures and restore a known-good backup when the database state cannot be established confidently.

## Idempotency Expectations

The base schema uses idempotent SQL where possible, such as `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`. Whether it runs is decided from `basyxsystem.schema_version`. The service does not first verify every base table. `base.sql` is skipped when the recorded version is `v1.0.2` or newer.

For every registered patch, the service compares the recorded schema version with the patch target and skips a target that has already been reached. When a patch is required, its SQL runs in a transaction; after it succeeds, the Configuration Service updates `basyxsystem.schema_version` to the registered target and sets the state to `clean` in that same transaction. The patch SQL is not responsible for advancing this metadata.

## Versioning Concept

The database schema version is stored in `basyxsystem.schema_version`. The schema state is stored in `basyxsystem.state`.

Regular BaSyx services validate both values during startup. If the schema version does not match the database schema version expected by that release, or if the state is `dirty`, the service fails fast instead of serving requests. The BaSyx application or image version and the database schema version are separate values. BaSyx Go expects database schema version `v1.2.2`.

```{warning}
Use the same BaSyx version or build for `basyxconfigurationservice` and the DB-backed runtime services. A newer runtime service may require schema changes that an older Configuration Service image cannot apply.
```

The Configuration Service applies registered upgrades only. It does not downgrade a newer database schema. An older Configuration Service can skip all of its patch targets and exit without making the database compatible with an older runtime, whose exact-version check will still fail. Use a matching BaSyx release or restore a compatible backup instead of manually changing schema metadata.

## Restart Behavior

The Configuration Service can be restarted. On restart:

- The system table step is idempotent.
- The base schema upload is skipped when the recorded schema version has reached the release's baseline threshold.
- Already applied patches are skipped when the schema version is equal to or newer than the patch target version.
