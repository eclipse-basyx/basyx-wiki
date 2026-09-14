# Setting Up the Digital Twin Registry
We provide example setups to get you started with the BaSyx Go Components on our [GitHub Repository](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

## Using Docker Compose
The easiest way to use and set up the Digital Twin Registry is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx Digital Twin Registry (Go)

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

  digital_twin_registry:
    container_name: digital_twin_registry
    image: eclipsebasyx/digitaltwinregistry-go:1.0.11
    pull_policy: always
    environment:
      - SERVER_PORT=5004
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
      - ABAC_ENABLED=false
    ports:
      - "5004:5004"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Digital Twin Registry*

Use the same BaSyx release for every service sharing this database, including the Configuration Service. These Compose examples select `1.0.11`; avoid mixing them with `SNAPSHOT` images. See [Version Scope](../common/registry_integration.md#version-scope) for the implementation revision used to check the usage guides.

### Start and Check the Service

Save the example as `docker-compose.yml`, then run these commands in the same directory:

```bash
docker compose up -d
docker compose ps -a
docker compose logs basyx_configuration digital_twin_registry
curl -i http://localhost:5004/health
```

The Configuration Service runs once and exits with code `0`. The HTTP service starts after successful initialization. Once it is listening, expect `200 OK` and `{"status":"UP"}` from the health endpoint; retry if startup is still in progress.

In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:5004/swagger) to inspect the API. Include any configured `server.contextPath` in health, Swagger, and API URLs.

For a secured setup example (including Keycloak), see `examples/BaSyxDigitalTwinRegistryExample`.

### Access Rules and Trustlist Files (Secured Setup)

For general handling of OIDC trustlist and ABAC access-rules files (config keys, env vars, startup behavior), see [Security Configuration Files (Common)](../common/configuration.md#security-files).

For the Digital Twin Registry specifically, these paths are resolved inside the container. In Docker Compose, mount the files (or a folder containing them) into the container and point the environment variables to the mounted paths.

Example:
```yaml
services:
  digital_twin_registry:
    volumes:
      - ./security_env:/security_env:ro
    environment:
      - ABAC_ENABLED=true
      - ABAC_MODELPATH=/security_env/access-rules.json
      - OIDC_TRUSTLISTPATH=/security_env/trustlist.json
```

If `ABAC_ENABLED=false`, the Digital Twin Registry does not require these files at startup.

## Using BaSyx Go Components without Docker
If you need to run the Digital Twin Registry without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker Images for production use-cases, as they are pre-configured and optimized for production environments.
```

### Prerequisites
- [Go](https://go.dev/dl/) `1.27.1` or newer, as specified in the pinned revision's [`go.mod`](https://github.com/eclipse-basyx/basyx-go-components/blob/20e102a9bccad077f6a1b0ff7897c8a06f1e34ee/go.mod).
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout 20e102a9bccad077f6a1b0ff7897c8a06f1e34ee
```

### Building the Binary

Change to the Digital Twin Registry service directory:
```bash
cd basyx-go-components/cmd/digitaltwinregistryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o digitaltwinregistryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o digitaltwinregistryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

#### Linux / macOS

Run the service with:
```bash
./digitaltwinregistryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\digitaltwinregistryservice.exe -config .\config.yaml
```

The Digital Twin Registry does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
