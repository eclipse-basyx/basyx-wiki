# Docker Compose Integration

In Docker Compose deployments, run the BaSyx Configuration Service after PostgreSQL is healthy and before regular BaSyx services start.

```{warning}
Use the same image tag for `basyxconfigurationservice` and the runtime services that share its database. This example uses `latest` for both.
```

If the named volume already contains BaSyx data, do not treat `depends_on` as a complete upgrade procedure. `service_completed_successfully` orders the new processes shown in the Compose project, but it does not stop older containers, external services, or other database clients. Back up and, where required, quiesce the database by following [Upgrading an existing database](operations.md#upgrading-an-existing-database) before starting the migration.

## Minimal Example

```yaml
services:
  db:
    image: postgres:16
    container_name: postgres_db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: basyxTestDB
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d basyxTestDB"]
      interval: 5s
      timeout: 5s
      retries: 20
    volumes:
      - postgres_data:/var/lib/postgresql/data

  basyx_configuration:
    container_name: basyx_configuration
    image: eclipsebasyx/basyxconfigurationservice-go:latest
    environment:
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DBNAME: basyxTestDB
      POSTGRES_MAXOPENCONNECTIONS: 50
      POSTGRES_MAXIDLECONNECTIONS: 25
      POSTGRES_CONNMAXLIFETIMEMINUTES: 5
      POSTGRES_CONNMAXIDLETIMEMINUTES: 0
    depends_on:
      db:
        condition: service_healthy

  submodelrepository:
    image: eclipsebasyx/submodelrepository-go:latest
    environment:
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DBNAME: basyxTestDB
      POSTGRES_MAXOPENCONNECTIONS: 50
      POSTGRES_MAXIDLECONNECTIONS: 25
      POSTGRES_CONNMAXLIFETIMEMINUTES: 5
      POSTGRES_CONNMAXIDLETIMEMINUTES: 0
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully

volumes:
  postgres_data:
```

`postgres_data` is a named volume mounted at the PostgreSQL 16 data directory, `/var/lib/postgresql/data`. It preserves the database across ordinary container replacement. Manage its lifecycle explicitly and include its database in backups; removing the volume removes the persisted database. See [Deployment, Versions, and Persistent State](../common/deployment.md).

## Startup Ordering

Recommended ordering:

1. PostgreSQL starts.
2. PostgreSQL health check succeeds.
3. `basyx_configuration` runs and exits successfully.
4. BaSyx services start.

Use `condition: service_completed_successfully` for services that depend on the database schema being initialized.

For an existing database, this only controls when the new `submodelrepository` process starts. It does not prove that every old process has stopped using the database.

Each container process has its own PostgreSQL pool. In this example, the Configuration Service exits before the Submodel Repository starts, so their configured limits do not normally overlap. Account for both during manual restarts or upgrades where they may run at the same time, and add the limits of all concurrently running service replicas when sizing PostgreSQL.

Update the Configuration Service and runtime images as one tag-aligned change. See [Version Scope](../common/deployment.md#version-scope) for the shared tag convention.

## Custom Schema and Patch Paths

The container image copies the repository database files into `/app`. By default, the service reads:

- Base schema: `/app/base.sql`
- Patch directory: `/app/patches`

For local or custom setups, override the command:

```yaml
basyx_configuration:
  image: eclipsebasyx/basyxconfigurationservice-go:latest
  command:
    - /app/basyxconfigurationservice
    - -databaseSchema
    - /custom/base.sql
    - -customPatchPath
    - /custom/patches
  volumes:
    - ./database:/custom:ro
```
