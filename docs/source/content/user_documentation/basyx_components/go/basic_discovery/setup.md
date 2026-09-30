# Setting Up the Basic Discovery Component

Additional deployment examples are available in the [BaSyx Go repository](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.0/examples). Use examples from the same release as the BaSyx components you deploy. The configuration below provides a minimal standalone Basic Discovery service with PostgreSQL and the BaSyx Configuration Service.

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to use and set up the Basic Discovery component is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx Basic Discovery (Go)

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres_basyx
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
    container_name: basyx_configuration
    image: eclipsebasyx/basyxconfigurationservice-go:latest
    pull_policy: always
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
      - POSTGRES_MAXOPENCONNECTIONS=50
      - POSTGRES_MAXIDLECONNECTIONS=25
      - POSTGRES_CONNMAXLIFETIMEMINUTES=5
      - POSTGRES_CONNMAXIDLETIMEMINUTES=0
    depends_on:
      postgres:
        condition: service_healthy

  aas_discovery:
    container_name: aas_discovery
    image: eclipsebasyx/aasdiscovery-go:latest
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
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Basic Discovery*

Use the same image tag for every BaSyx Go service sharing this database, including the Configuration Service.

### Start and Check the Discovery Service

```{warning}
This minimal local Compose setup does not declare a named PostgreSQL volume. An image-created anonymous volume is not automatically reused after `docker compose down`, so recreating the containers can make previously stored data appear to be lost. Add a correctly mounted named volume before storing persistent data, and migrate existing data explicitly rather than expecting a new volume declaration to copy it. See [Persistent State](../common/deployment.md#persistent-state).
```

Save the example as `docker-compose.yml`, then run the following command in the same directory:

```bash
docker compose up -d
```

The Configuration Service is a one-time initialization/migration job. An exit code of `0` is expected. The Discovery Service starts only after that job completes successfully.

Once the Discovery Service is ready, check its health:

```bash
curl -i http://localhost:8086/health
```

Expect HTTP `200` with `{"status":"UP"}`. In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:8086/swagger) to explore the API, then follow [Using Basic Discovery](usage) to register your first asset links.

The Compose example explicitly selects port `8086`. When using a context path, include it in health, Swagger, and API URLS. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8086/api/v3/health`.

### Security

The local Compose example is unsecured because it does not enable authorization. For secured deployments, configure OIDC together with the authorization mechanism required for your deployment. See [OIDC and ABAC Configuration](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files).

For Basic Discovery, an omitted `abac.policyFileImport` defaults to `if_missing`. Once an active policy exists in PostgreSQL, editing the file and restarting does not replace it.

For this component in Docker Compose, mount the security files into the container and configure `ABAC_ENABLED=true`, `ABAC_MODELPATH`, and `OIDC_TRUSTLISTPATH` if you enable ABAC.

### Relationship-Based Access Control

Basic Discovery also supports experimental relationship-based access control (ReBAC) for Discovery registrations. ReBAC is disabled by default and requires OIDC and ABAC to be enabled.

For ReBAC-covered Discovery routes, an authenticated request is allowed when either ABAC or ReBAC grants access. Anonymous requests and endpoints outside the ReBAC-covered Discovery routes remain governed by ABAC. The `/verify` endpoint, when enabled, remains ABAC-only.

Enable ReBAC with `rebac.enabled: true` or `REBAC_ENABLED=true`. When multiple BaSyx services share the same database, enable ReBAC consistently in all of them.

Discovery registrations can be shared through ReBAC. Registrations created through AAS Registry Discovery integration inherit access from their source descriptor. See [Relationship-Based Access Control](../common/rebac) for configuration and access-management details.

```{note}
ReBAC support described here applies to the standalone Basic Discovery component. The Digital Twin Registry uses ABAC only.
```

## Using BaSyx Go Components without Docker
If you need to run the Basic Discovery component without Docker, build the binary from source for your target platform.

Published container images are the normal deployment artifacts. A native build should use the same source release as the Configuration Service and database assets.

### Prerequisites
- [Go](https://go.dev/dl/) at the version declared by the selected release's `go.mod`.
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components.git
git -C basyx-go-components checkout RELEASE_TAG
```

Replace `RELEASE_TAG` with the stable release you intend to build. Use the Configuration Service and SQL assets from this same checkout.

### Building the Binary

Change to the Basic Discovery service directory:
```bash
cd basyx-go-components/cmd/discoveryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o discoveryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o discoveryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

Set the Discovery port explicitly in `config.yaml`:

```yaml
server:
  port: 8086
```

#### Linux / macOS

Run the service with:
```bash
./discoveryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\discoveryservice.exe -config .\config.yaml
```

The Basic Discovery component does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
