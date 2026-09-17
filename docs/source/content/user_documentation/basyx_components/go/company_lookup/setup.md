# Setting Up the Company Lookup
We provide example setups to get you started with the BaSyx Go Components in the [Company Lookup example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxCompanyLookup).
If you need to configure the service yourself, this page will guide you through the process.

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose
The easiest way to set up the Company Lookup is with Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx Company Lookup (Go)

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres_basyx_company_lookup
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: basyxCompanyLookupDB
    command: ["postgres", "-c", "listen_addresses=*"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d basyxCompanyLookupDB"]
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
      - POSTGRES_DBNAME=basyxCompanyLookupDB
      - POSTGRES_MAXOPENCONNECTIONS=50
      - POSTGRES_MAXIDLECONNECTIONS=25
      - POSTGRES_CONNMAXLIFETIMEMINUTES=5
      - POSTGRES_CONNMAXIDLETIMEMINUTES=0
    depends_on:
      postgres:
        condition: service_healthy

  company-lookup:
    container_name: company-lookup
    image: eclipsebasyx/companylookup-go:latest
    pull_policy: always
    ports:
      - 5080:5080
    environment:
      - SERVER_PORT=5080
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxCompanyLookupDB
      - POSTGRES_MAXOPENCONNECTIONS=50
      - POSTGRES_MAXIDLECONNECTIONS=25
      - POSTGRES_CONNMAXLIFETIMEMINUTES=5
      - POSTGRES_CONNMAXIDLETIMEMINUTES=0
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```
*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and BaSyx Go Company Lookup*

Use the same image tag for every BaSyx Go service sharing this database, including the Configuration Service.

### Start and Check the Service

```{warning}
The 1.0.11 Company Lookup executable does not install the shared OIDC/ABAC middleware. Common `oidc.*` or `abac.*` settings do not secure it. Put required access control at a trusted deployment boundary and prevent direct bypass; read [Security Limitations in 1.0.11](index.md#security-limitations-in-1011) before exposing this service.
```

This minimal local Compose file also does not declare a named PostgreSQL volume. An image-created anonymous volume is not automatically reused after `docker compose down`; container recreation can therefore make the database appear empty. Add a correctly mounted named volume before storing persistent data, and explicitly migrate any existing database rather than expecting a new volume declaration to copy it. See [Persistent State](../common/deployment.md#persistent-state).

Save the example as `docker-compose.yml`, then run these commands in the same directory:

```bash
docker compose up -d
docker compose ps -a
docker compose logs basyx_configuration company-lookup
curl -i http://localhost:5080/health
```

The Configuration Service runs once and exits with code `0`. The HTTP service starts after successful initialization. Once it is listening, expect `200 OK` and `{"status":"UP"}` from the health endpoint; retry if startup is still in progress.

In Windows PowerShell, use `curl.exe` instead of `curl`. Open [Swagger UI](http://localhost:5080/swagger) to inspect the API. Include any configured `server.contextPath` in health, Swagger, and API URLs.

If you need advanced configuration options, see [General Configuration](../common/configuration).

## Using BaSyx Go Components without Docker
If you need to run the Company Lookup without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker Images for production use-cases, as they are pre-configured and optimized for production environments.
```

### Prerequisites
- [Go](https://go.dev/dl/) at the version declared by the selected release's `go.mod`.
- PostgreSQL 16 or newer, initialized by a Configuration Service built from the same source revision as the HTTP service.
- [Git](https://git-scm.com/)

### Cloning the Repository
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout RELEASE_TAG
```

Replace `RELEASE_TAG` with the stable release you intend to build. Initialize PostgreSQL with the Configuration Service and SQL assets from this same checkout.

### Building the Binary

Change to the Company Lookup service directory:
```bash
cd basyx-go-components/cmd/companylookupservice
```

#### Linux / macOS

Build the executable with:
```bash
go build -o companylookupservice
```

#### Windows

Build the executable with the `.exe` extension:
```powershell
go build -o companylookupservice.exe
```

### Running the Service
Before running the service, ensure PostgreSQL is available and that the BaSyx database schema has already been initialized by the [BaSyx Configuration Service](../configuration_service/index). Configure the PostgreSQL connection through environment variables or the provided `config.yaml`.

#### Linux / macOS

Run the service with:
```bash
./companylookupservice -config ./config.yaml
```

#### Windows PowerShell

Run the service with:
```powershell
.\companylookupservice.exe -config .\config.yaml
```

The Company Lookup does not initialize the database schema itself. Database initialization and migrations are handled by the BaSyx Configuration Service.
