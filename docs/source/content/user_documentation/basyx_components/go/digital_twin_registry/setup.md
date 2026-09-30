# Setting Up the Digital Twin Registry

Example deployments are available in the BaSyx Go Components [examples directory](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.0/examples). This page provides a small standalone setup and the requirements for building from source.

## Using Docker Compose

The minimal setup contains PostgreSQL, the BaSyx Configuration Service that initializes the database, and the Digital Twin Registry.

```{warning}
The Compose file below is for local evaluation and development. It uses demo database credentials, disables ABAC, publishes the API without TLS, has no named PostgreSQL volume, and defaults to the mutable `latest` BaSyx image tag. Do not expose it to an untrusted network or use it unchanged for production.
```

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
    image: eclipsebasyx/basyxconfigurationservice-go:${BASYX_VERSION:-latest}
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
    image: eclipsebasyx/digitaltwinregistry-go:${BASYX_VERSION:-latest}
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

*docker-compose.yml including PostgreSQL 18, the BaSyx Go Configuration Service, and the Digital Twin Registry*

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
curl -i http://localhost:5004/health
```

Expect HTTP `200` with `{"status":"UP"}`. Open [Swagger UI](http://localhost:5004/swagger) to explore the API. To help you with the first steps using the registry, follow TODO TODO TODO to TODO TODO TODO.

The Compose example explicitly selects port `5004`. When using a context path, include it in health, Swagger, and API URLS. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:5004/api/v3/health`.

For a secured example with Keycloak, see [`examples/BaSyxDigitalTwinRegistryExample`](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.0/examples/BaSyxDigitalTwinRegistryExample). Before enabling custom `Edc-Bpn` header injection, read [AssetLink Visibility and `Edc-Bpn`](index.md#assetlink-visibility-and-edc-bpn).

### Access Rules and Trust-List Files

The local Compose example is unsecured: `ABAC_ENABLED=false`, and custom header injection is explicitly disabled. Mounted security files have no effect unless OIDC/ABAC is enabled and configured with a matching policy. See [OIDC and ABAC configuration](../common/configuration.md#oidc-and-abac) and [Security Configuration Files](../common/configuration.md#security-files).

For DTR, an omitted `abac.policyFileImport` uses `always`: the access-rules file is imported on every startup and supersedes the active database policy. Set `ABAC_POLICY_FILE_IMPORT` to `always`, `if_missing`, or `never` deliberately for the required policy lifecycle.

Paths are resolved inside the DTR container. Mount the files read-only and configure their container paths, for example:

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

If `ABAC_ENABLED=false`, the DTR does not require these files at startup.

## Using BaSyx Go Components without Docker

Build the binary from the same source revision as the Configuration Service and database assets. Published images are convenient deployment artifacts, but a correctly built native binary supports the same service behavior; production readiness depends on the surrounding security, persistence, networking, and operational configuration.

### Prerequisites

- [Go](https://go.dev/dl/) at the version declared by the selected release's `go.mod`
- PostgreSQL 16 or newer, initialized by a Configuration Service from the same source revision
- [Git](https://git-scm.com/)

### Clone the Repository

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components.git
git -C basyx-go-components checkout RELEASE_TAG
```

Replace `RELEASE_TAG` with the concrete release or commit you intend to build. Use the Configuration Service and SQL assets from this checkout.

### Build the Binary

Change to the DTR command directory:

```bash
cd basyx-go-components/cmd/digitaltwinregistryservice
```

On Linux or macOS:

```bash
go build -o digitaltwinregistryservice
```

On Windows PowerShell:

```powershell
go build -o digitaltwinregistryservice.exe
```

### Run the Service

Ensure PostgreSQL is available and the BaSyx database schema has been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or `config.yaml`.

On Linux or macOS:

```bash
./digitaltwinregistryservice -config ./config.yaml
```

On Windows PowerShell:

```powershell
.\digitaltwinregistryservice.exe -config .\config.yaml
```

The DTR does not initialize or migrate the database schema itself. Run the Configuration Service successfully before starting the DTR and whenever the selected BaSyx version requires a schema update.
