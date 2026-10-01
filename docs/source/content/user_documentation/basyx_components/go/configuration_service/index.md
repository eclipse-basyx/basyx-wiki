# BaSyx Configuration Service

The BaSyx Configuration Service is a one-shot startup component for preparing the PostgreSQL database used by BaSyx services. It connects to the configured database, ensures the BaSyx system table exists, uploads the base database schema when required, and applies registered schema patches in version order.

It is intended to run before the BaSyx services that use the same database. After all registered initialization sequences finish successfully, the process exits.

## Purpose

Multiple BaSyx containers can share one PostgreSQL database. If each service tried to create or migrate the schema independently, startup races and conflicting schema changes could occur. The Configuration Service centralizes that responsibility in one component.

Typical use cases include:

- Initializing a fresh PostgreSQL database for BaSyx services.
- Applying standardized BaSyx database patches during deployment startup.
- Coordinating schema initialization in Docker Compose or other containerized environments.
- Making service startup depend on a completed database initialization job.

## User Benefits

The BaSyx Configuration Service makes database startup and upgrades safer and easier to operate.

Key benefits include:

- **Safer updates**: Database schema changes are applied centrally before regular BaSyx services start, reducing the risk of competing containers modifying the schema at the same time.
- **Version-aware patches**: Registered patches are skipped when the recorded schema version has already reached their target version.
- **Clear database state**: The current schema version and schema state are stored in the `basyxsystem` table. DB-backed BaSyx services verify the recorded version and require a `clean` state before serving requests.
- **Fail-fast protection**: DB-backed BaSyx services fail during startup if the schema metadata is unavailable, the recorded schema version does not exactly match the version expected by the service, or the recorded schema state is not `clean`.
- **Traceable errors**: Startup failures include BaSyx error codes such as `BASYXCFG-DB-CONNECT`, `BASYXCFG-SCHEMA-EXECUTE`, and `BASYXCFG-PATCH-EXECUTE`, making troubleshooting easier in container logs and CI pipelines.
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
