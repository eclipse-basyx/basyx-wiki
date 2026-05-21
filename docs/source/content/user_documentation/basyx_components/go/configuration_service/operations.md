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

Common failure categories include:

- Database connection failure.
- Missing or unreadable schema or patch files.
- SQL execution errors.
- Invalid or unreadable database version information.

## Idempotency Expectations

The base schema uses idempotent SQL where possible, such as `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`.

Patch files should also be safe to run in controlled deployment scenarios. The service checks the database version before running a patch, but the patch author is still responsible for writing safe SQL and updating the database version within the patch file.

## Versioning Concept

The database version is stored in the `basyxsystem` table. The Configuration Service creates this table if it is missing and assumes version `v1.0.0` for newly initialized or empty system tables.

Regular BaSyx services validate the database version during startup. If the database version does not match the expected service version, the service fails fast instead of running against an incompatible schema.

## Restart Behavior

The Configuration Service can be restarted. On restart:

- The system table step is idempotent.
- The base schema upload is skipped when core base schema tables are already present.
- Already applied patches are skipped when the database version is equal to or newer than the patch target version.

