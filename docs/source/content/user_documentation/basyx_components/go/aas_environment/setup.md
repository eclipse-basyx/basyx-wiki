# Setting Up the AAS Environment

This setup runs the `1.0.11` AAS Environment with PostgreSQL 18 and the matching `1.0.11` Configuration Service. It exposes one application URL, `http://localhost:8090`, and is sufficient for the complete [first-use walkthrough](usage). No separate Registry, Discovery, or UI container is required.

Review the [version distinctions](../common/deployment.md#version-scope) before mixing images or source builds. For an existing database, do not treat startup as an upgrade procedure: follow [Upgrading an Existing Database](../configuration_service/operations.md#upgrading-an-existing-database) first.

## Prerequisites and Security Posture

- Docker with Docker Compose
- host port `8090` available

```{warning}
This local example explicitly sets `ABAC_ENABLED=false`. Its APIs accept unauthenticated requests and must not be exposed to an untrusted network. Configure and verify [Runtime Security](../common/security) before using this topology outside a trusted development environment.
```

## Compose Configuration

Save the following as `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: basyxTestDB
    command: ["postgres", "-c", "listen_addresses=*"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d basyxTestDB"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - aas_environment_postgres:/var/lib/postgresql

  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:1.0.11
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DBNAME: basyxTestDB
    depends_on:
      postgres:
        condition: service_healthy

  aas_environment:
    image: eclipsebasyx/aasenvironment-go:1.0.11
    environment:
      SERVER_PORT: 5004
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DBNAME: basyxTestDB
      GENERAL_AASREGISTRYINTEGRATION: "true"
      GENERAL_SUBMODELREGISTRYINTEGRATION: "true"
      GENERAL_EXTERNALURL: http://localhost:8090
      ABAC_ENABLED: "false"
    ports:
      - "8090:5004"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully

volumes:
  aas_environment_postgres:
```

The database health check prevents initialization from starting too early. The Configuration Service initializes or migrates the schema as a one-shot job, and the AAS Environment starts only after that job exits successfully. Both Registry synchronization flags are enabled because the usage walkthrough verifies generated AAS and Submodel descriptors. `GENERAL_EXTERNALURL` matches the host URL clients use, so those descriptors advertise reachable endpoints.

Do not add `GENERAL_DISCOVERYINTEGRATION`: the AAS Environment executable forces Discovery integration on. The three services above are the complete topology for this walkthrough.

## Start and Check Readiness

Start the project:

```bash
docker compose up -d
```

The Configuration Service container completing with exit code `0` is expected. If it fails against a previously used database, inspect its logs and follow the [database upgrade guidance](../configuration_service/operations.md#upgrading-an-existing-database) rather than deleting persistent data.

Wait until the Environment is ready:

```bash
curl -i http://localhost:8090/health
```

Continue when the response is HTTP `200` with `{"status":"UP"}`. Swagger UI is available at [http://localhost:8090/swagger](http://localhost:8090/swagger). Then follow [Using the AAS Environment](usage).

## Persistent State and Stopping

The named volume `aas_environment_postgres` stores PostgreSQL 18 data at `/var/lib/postgresql`. `docker compose stop` stops the containers and `docker compose down` removes the containers and network while retaining the named volume. A later `docker compose up -d` reuses it. `docker compose down -v` also deletes the volume and its stored AASs, Submodels, Concept Descriptions, descriptors, Discovery mappings, and configuration state.

```{warning}
Do not run `docker compose down -v` when the data must be retained. Adding or renaming a volume later does not migrate the old database. See [Persistent State](../common/deployment.md#persistent-state) for lifecycle and backup considerations.
```

For a larger topology with automatic AASX preconfiguration and a Web UI, see the release-pinned [BaSyx Minimal Example](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxMinimalExample). Its Compose file at that revision uses mutable `SNAPSHOT` BaSyx image tags; replace those tags with `1.0.11` or pin image digests before using it as a release-matched deployment.
