# BaSyx Configuration Service

The BaSyx Configuration Service is a one-shot startup component for preparing the PostgreSQL database used by BaSyx services. It connects to the configured database, ensures the BaSyx system version table exists, uploads the base database schema when required, and applies registered schema patches in version order.

It is intended to run before the BaSyx services that use the same database. After all registered initialization sequences finish successfully, the process exits.

## Purpose

Multiple BaSyx containers can share one PostgreSQL database. If each service tried to create or migrate the schema independently, startup races and conflicting schema changes could occur. The Configuration Service centralizes that responsibility in one component.

Typical use cases include:

- Initializing a fresh PostgreSQL database for BaSyx services.
- Applying standardized BaSyx database patches during deployment startup.
- Serializing schema initialization in Docker Compose or containerized environments.
- Making service startup depend on a completed database initialization job.

## Existing BaSyx Setups

If you already operate a BaSyx (Go) setup that was created before the BaSyx Configuration Service was introduced, read the [Docker Compose Integration](docker-compose.md) guide before updating your deployment.

Existing setups must be adapted so the Configuration Service runs after PostgreSQL is healthy and before any database-backed BaSyx service starts. This is especially important for deployments that already have persistent PostgreSQL volumes, because the Configuration Service is responsible for checking the schema version and applying required patches before the updated services validate the database.

## User Benefits

The BaSyx Configuration Service makes database startup and upgrades safer and easier to operate.

Key benefits include:

- **Safer updates**: Database schema changes are applied centrally before regular BaSyx services start, reducing the risk of competing containers modifying the schema at the same time.
- **Reduced risk of data loss**: Patches are versioned and executed only when required. This helps avoid accidental repeated migrations and makes upgrade behavior more predictable.
- **Clear database versioning**: The current schema version is stored in the `basyxsystem` table. BaSyx services can verify that the database version matches the version they expect before serving requests.
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
