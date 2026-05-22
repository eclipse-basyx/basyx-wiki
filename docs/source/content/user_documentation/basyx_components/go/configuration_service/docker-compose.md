# Docker Compose Integration

In Docker Compose deployments, run the BaSyx Configuration Service after PostgreSQL is healthy and before regular BaSyx services start.

```{warning}
Use the same BaSyx version or build for `basyxconfigurationservice` and the runtime services.
```

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
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully

volumes:
  postgres_data:
```

## Startup Ordering

Recommended ordering:

1. PostgreSQL starts.
2. PostgreSQL health check succeeds.
3. `basyx_configuration` runs and exits successfully.
4. BaSyx services start.

Use `condition: service_completed_successfully` for services that depend on the database schema being initialized.

```{warning}
Mutable image tags such as `latest` and `SNAPSHOT` can change between restarts. If images are pulled fresh on restart, run `basyx_configuration` before DB-backed runtime services because schema requirements may have changed.
```

Pin exact image versions or image digests for reproducible deployments.

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
