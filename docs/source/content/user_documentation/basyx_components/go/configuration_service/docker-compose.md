# Docker Compose Integration

In Docker Compose deployments, run the BaSyx Configuration Service after PostgreSQL is healthy and before regular BaSyx services start.

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
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
      db:
        condition: service_healthy
    environment:
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DBNAME: basyxTestDB

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

## Persistent Storage

Use persistent PostgreSQL storage for non-temporary deployments. Without persistent storage, the database is recreated whenever the database volume is removed, and the Configuration Service will upload the base schema again.

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

