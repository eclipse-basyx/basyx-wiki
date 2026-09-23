# Operational Considerations

## Logging

The service logs each sequence before execution and logs completion status. Errors include BaSyx-style error codes such as `BASYXCFG-DB-CONNECT`, `BASYXCFG-SCHEMA-EXECUTE`, or `BASYXCFG-PATCH-EXECUTE`.

Illustrative shortened startup logs (the exact steps and fields depend on the release and database state):

```text
[Step 1] Connecting to Database
[Step 1] Database connection established
[Step 2] Initializing system table
[Step 3] Uploading SQL schema
[Step 4] Applying schema patch v1.0.1 (/app/patches/1_0_1.sql)
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

If a BaSyx service fails with `DB-CHECKVER-DIRTYSTATE`, the database schema was marked dirty because a previous schema patch did not complete successfully. Keep DB-backed runtime services stopped, preserve the logs, determine which patch and SQL statements ran, and use the matching release's recovery or restore procedure. Do not blindly update `basyxsystem.state` to `clean`: that marker does not prove that a partially applied patch was repaired. Run the matching Configuration Service again only after the failure cause and the migration's recovery requirements have been addressed; verify the resulting schema before restarting runtimes.

## Idempotency Expectations

The base schema uses idempotent SQL where possible, such as `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`.

Patch files should also be safe to run in controlled deployment scenarios. The service checks the database version before running a patch, but the patch author is still responsible for writing safe SQL and updating the database version within the patch file.

## Versioning Concept

The database schema version is stored in `basyxsystem.schema_version`. The schema state is stored in `basyxsystem.state`.

Regular BaSyx services validate both values during startup. If the schema version does not match the expected service version, or if the state is `dirty`, the service fails fast instead of running against an unsafe schema.

```{warning}
Use the same image tag for `basyxconfigurationservice` and the DB-backed runtime services. For native builds, use one source release for the Configuration Service and runtime services. A newer runtime service may require schema changes that an older Configuration Service cannot apply.
```

Application and schema versions are related but not interchangeable. The Configuration Service included in a release contains the registered migrations, and that release's runtime services define the schema they accept.

## Upgrading an existing database

Use this procedure when the PostgreSQL database already contains BaSyx data. Deployment ordering alone is not a migration plan.

1. Record the current `basyxsystem.schema_version` and `basyxsystem.state`, and confirm which database every BaSyx process uses.
2. Identify the target **application release** and the database **schema version** expected by that release. Keep those version dimensions distinct.
3. Read the migration notes and SQL-patch prerequisites for every schema transition between the current and target versions.
4. Verify prerequisites in a representative environment, including adequate storage, database permissions, and a tested restore path.
5. Plan a maintenance window and identify every runtime, worker, administrative tool, and external client that can access the affected database.
6. Stop those database users when a migration requires quiescence, and verify that old processes are no longer connected. Starting a Job or using a Compose completion dependency does not do this for you.
7. Take a complete pre-upgrade backup after quiescence. Where attachments or thumbnails are present, the backup must include their PostgreSQL Large Objects as well as ordinary tables. Verify that the backup is restorable before proceeding.
8. Run only the Configuration Service that matches the target application release, using the base schema and registered patch assets from that same release.
9. Require a successful process exit, then verify the resulting `basyxsystem.schema_version` and `basyxsystem.state`. Do not start target runtimes while the state is dirty or the version is unexpected.
10. Start runtime services from the matching application release, and confirm that their schema checks complete successfully.
11. Verify representative metadata and binary content after startup, including attachment and thumbnail download where those data types are used. Retain the pre-upgrade backup until these checks and application-level validation succeed.

### Attachment and thumbnail transition at schema v1.1.8

The patch [`1_1_8.sql`](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/database/patches/1_1_8.sql) is a **database schema transition to v1.1.8**, not an application release numbered 1.1.8. It introduces canonical binary-content and reference structures used by File attachments and thumbnails. When an upgrade crosses this transition, treat it as a quiesced database upgrade: stop all database-backed BaSyx services, back up the database including Large Objects, run the matching Configuration Service alone, and verify attachment and thumbnail reads after the matching runtimes start. Legacy attachment Large Objects are not rewritten by this patch, so their presence makes complete backup and post-upgrade binary checks essential.

### Rollback

Changing a runtime or Configuration Service image back to an older tag does not roll the database schema or migrated data back. If the upgrade must be reversed, stop all database users and restore the complete pre-upgrade database backup, including Large Objects, before starting the older matching application release. Do not try to manufacture rollback by changing only `basyxsystem.schema_version` or by clearing a dirty marker.

## Restart Behavior

After the upgrade prerequisites and failure-recovery checks above are satisfied, the Configuration Service can be restarted. On restart:

- The system table step is idempotent.
- The base schema upload is skipped when core base schema tables are already present.
- Already applied patches are skipped when the schema version is equal to or newer than the patch target version.
