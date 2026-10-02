# Capabilities and Limits

## What the Service Does

The BaSyx Configuration Service performs database initialization tasks required before regular BaSyx services start.

It currently supports:

- Loading database connection settings through the common BaSyx configuration mechanism.
- Connecting to PostgreSQL using the configured `postgres` settings.
- Creating and seeding the `basyxsystem` table when it is missing or empty.
- Uploading the base SQL schema from `base.sql` when the recorded schema version is below the baseline threshold for the release.
- Applying registered SQL patch files only when the database schema version is older than the patch target version.
- Tracking the schema version and schema state through `basyxsystem.schema_version` and `basyxsystem.state`.
- Using PostgreSQL advisory locks to coordinate schema initialization and patch execution.
- Exiting with a non-zero status code when initialization fails.

The base-schema decision is version-based. If the recorded schema version has reached the baseline threshold, the service skips `base.sql`; it does not independently verify that every expected base table exists.

## What the Service Does Not Do

The BaSyx Configuration Service is intentionally narrow in scope.

It does not provide:

- A general-purpose orchestration platform.
- A workflow engine for business processes.
- Runtime business process execution.
- A replacement for Kubernetes, Docker Compose, Helm, or other deployment tooling.
- Automatic backup or database dump creation.
- A browser-based administration UI.
- Dynamic patch discovery from arbitrary folders.
