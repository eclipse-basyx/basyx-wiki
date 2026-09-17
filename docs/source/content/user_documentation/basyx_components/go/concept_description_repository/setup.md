# Setting Up the Concept Description Repository

The Docker and native instructions on this page target BaSyx Go **1.0.11**. Keep the Repository, Configuration Service, source checkout, and database schema aligned as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose

The minimal setup contains PostgreSQL, the one-time BaSyx Configuration Service database initializer, and the Concept Description Repository:

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres_basyx_cd
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

  basyx_configuration:
    container_name: basyx_configuration_cd
    image: eclipsebasyx/basyxconfigurationservice-go:1.0.11
    pull_policy: always
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    depends_on:
      postgres:
        condition: service_healthy

  concept_description_repository:
    container_name: concept_description_repository
    image: eclipsebasyx/conceptdescriptionrepository-go:1.0.11
    pull_policy: always
    environment:
      - SERVER_PORT=8086
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8086:8086"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```

Use the same BaSyx release for every service sharing this database.

```{note}
BaSyx Go 1.0.11's checked-in Concept Description configuration uses port `5004`, while the image declares `SERVER_PORT=5000`. Set `SERVER_PORT` explicitly, as the example does, rather than relying on either default.
```

```{warning}
This minimal example has no named PostgreSQL volume. Add and correctly mount one before storing data that must survive container recreation. See [Persistent State](../common/deployment.md#persistent-state).
```

Save the example as `docker-compose.yml`, then start it:

```bash
docker compose up -d
curl -i http://localhost:8086/health
```

The Configuration Service is expected to exit with code `0` after initializing or migrating the schema. The Repository starts only after it succeeds. A ready Repository returns HTTP `200` with `{"status":"UP"}`. Swagger UI is available at [http://localhost:8086/swagger](http://localhost:8086/swagger).

## Configuration File

The image contains a configuration file at `/config/config.yaml`. To supply your own file, mount it at that path. This representative configuration uses the same values as the Compose example:

```yaml
server:
  port: 8086
  contextPath: ""
  host: 0.0.0.0
  strictVerification: permissive

postgres:
  host: postgres
  port: 5432
  user: admin
  password: admin123
  dbname: basyxTestDB
  maxOpenConnections: 50
  maxIdleConnections: 25
  connMaxLifetimeMinutes: 5
  connMaxIdleTimeMinutes: 0

oidc:
  trustlistPath: "config/trustlist.json"

abac:
  enabled: false
  modelPath: "config/access_rules/access-rules.json"
```

Do not combine `postgres.dsn` with the individual host, port, user, password, database, or SSL settings. See [General Configuration](../common/configuration) for the complete shared configuration model.

### Environment Variables

Environment variables use uppercase configuration paths with dots replaced by underscores:

| Environment variable | Purpose |
| --- | --- |
| `SERVER_PORT` | HTTP listen port. Set this explicitly. |
| `SERVER_CONTEXTPATH` | Optional prefix for every service route. |
| `SERVER_STRICTVERIFICATION` | Model verification mode: `off`, `permissive`, or `strict`. |
| `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DBNAME` | Writer database connection. |
| `POSTGRES_DSN` | Alternative complete writer connection string. Do not mix it with the individual connection fields. |
| `POSTGRES_READER_HOST`, `POSTGRES_READER_PORT`, `POSTGRES_READER_USER`, `POSTGRES_READER_PASSWORD`, `POSTGRES_READER_DBNAME` | Optional read-replica connection. Omit all reader settings to reuse the writer pool. |
| `ABAC_ENABLED` | Enables ABAC enforcement. Default: `false`. |
| `ABAC_MODELPATH` | Path to the mounted access-rule model. |
| `ABAC_POLICY_FILE_IMPORT` | Policy import mode. The default is `if_missing`. |
| `OIDC_TRUSTLISTPATH` | Path to the mounted OIDC trust list. |

An explicitly configured reader may be eventually consistent. Omit it when requests must immediately read their own writes.

### Secured Setup

The Compose example is unsecured. To enable the supported security middleware, set `ABAC_ENABLED=true`, mount the access-rule and OIDC trust-list files, and set their container paths. A mounted policy is not automatically re-imported on every restart: the effective default import mode is `if_missing`. Follow [Runtime Security](../common/security), including its policy-persistence guidance.

## Running without Docker

Use PostgreSQL initialized by a Configuration Service from the same release, then build the service from the release checkout:

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout v1.0.11
cd basyx-go-components/cmd/conceptdescriptionrepositoryservice
go build -o conceptdescriptionrepositoryservice
./conceptdescriptionrepositoryservice -config ./config.yaml
```

On Windows, build `conceptdescriptionrepositoryservice.exe` and run `./conceptdescriptionrepositoryservice.exe -config ./config.yaml` in PowerShell. The service validates the existing database schema; it does not initialize that schema itself.
