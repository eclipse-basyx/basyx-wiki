# Deployment and Versions

Use this page to keep BaSyx images, database initialization assets, and persistent PostgreSQL data aligned. Component setup pages contain runnable examples; this page defines the shared deployment contract behind them.

(version-scope)=
## Version Scope

Normal container examples in this documentation use the `latest` image tag. For BaSyx Go images, `latest` points to the latest stable BaSyx Go release. All component images published as part of that stable release, including the Configuration Service, receive the corresponding `latest` tag.

Use the same image tag for the Configuration Service and every database-backed BaSyx Go component that shares its database. The examples achieve this by using `latest` consistently. For reproducible deployments, use the same concrete release tag across those images. When immutable image selection is required, pin each image to the corresponding digest from that release.

The Configuration Service image contains the database schema and patch assets for its release. It initializes or migrates the database. Before accepting requests, runtime services require readable schema metadata whose recorded version exactly matches the version expected by that service and whose state is `clean`. They do not structurally inspect every database object. Normal setup does not require selecting an internal schema version separately.

Application releases, source revisions, Go toolchain requirements, database schema versions, and API or metamodel versions remain separate concepts. API and metamodel versions belong to individual component contracts; consult the component page and the running service's OpenAPI document rather than assuming one universal version.

## First Startup

BaSyx Go requires PostgreSQL 16 or newer. Upgrade PostgreSQL itself before running the Configuration Service when an existing deployment uses an older version.

A database-backed BaSyx deployment starts in this order:

1. Start PostgreSQL and wait until it is healthy.
2. Run the BaSyx Configuration Service using the same image tag as the runtime services and require successful completion.
3. Start the runtime services.

The Configuration Service is a one-shot job, so exit code `0` is the expected successful state. In Docker Compose, runtime services can express this ordering with `condition: service_completed_successfully`.

On an empty database, the Configuration Service creates the BaSyx base schema and applies its registered patches. That is **initialization**. Running it against a database that already contains BaSyx data can be an **upgrade** and requires the release-specific migration precautions described under [Existing Databases](#existing-databases). Startup ordering alone does not make an in-use database safe to migrate.

(persistent-state)=
## Persistent State

Database-backed BaSyx state belongs to PostgreSQL, not to the application containers. Use durable PostgreSQL storage and include PostgreSQL Large Objects in backup and migration procedures. Removing a Compose volume, replacing a Kubernetes volume, or declaring a new volume does not migrate the existing database; restore or migrate the data explicitly before directing BaSyx services to new storage.

## Existing Databases

Do not treat an existing database like an empty first-start database. Before changing BaSyx releases or applying a newer schema, stop database writers and take a tested backup. Run the matching Configuration Service and start the runtime services only after it exits successfully. Registered patches are upgrades, not reverse migrations; restore a compatible backup to roll back. See [Configuration Service operational considerations](../configuration_service/operations) for schema-state, compatibility, and migration-failure guidance.

Use [Configuration Service usage](../configuration_service/usage) for the initializer's flags and registered-patch behavior. Keep the selected runtime release, Configuration Service, and source SQL assets aligned.
