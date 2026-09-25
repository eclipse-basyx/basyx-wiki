# Setting Up the AAS Repository
We provide example setups to get you started with the BaSyx Go Components in the [example directory](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

The Docker quick-start uses `latest`, which tracks the newest stable BaSyx Go release. `SNAPSHOT` tracks unreleased development from `main`. For reproducible deployments, pin matching concrete release tags or image digests instead of relying on a mutable tag. See [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to use and set up the AAS Repository is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx AAS Repository (Go)

```{warning}
This Compose file is for local evaluation and development. It uses demonstration database credentials, disables ABAC, uses mutable image tags, exposes HTTP without TLS, and has no named PostgreSQL volume. Do not expose it to an untrusted network or use it unchanged for production.
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

  aas_repository:
    container_name: aas_repository
    image: eclipsebasyx/aasrepository-go:latest
    pull_policy: always
    environment:
      - SERVER_PORT=8084
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8084:8084"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go AAS Repository*

The Configuration Service and every database-backed BaSyx component sharing this database must come from matching release or build artifacts. Using `latest` consistently is suitable for this quick-start, but it is not immutable: later pulls can resolve to different digests. For reproducible deployments, use the same concrete release version across the BaSyx images or pin matching image digests.

### Start and Check the Repository

This minimal local Compose file does not declare a named PostgreSQL volume. Add a correctly mounted named volume before storing data that must survive container replacement; adding one later does not migrate data from an existing anonymous volume.

Save the example as `docker-compose.yml`, then run:

```bash
docker compose up -d
```

The Configuration Service is a one-time initialization/migration job. An exit code of `0` is expected. The Repository starts only after that job completes successfully.

Once the Repository is ready, check its health:

```bash
curl -i http://localhost:8084/health
```
Expect HTTP `200` with `{"status":"UP"}`. Open [Swagger UI](http://localhost:8084/swagger) to explore the API. To help you with the first steps using the repository, follow [Using the AAS Repository](usage).

Include any configured context path in every URL. For example, `SERVER_CONTEXTPATH=/api/v3` makes the health URL `http://localhost:8084/api/v3/health` and Swagger URL `http://localhost:8084/api/v3/swagger`.

### Access Rules and Trustlist Files (Secured Setup)

The local Compose example does not enable ABAC and is not a secured deployment. For this component, enable the supported authorization with `ABAC_ENABLED=true`, mount the access-rule and OIDC trust-list files, and configure their container paths. When `ABAC_POLICY_FILE_IMPORT` is omitted, the effective import mode is `if_missing`, so editing a mounted policy file and restarting does not replace an active policy already stored in PostgreSQL. See [OIDC and ABAC Configuration](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files) before exposing the service.

## Using BaSyx Go Components without Docker
If you need to run the AAS Repository without Docker, build the binary from source for your target platform.

Published container images are the normal deployment artifacts. Production deployments must configure appropriate authentication and authorization, persistent database storage, secure credentials, networking and TLS, backups, and reproducible image versions where required. A native binary can be deployed with the same operational controls.

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

Replace `RELEASE_TAG` with the stable release you intend to build. Initialize PostgreSQL with the Configuration Service and SQL assets from this same checkout.

### Building the Binary

Change to the AAS Repository service directory:
```bash
cd basyx-go-components/cmd/aasrepositoryservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o aasrepositoryservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o aasrepositoryservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

The provided native `config.yaml` listens on port `5004` unless `server.port` is overridden. The Compose example overrides this with `SERVER_PORT=8084`, so its URLs use port `8084`.

#### Linux / macOS

Run the service with:
```bash
./aasrepositoryservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\aasrepositoryservice.exe -config .\config.yaml
```

The AAS Repository does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.

The Compose example uses port `8084` so it can run alongside the Submodel Repository on `8085`. The two setup files describe independent Compose projects. If using both simultaneously, use distinct container names and host ports. For shared-database access through both Repository APIs, combine them into one Compose project with one PostgreSQL service and one Configuration Service, and configure both Repositories for that database.
