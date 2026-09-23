# Deployment and Versions

Use this page to keep BaSyx images, database initialization assets, and persistent PostgreSQL data aligned. Component setup pages contain runnable examples; this page defines the shared deployment contract behind them.

(version-scope)=
## Version Scope

Normal container examples in this documentation use the `latest` image tag. For BaSyx Go images, `latest` points to the latest stable BaSyx Go release. All component images published as part of that stable release, including the Configuration Service, receive the corresponding `latest` tag.

Use the same image tag for the Configuration Service and every database-backed BaSyx Go component that shares its database. The examples achieve this by using `latest` consistently. If a deployment instead selects a concrete release tag, use that tag consistently across those images. Deployments that require immutable inputs can pin a concrete release tag or image digest.

The Configuration Service image contains the database schema and patch assets for its release. It initializes or migrates the database, and runtime services validate that the resulting schema is compatible and clean before accepting requests. Normal setup does not require selecting an internal schema version separately.

Application releases, source revisions, Go toolchain requirements, database schema versions, and API or metamodel versions remain separate concepts. API and metamodel versions belong to individual component contracts; consult the component page and the running service's OpenAPI document rather than assuming one universal version.

## First Startup

A database-backed BaSyx deployment starts in this order:

1. Start PostgreSQL and wait until it is healthy.
2. Run the BaSyx Configuration Service using the same image tag as the runtime services and require successful completion.
3. Start the runtime services.

The Configuration Service is a one-shot job, so exit code `0` is the expected successful state. In Docker Compose, runtime services can express this ordering with `condition: service_completed_successfully`.

On an empty database, the Configuration Service creates the BaSyx base schema and applies its registered patches. That is **initialization**. Running it against a database that already contains BaSyx data can be an **upgrade** and requires the release-specific migration precautions described under [Existing Databases](#existing-databases). Startup ordering alone does not make an in-use database safe to migrate.

## Existing Databases

Do not treat an existing database like an empty first-start database. Before changing BaSyx releases or applying a newer schema, use the canonical [upgrading an existing database](../configuration_service/operations.md#upgrading-an-existing-database) procedure. It covers migration prerequisites, backup scope, workload quiescence, success checks, and restore-based rollback.

Use [Configuration Service usage](../configuration_service/usage) for the initializer's flags and registered-patch behavior. Keep the selected runtime release, Configuration Service, and source SQL assets aligned.
