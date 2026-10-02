# Setting Up the Digital Product Passport API

This setup runs BaSyx Go v1.1.0 of the DPP API and Configuration Service with PostgreSQL 18. It exposes the DPP API at `http://localhost:8088` and enables history so that the complete [usage walkthrough](usage) can retrieve an earlier passport state.

## Prerequisites and Security Posture

- Docker with Docker Compose
- host port `8088` available
- PostgreSQL 16 or newer for existing external database deployments

```{warning}
This local example uses illustrative credentials and explicitly disables ABAC. Its APIs accept unauthenticated requests and must not be exposed to an untrusted network. Replace the credentials, configure transport security, and enable [Runtime Security](../common/security) before using this topology beyond local development.
```

## Compose Configuration

Save the following as `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_USER: basyx_demo
      POSTGRES_PASSWORD: change-me
      POSTGRES_DB: basyxDpp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U basyx_demo -d basyxDpp"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - dpp_postgres:/var/lib/postgresql

  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:1.1.0
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: basyx_demo
      POSTGRES_PASSWORD: change-me
      POSTGRES_DBNAME: basyxDpp
    depends_on:
      postgres:
        condition: service_healthy

  dpp_api:
    image: eclipsebasyx/dppapi-go:1.1.0
    environment:
      SERVER_PORT: 8080
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: basyx_demo
      POSTGRES_PASSWORD: change-me
      POSTGRES_DBNAME: basyxDpp
      BASYX_HISTORY_MODE: api
      ABAC_ENABLED: "false"
    ports:
      - "8088:8080"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully

volumes:
  dpp_postgres:
```

The health check waits for PostgreSQL before the one-shot Configuration Service starts. The DPP API starts only after schema initialization or migration completes successfully. The Configuration Service is not required in normal request traffic after the database is prepared.

Use the same concrete BaSyx Go release tag for the Configuration Service and DPP API. For a reproducible deployment, alternatively pin both images to the corresponding immutable image digests from the same release. Do not combine a database migrated by one release with a runtime that expects another schema version.

`BASYX_HISTORY_MODE=api` records DPP-related AAS and Submodel changes required by the historical-read example. History is disabled by default in the stock service. Enabling it later does not reconstruct earlier states.

## Start and Check Readiness

Start the project:

```bash
docker compose up -d
```

The Configuration Service container completing with exit code `0` is expected. Wait until the DPP API is ready:

```bash
curl -i http://localhost:8088/health
```

Continue when the response is HTTP `200` with `{"status":"UP"}`. Swagger UI is available at [http://localhost:8088/swagger](http://localhost:8088/swagger).

## Configuration and Integrations

The DPP API uses the shared server, PostgreSQL, history, Registry-integration, observability, and security settings described in [General Configuration](../common/configuration). Configure a reader database only when the deployment can tolerate replica lag for read operations. Mutations and transaction-sensitive reads use the writer database.

The service can maintain AAS and Submodel descriptors in the same PostgreSQL database when the corresponding Registry-integration flags are enabled. A separate Registry process can expose those descriptors only when it uses that database. Registry services are not required for the DPP API itself.

The standalone DPP API does not expose the Submodel Repository attachment endpoint. If DPP content refers to database-managed `File` attachments, configure `general.externalUrl` with an externally reachable base URL for a deployment that exposes the corresponding `/submodels/.../attachment` route. Generated related-resource URLs use that route.

The DPP API uses the file-backed ABAC policy setup rather than the database-backed ABAC policy-management API. In v1.1.0, experimental ReBAC covers current-state DPP routes when enabled. Historical reads remain subject to the configured authentication and ABAC policies, but ReBAC does not cover the historical route. Historical resolution cannot apply a backend authorization filter to stored snapshots; when ABAC requires such a filter, the historical DPP is not returned. See [Runtime Security](../common/security) and [Relationship-Based Access Control](../common/rebac) before securing the service.

## Persistent State and Stopping

The named volume `dpp_postgres` stores the PostgreSQL data. `docker compose down` retains it; `docker compose down -v` deletes the database, including passports, recorded history, and Configuration Service state.

```{warning}
Do not remove the volume when the data must be retained. Back up PostgreSQL before upgrades or destructive operations and follow the [Configuration Service upgrade guidance](../configuration_service/operations.md#upgrading-an-existing-database).
```
