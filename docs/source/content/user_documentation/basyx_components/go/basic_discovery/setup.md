# Setting Up the Basic Discovery Component
We provide example setups to get you started with the BaSyx Go Components in the [examples directory](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

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

This minimal example does not declare a named PostgreSQL volume. Container recreation can therefore leave a new database container attached to different storage and make existing data appear lost. Add the [version-correct named volume](../common/deployment.md#persistent-state) before creating data when persistence is required; adding one later does not migrate data from an existing anonymous volume.

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

The Compose example explicitly selects port `8086`. When using a context path, include it in health, Swagger, and API URLs; for example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8086/api/v3/health`.

### Access Rules and Trustlist Files (Secured Setup)

The local Compose example is unsecured because it does not enable ABAC. Security-related settings or mounted files do not secure the service unless the OIDC/ABAC middleware is enabled and configured with a matching policy. Follow [Runtime Security](../common/security) for the complete workflow and [Security Configuration Files](../common/configuration.md#security-files) for the field reference.

For Basic Discovery, an omitted `abac.policyFileImport` defaults to `if_missing`. Once an active policy exists in PostgreSQL, editing the file and restarting does not replace it. Read [Policy Persistence and Restart Behavior](../common/security.md#policy-persistence-and-restart-behavior) before editing the file or restarting the service.

For this component in Docker Compose, mount the security files into the container and configure `ABAC_ENABLED=true`, `ABAC_MODELPATH`, and `OIDC_TRUSTLISTPATH` if you enable ABAC.

## Using BaSyx Go Components without Docker
If you need to run the Basic Discovery component without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker Images for production use-cases, as they are pre-configured and optimized for production environments.
```

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
