# Setting Up the Digital Twin Registry

Example deployments are available in the BaSyx Go Components [examples directory](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples). This page provides a small standalone setup and the requirements for building from source.

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

*`docker-compose.yml` for local evaluation with PostgreSQL 18, the BaSyx Configuration Service, and the Digital Twin Registry*

With no `BASYX_VERSION` value, this quick start uses `latest`, which can change to a different image digest at any time. For a reproducible deployment, set the same `BASYX_VERSION` in a `.env` file to a concrete release tag or commit-specific tag:

```text
BASYX_VERSION=<release-or-commit-specific-tag>
```

Alternatively, replace each complete `image` reference with an image digest. Use the same BaSyx version or build revision for every database-backed BaSyx service in the deployment, especially the Configuration Service. `latest` tracks the newest release and `SNAPSHOT` tracks the current main-branch snapshot; neither mutable tag guarantees repeatable or mutually compatible pulls over time. See [Version Scope](../common/deployment.md#version-scope).

### Start and Check the Service

Save the example as `docker-compose.yml`, then run:

```bash
docker compose up -d
docker compose ps -a
docker compose logs basyx_configuration digital_twin_registry
curl -i http://localhost:5004/health
```

The Configuration Service runs once and exits with code `0`. The DTR starts after successful database initialization. Once it is listening, the health endpoint returns `200 OK` and `{"status":"UP"}`; retry if startup is still in progress.

In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:5004/swagger) to inspect the API. Include any configured `server.contextPath` in health, Swagger, and API URLs.

The example has no named PostgreSQL volume. Add a named volume that matches the selected PostgreSQL image before creating data that must survive container replacement; adding a volume later does not migrate data from an existing anonymous volume.

For a secured example with Keycloak, see [`examples/BaSyxDigitalTwinRegistryExample`](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxDigitalTwinRegistryExample). Before enabling custom `Edc-Bpn` header injection, read [AssetLink Visibility and `Edc-Bpn`](index.md#assetlink-visibility-and-edc-bpn).

### Production Deployment Requirements

Published container images are the normal deployment artifacts, but the default Compose setup is not a production configuration. A production deployment should use:

- a concrete BaSyx release/commit tag or image digest
- persistent PostgreSQL storage and tested backup/restore procedures
- unique database credentials stored as secrets, with database transport security where required
- authentication and authorization appropriate to the deployment
- TLS at the service or a trusted ingress/reverse proxy
- network controls that prevent bypassing any trusted identity-header gateway

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
