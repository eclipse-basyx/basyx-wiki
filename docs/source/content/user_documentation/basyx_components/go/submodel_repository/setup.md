# Setting Up the Submodel Repository

The selected release's `examples/` directory contains additional deployment setups. The configuration below provides a minimal standalone Submodel Repository with PostgreSQL and the BaSyx Configuration Service.

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to use and set up the Submodel Repository is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx Submodel Repository (Go)

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

  submodel_repository:
    container_name: submodel_repository
    image: eclipsebasyx/submodelrepository-go:latest
    pull_policy: always
    environment:
      - SERVER_PORT=8085
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8085:8085"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Submodel Repository*

Use the same image tag for every BaSyx Go service sharing this database, including the Configuration Service. For reproducible deployments, replace `latest` with the same concrete BaSyx version tag for all of these services. Alternatively, pin each service image to the corresponding immutable image digest from the same release. The `latest` tag is mutable and advances when a new release is published.

### Start and Check the Repository

```{warning}
This minimal local Compose setup does not declare a named PostgreSQL volume. An image-created anonymous volume is not automatically reused after `docker compose down`, so recreating the containers can make previously stored data appear to be lost. Add a correctly mounted named volume before storing persistent data, and migrate existing data explicitly rather than expecting a new volume declaration to copy it. See [Persistent State](../common/deployment.md#persistent-state).
```

Save the example as `docker-compose.yml`, then run the following command in the same directory:

```bash
docker compose up -d
```

The Configuration Service is a one-time initialization/migration job. An exit code of `0` is expected. The Repository starts only after that job completes successfully.

Once the Repository is ready, check its health:

```bash
curl -i http://localhost:8085/health
```

Expect HTTP `200` with `{"status":"UP"}`. In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:8085/swagger) to explore the API, then follow [Using the Submodel Repository](usage) to create your first Submodel.

The Compose example explicitly selects port `8085`. When using a context path, include it in health, Swagger, and API URLS. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8085/api/v3/health`.

### Security Configuration

The local Compose example does not enable authorization and is not a secured deployment. To enable OIDC-based ABAC, set `ABAC_ENABLED=true`, mount the access-rule and OIDC trust-list files, and configure their container paths. When `ABAC_POLICY_FILE_IMPORT` is omitted, the effective import mode is `if_missing`, so editing a mounted policy file and restarting does not replace an active policy already stored in PostgreSQL. See [OIDC and ABAC Configuration](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files) before exposing the service.

The Submodel Repository also supports experimental relationship-based access control (ReBAC). ReBAC is disabled by default, requires ABAC and a readable OIDC trust list, and can be enabled with `REBAC_ENABLED=true`. For ReBAC-covered routes—including Submodels, Submodel Elements, attachments, and synchronous and asynchronous Operation invocation, status, and results—an authenticated request is allowed when either ABAC or ReBAC grants access. Anonymous requests and endpoints outside the ReBAC-covered routes remain ABAC-only. In particular, `$history`, `$recent-changes`, event feed endpoints, and `$signed` representations remain ABAC-only. If multiple ReBAC-capable BaSyx services share the same database, enable ReBAC consistently across them; services running without ReBAC do not apply ReBAC grants or ownership semantics. See [Relationship-Based Access Control](../common/rebac) for configuration and access-management details.

## Using BaSyx Go Components without Docker
If you need to run the Submodel Repository without Docker, build the binary from source for your target platform.

Published BaSyx container images provide a ready-to-run distribution of the service. The minimal Compose example above is intentionally unsecured and is not, by itself, a production-ready deployment configuration.

### Prerequisites
- [Go](https://go.dev/dl/) at the version declared by the selected release's `go.mod`.
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository

Download the source code:
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout RELEASE_TAG
```

Replace `RELEASE_TAG` with the stable release you intend to build. Use the Configuration Service and SQL assets from this same checkout.

### Building the Binary

Change to the Submodel Repository service directory:
```bash
cd basyx-go-components/cmd/submodelrepositoryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o submodelrepositoryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o submodelrepositoryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

#### Linux / macOS

Run the service with:
```bash
./submodelrepositoryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\submodelrepositoryservice.exe -config .\config.yaml
```

The Submodel Repository does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
