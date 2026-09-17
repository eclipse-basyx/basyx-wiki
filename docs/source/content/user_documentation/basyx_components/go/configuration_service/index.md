# BaSyx Configuration Service

The BaSyx Configuration Service is a one-shot startup component for preparing the PostgreSQL database used by BaSyx services. It connects to the configured database, ensures the BaSyx system table exists, uploads the base database schema when required, and applies registered schema patches in version order.

It is intended to run before the BaSyx services that use the same database. After all registered initialization sequences finish successfully, the process exits.

Preparing a new, empty database and migrating an existing database are different operational procedures. Startup ordering is sufficient for a fresh database, but it does not by itself make an upgrade safe: old processes might still be using the database, and migration-specific backup or quiescence requirements can apply. Before updating a database that contains data, follow [Upgrading an existing database](operations.md#upgrading-an-existing-database).

## Version Compatibility

Use the same image tag for the Configuration Service and the database-backed BaSyx Go components that share a database. The examples use `latest`; see [Version Scope](../common/deployment.md#version-scope) for the stable-tag convention and guidance for explicitly pinned deployments.

## Purpose

Multiple BaSyx containers can share one PostgreSQL database. If each service tried to create or migrate the schema independently, startup races and conflicting schema changes could occur. The Configuration Service centralizes that responsibility in one component.

Typical use cases include:

- Initializing a fresh PostgreSQL database for BaSyx services.
- Applying standardized BaSyx database patches during deployment startup.
- Serializing schema initialization in Docker Compose or containerized environments.
- Making service startup depend on a completed database initialization job.

## User Benefits

The BaSyx Configuration Service makes database startup and upgrades safer and easier to operate.

Key benefits include:

- **Safer updates**: Database schema changes are applied centrally before regular BaSyx services start, reducing the risk of competing containers modifying the schema at the same time.
- **Reduced risk of data loss**: Patches are versioned and executed only when required. This helps avoid accidental repeated migrations and makes upgrade behavior more predictable.
- **Clear database state**: The current schema version and schema state are stored in the `basyxsystem` table. BaSyx services can verify that the database is compatible and clean before serving requests.
- **Fail-fast protection**: If the database schema is missing, outdated, or incompatible, services fail during startup instead of running against an unsafe database state.
- **Traceable errors**: Startup failures include stable BaSyx error codes such as `BASYXCFG-DB-CONNECT`, `BASYXCFG-SCHEMA-EXECUTE`, and `BASYXCFG-PATCH-EXECUTE`, making troubleshooting easier in container logs and CI pipelines.
- **Repeatable deployments**: The same initialization flow can be used for local development, Docker Compose examples, CI environments, and containerized deployments.
- **Simpler service containers**: Regular BaSyx services no longer need to own schema initialization. They can focus on their runtime responsibilities and rely on a prepared database.
- **Predictable startup ordering**: Deployment tooling can wait for the Configuration Service to complete successfully before starting dependent services.
- **Improved auditability**: Schema changes are represented as explicit SQL patch files, making it easier to understand which database changes belong to which release.

## Documentation

- [Capabilities and Limits](capabilities.md)
- [When to Use the Service](when-to-use.md)
- [Basic Usage](usage.md)
- [Docker Compose Integration](docker-compose.md)
- [Kubernetes Job Integration](kubernetes-job.md)
- [Operational Considerations](operations.md)
- [Deployment, Versions, and Persistent State](../common/deployment.md)

```{warning}
This note is only relevant for users with BaSyx Go deployments created before v1.0.0. If you already operate such a setup, read the [Docker Compose Integration](docker-compose.md) guide before updating your deployment.

Existing pre-v1.0.0 setups must be adapted so the Configuration Service runs after PostgreSQL is healthy and before any database-backed BaSyx service starts. This is especially important for deployments with persistent PostgreSQL volumes, because the Configuration Service checks the schema version and applies required patches before updated services validate the database.
```

```{toctree}
:hidden:
:maxdepth: 1

capabilities
when-to-use
usage
docker-compose
kubernetes-job
operations
```
