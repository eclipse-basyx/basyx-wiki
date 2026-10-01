# When to Start the Service

For BaSyx deployments that use the shared PostgreSQL schema, run the Configuration Service whenever the database needs to be initialized or migrated. It is also useful as a one-shot deployment prerequisite so that this preparation happens automatically when necessary.

Regular BaSyx services validate that the database state is `clean` and that its schema version exactly matches the version expected by the running release. They do not check whether the Configuration Service ran during the current startup. An ordinary restart can reuse a database that already passes those checks.

## When Schema Preparation Is Required

Start the BaSyx Configuration Service in these situations:

- **Before the first start of BaSyx components**: On a fresh database, the service creates the system version table, uploads the base schema, and applies registered patches.
- **Before starting BaSyx services after an update**: When a new BaSyx version introduces database patches, run the Configuration Service first so the database reaches the version expected by the updated services.
- **Before restarting services against a recreated database**: If the PostgreSQL volume was removed or the database was recreated, run the Configuration Service before any BaSyx service starts.

## Recommended Startup Order

Use this order for database-backed BaSyx deployments:

1. Start PostgreSQL.
2. Wait until PostgreSQL is healthy.
3. Start the BaSyx Configuration Service.
4. Wait until the Configuration Service exits successfully.
5. Start the regular BaSyx services.

In Docker Compose, dependent services should use `service_completed_successfully` for the Configuration Service dependency.

## Existing Databases

The Configuration Service can remain part of deployment sequencing for existing databases. It uses the recorded schema version to skip the base upload and registered patches that are no longer required. It does not verify the presence of every expected table before skipping the base schema.

This idempotent deployment pattern is suitable for fresh installations and upgrades, but it is not a technical requirement for every ordinary restart.

## When It Does Not Apply

The Configuration Service is not relevant for deployments that do not use the BaSyx PostgreSQL schema. A PostgreSQL-backed deployment whose database is already `clean` and at the exact schema version expected by its runtime services does not require another Configuration Service run solely because those services restart.
