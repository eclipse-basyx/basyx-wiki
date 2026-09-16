# Setting Up the Digital Twin Registry
We provide example setups to get you started with the BaSyx Go Components in the [release 1.0.11 examples](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.0.11/examples).
But if you need to configure the service yourself, this page will guide you through.

The Docker and native examples on this page target BaSyx Go application release `1.0.11`. Keep all BaSyx services, source assets, and database initialization at that release; see [Version Scope](../common/deployment.md#version-scope).

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
      - GENERAL_ENABLECUSTOMMIDDLEWAREHEADERINJECTION=false
    ports:
      - "5004:5004"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Digital Twin Registry*

Use the same BaSyx release for every service sharing this database, including the Configuration Service. These Compose examples select `1.0.11`; avoid mixing them with `SNAPSHOT` images.

### Start and Check the Service

This minimal example does not declare a named PostgreSQL volume. Container recreation can therefore leave a new database container attached to different storage and make existing data appear lost. Add the [version-correct named volume](../common/deployment.md#persistent-state) before creating data when persistence is required; adding one later does not migrate data from an existing anonymous volume.

Save the example as `docker-compose.yml`, then run these commands in the same directory:

```bash
docker compose up -d
docker compose ps -a
docker compose logs basyx_configuration digital_twin_registry
curl -i http://localhost:5004/health
```

The Configuration Service runs once and exits with code `0`. The HTTP service starts after successful initialization. Once it is listening, expect `200 OK` and `{"status":"UP"}` from the health endpoint; retry if startup is still in progress.

In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:5004/swagger) to inspect the API. Include any configured `server.contextPath` in health, Swagger, and API URLs.

For a secured setup example (including Keycloak), see [`examples/BaSyxDigitalTwinRegistryExample`](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.0.11/examples/BaSyxDigitalTwinRegistryExample). Before enabling custom `Edc-Bpn` header injection, read the [Edc-Bpn Trust Boundary](index.md#edc-bpn-trust-boundary); an ordinary deployment must not trust a caller-supplied identity header.

### Access Rules and Trustlist Files (Secured Setup)

The local Compose example is unsecured: `ABAC_ENABLED=false`, and custom header injection is explicitly disabled. Security-related settings or mounted files do not secure the service unless the OIDC/ABAC middleware is enabled and configured with a matching policy. Follow [Runtime Security](../common/security) for the complete workflow and [Security Configuration Files](../common/configuration.md#security-files) for the field reference.

For DTR, an omitted `abac.policyFileImport` defaults to `always`: the access-rules file is imported on every startup and supersedes the active database policy. Read [Policy Persistence and Restart Behavior](../common/security.md#policy-persistence-and-restart-behavior) before editing the file or restarting the service.

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
- [Go](https://go.dev/dl/) `1.27.0` or a compatible newer toolchain, as specified in release 1.0.11's [`go.mod`](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/go.mod).
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components.git
git -C basyx-go-components checkout v1.0.11
git -C basyx-go-components rev-parse HEAD
```

The final command must print `81324eb3aad9d63baea93d3385bc9ca7e6a6a05a`. The tag is [release `v1.0.11`](https://github.com/eclipse-basyx/basyx-go-components/releases/tag/v1.0.11), and the expected revision is the [pinned commit](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a).

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
