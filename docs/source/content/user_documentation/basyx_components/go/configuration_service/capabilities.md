# Capabilities and Limits

## What the Service Does

The BaSyx Configuration Service performs database initialization tasks required before regular BaSyx services start.

It currently supports:

- Loading database connection settings through the common BaSyx configuration mechanism.
- Connecting to PostgreSQL using the configured `postgres` settings.
- Creating and seeding the `basyxsystem` version table when it is missing or empty.
- Uploading the base SQL schema from `base.sql` when the base schema is not yet present.
- Applying registered SQL patch files only when the database version is older than the patch target version.
- Serializing schema and patch execution with a PostgreSQL advisory lock.
- Exiting with a non-zero status code when initialization fails.

The service uses ordered initialization sequences internally. From an integrator perspective, this means startup steps run deterministically in the order registered by the service binary.

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

Deployment tooling is still responsible for starting containers, defining dependencies, configuring volumes, and managing persistent PostgreSQL storage.

