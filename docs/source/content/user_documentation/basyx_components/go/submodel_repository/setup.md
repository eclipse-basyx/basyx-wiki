# Setting Up the Submodel Repository

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

We provide example setups to get you started with the BaSyx Go Components in the [examples directory](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

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

Use the same image tag for every BaSyx Go service sharing this database, including the Configuration Service.

### Before the First Start

This minimal Compose file does not declare a named PostgreSQL volume. Do not rely on container removal or recreation to preserve data. For durable local state, add the release-appropriate named-volume mount before creating data; adding one later does not migrate an existing anonymous volume. See [Persistent State](../common/deployment.md#persistent-state) for the PostgreSQL 18 mount path, lifecycle table, and safe cleanup guidance.

The local example is unsecured: ABAC remains at its default `false` value. If you enable it, follow the [Runtime Security](../common/security) workflow for the trust list, access rules, and verification. The Submodel Repository's default policy import mode is `if_missing`: after an active policy exists in PostgreSQL, editing the mounted file and restarting does not replace that policy. Review [Policy Persistence and Restart Behavior](../common/security.md#policy-persistence-and-restart-behavior) before changing policy files.

### Start and Check the Repository

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

The Compose example explicitly selects port `8085`. When using a context path, include it in health, Swagger, and API URLs; for example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8085/api/v3/health`.

### Access Rules and Trustlist Files (Secured Setup)

For the complete OIDC/ABAC workflow and policy lifecycle, see [Runtime Security](../common/security). For the configuration keys and file mounts, see [Security Configuration Files (Common)](../common/configuration.md#security-files).

For this component in Docker Compose, mount the security files into the container and configure `ABAC_ENABLED=true`, `ABAC_MODELPATH`, and `OIDC_TRUSTLISTPATH` if you enable ABAC.

## Using BaSyx Go Components without Docker
If you need to run the Submodel Repository without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker Images for production use-cases, as they are pre-configured and optimized for production environments.
```

### Prerequisites
- [Go](https://go.dev/dl/) at the version declared by the selected release's `go.mod`.
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository

Download the source code:
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
cd basyx-go-components
git checkout RELEASE_TAG
```

Replace `RELEASE_TAG` with the stable release you intend to build. Use the Configuration Service and SQL assets from this same checkout.

### Building the Binary

From the repository root, change to the Submodel Repository service directory:
```bash
cd cmd/submodelrepositoryservice
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
