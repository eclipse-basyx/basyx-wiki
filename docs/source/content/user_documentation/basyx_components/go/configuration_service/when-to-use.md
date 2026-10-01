# When to Start the Service

**TL;DR:** Essentially, every time a BaSyx Go setup is run.

For BaSyx deployments that use the shared PostgreSQL database schema, the BaSyx Configuration Service is a required startup component. It prepares and updates the database schema before regular BaSyx services start.

Regular BaSyx services validate the database version during startup. If the Configuration Service has not initialized or updated the database first, those services can fail fast because the schema version is missing, outdated, or incompatible.

## Required Startup Points

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

The Configuration Service should also be part of deployments with existing databases. It detects already initialized schemas and skips work that is not required. Registered patches are executed only when the current database version is older than the patch target version.

This makes it suitable for both fresh installations and upgrades.

## When It Does Not Apply

The Configuration Service is not relevant only for deployments that do not use the BaSyx PostgreSQL schema at all. For BaSyx services running with PostgreSQL persistence, it should be treated as part of the required startup process.
