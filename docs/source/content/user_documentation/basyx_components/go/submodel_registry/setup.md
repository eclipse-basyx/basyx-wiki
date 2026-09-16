# Setting Up the Submodel Registry
We provide example setups to get you started with the BaSyx Go Components in the release-pinned [example directory](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples).
But if you need to configure the service yourself, this page will guide you through.

The Docker and native instructions on this page both target BaSyx Go **1.0.11**. Keep the Registry, Configuration Service, source checkout, and database schema aligned as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to use and set up the Submodel Registry is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx Submodel Registry (Go)

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
    image: eclipsebasyx/basyxconfigurationservice-go:1.0.11
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

  submodel_registry:
    container_name: submodel_registry
    image: eclipsebasyx/submodelregistry-go:1.0.11
    pull_policy: always
    environment:
      - SERVER_PORT=8083
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8083:8083"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Submodel Registry*

Use the same BaSyx release for every service sharing this database, including the Configuration Service, here `1.0.11`.

### Start and Check the Registry

```{warning}
This minimal local Compose file does not declare a named PostgreSQL volume. An image-created anonymous volume is not automatically reused after `docker compose down`; container recreation can therefore make the Registry appear empty. Add a correctly mounted named volume before storing persistent descriptors, and explicitly migrate existing data rather than expecting a new declaration to copy it. See [Persistent State](../common/deployment.md#persistent-state).
```

The services can be started by running the following command in the directory of the compose file:

```bash
docker compose up -d
```

The Configuration Service is a one-time initialization/migration job. An exit code of `0` is expected. The Submodel Registry starts only after that job completes successfully.

Once the Registry is ready, check its health:

```bash
curl -i http://localhost:8083/health
```

In Windows PowerShell, use `curl.exe` instead of `curl` to invoke curl rather than the PowerShell alias. Expect HTTP `200` with `{"status":"UP"}`. Open [Swagger UI](http://localhost:8083/swagger), then follow [Using the Submodel Registry](usage) to register your first descriptor.

The example uses port `8083` and an empty context path. If `server.contextPath` is configured, include it in health, Swagger, and API URLs. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8083/api/v3/health` and Swagger URL `http://localhost:8083/api/v3/swagger`.

### Access Rules and Trustlist Files (Secured Setup)

The local Compose example does not enable ABAC and is not a secured deployment. For this component, enable the supported middleware with `ABAC_ENABLED=true`, mount the access-rule and OIDC trust-list files, and configure their container paths. When `ABAC_POLICY_FILE_IMPORT` is omitted, the effective import mode is `if_missing`; editing a mounted policy and restarting does not replace an active policy already stored in PostgreSQL. Follow [Runtime Security](../common/security), especially [Policy Persistence and Restart Behavior](../common/security.md#policy-persistence-and-restart-behavior), before exposing the service.

## Using BaSyx Go Components without Docker
If you need to run the Submodel Registry without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker Images for production use-cases, as they are pre-configured and optimized for production environments.
```

### Prerequisites
- [Go](https://go.dev/dl/) `1.27.0` or a compatible newer toolchain, as specified by release 1.0.11's [`go.mod`](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/go.mod).
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository

Download the source code:
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout v1.0.11
```

Tag `v1.0.11` resolves to commit `81324eb3aad9d63baea93d3385bc9ca7e6a6a05a`. Initialize PostgreSQL with the Configuration Service and SQL assets from this same checkout.

### Building the Binary

Change to the Submodel Registry service directory:
```bash
cd basyx-go-components/cmd/submodelregistryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o submodelregistryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o submodelregistryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

#### Linux / macOS

Run the service with:
```bash
./submodelregistryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\submodelregistryservice.exe -config .\config.yaml
```

The Submodel Registry does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
