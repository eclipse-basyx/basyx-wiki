# Operational Considerations

## Logging

The service logs each sequence before execution and logs completion status. Errors include BaSyx-style error codes such as `BASYXCFG-DB-CONNECT`, `BASYXCFG-SCHEMA-EXECUTE`, or `BASYXCFG-PATCH-EXECUTE`.

Example startup logs:

```text
[Step 1] Connecting to Database
[Step 1] Database connection established
[Step 2] Initializing system table
[Step 3] Uploading SQL schema
[Step 4] Applying schema patch v1.0.1 (/app/patches/101.sql)
BaSyx configuration completed successfully
```

## Failure Behavior

If a sequence fails, the service stops immediately and exits with a non-zero status code. Dependent containers should not start when Docker Compose uses `service_completed_successfully`.

If an error occurs during schema patch execution, the database is marked as `dirty` in `basyxsystem.state`. DB-backed BaSyx services check this state during startup and refuse to start while the database is dirty.

Common failure categories include:

- Database connection failure.
- Missing or unreadable schema or patch files.
- SQL execution errors.
- Invalid or unreadable schema version or state information.

### Dirty Schema State

`basyxsystem.state` can be `clean` or `dirty`. Successful schema initialization and patching leaves the database state as `clean`.

If a BaSyx service fails with `DB-CHECKVER-DIRTYSTATE`, the database schema was marked dirty because a previous schema patch did not complete successfully. Stop DB-backed BaSyx runtime services, run the matching `basyxconfigurationservice` version against the database, verify it exits successfully, and then restart the runtime services.

## Idempotency Expectations

The base schema uses idempotent SQL where possible, such as `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`.

Patch files should also be safe to run in controlled deployment scenarios. The service checks the database version before running a patch, but the patch author is still responsible for writing safe SQL and updating the database version within the patch file.

## Versioning Concept

The database schema version is stored in `basyxsystem.schema_version`. The schema state is stored in `basyxsystem.state`.

Regular BaSyx services validate both values during startup. If the schema version does not match the expected service version, or if the state is `dirty`, the service fails fast instead of running against an unsafe schema.

```{warning}
Use the same BaSyx version or build for `basyxconfigurationservice` and the DB-backed runtime services. A newer runtime service may require schema changes that an older Configuration Service image cannot apply.
```

## Restart Behavior

The Configuration Service can be restarted. On restart:

- The system table step is idempotent.
- The base schema upload is skipped when core base schema tables are already present.
- Already applied patches are skipped when the schema version is equal to or newer than the patch target version.
