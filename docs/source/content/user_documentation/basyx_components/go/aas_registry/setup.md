# Setting Up the AAS Registry
We provide example setups to get you started with the BaSyx Go Components in the [example directory](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.0/examples).
But if you need to configure the service yourself, this page will guide you through.

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to use and set up the AAS Registry is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration (Go)
3. BaSyx AAS Registry (Go)

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

  aas_registry:
    image: eclipsebasyx/aasregistry-go:latest
    pull_policy: always
    container_name: aas_registry
    environment:
      - SERVER_PORT=8082
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8082:8082"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Go Configuration Service, and BaSyx Go AAS Registry*

Use the same image tag for every BaSyx Go service sharing this database, including the Configuration Service. For reproducible deployments, replace `latest` with the same concrete BaSyx version tag for all of these services. Alternatively, pin each service image to the corresponding immutable image digest from the same release. The `latest` tag is mutable and advances when a new release is published.

### Start and Check the Registry

```{warning}
This minimal local Compose setup does not declare a named PostgreSQL volume. An image-created anonymous volume is not automatically reused after `docker compose down`, so recreating the containers can make previously stored data appear to be lost. Add a correctly mounted named volume before storing persistent data, and migrate existing data explicitly rather than expecting a new volume declaration to copy it. See [Persistent State](../common/deployment.md#persistent-state).
```

The services can be started by running the following command in the directory of the compose file:

```bash
docker compose up -d
```

The Configuration Service is a one-time initialization/migration job. An exit code of `0` is expected. The Registry starts only after that job completes successfully.

Once the Registry is ready, check its health:

```bash
curl -i http://localhost:8082/health
```
Expect HTTP `200` with `{"status":"UP"}`. Open [Swagger UI](http://localhost:8082/swagger) to explore the API. To help you with the first steps using the registry, follow [Using the AAS Registry](usage) to register your first descriptor.

The Compose example explicitly selects port `8082`. When using a context path, include it in health, Swagger, and API URLS. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8082/api/v3/health`.

### Security Configuration

The local Compose example does not enable authorization and is not a secured deployment. To enable OIDC-based ABAC, set `ABAC_ENABLED=true`, mount the access-rule and OIDC trust-list files, and configure their container paths. When `ABAC_POLICY_FILE_IMPORT` is omitted, the effective import mode is `if_missing`, so editing a mounted policy file and restarting does not replace an active policy already stored in PostgreSQL. See [OIDC and ABAC Configuration](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files) before exposing the service.

The standalone AAS Registry also supports experimental relationship-based access control (ReBAC). ReBAC is disabled by default, requires OIDC and ABAC, and can be enabled with `REBAC_ENABLED=true`. For ReBAC-covered Registry routes, an authenticated request is allowed when either ABAC or ReBAC grants access; anonymous requests and endpoints outside those routes remain ABAC-only. See [Relationship-Based Access Control](../common/rebac) for configuration and access-management details.

## Using BaSyx Go Components without Docker
If you need to run the AAS Registry without Docker, build the binary from source for your target platform.

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

Replace `RELEASE_TAG` with the stable release you intend to build. Initialize PostgreSQL using the Configuration Service and database schema files from the same checkout.

### Building the Binary

Change to the AAS Registry service directory:
```bash
cd basyx-go-components/cmd/aasregistryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o aasregistryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o aasregistryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

#### Linux / macOS

Run the service with:
```bash
./aasregistryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\aasregistryservice.exe -config .\config.yaml
```

The AAS Registry does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
