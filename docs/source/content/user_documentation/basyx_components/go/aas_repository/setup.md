# Setting Up the AAS Repository
We provide example setups to get you started with the BaSyx Go Components on our [GitHub Repository](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

## Using Docker Compose
The easiest way to use and set up the AAS Repository is Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL
2. BaSyx Configuration Service (Go), which initializes the database
3. BaSyx AAS Repository (Go)

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

  aas_repository:
    container_name: aas_repository
    image: eclipsebasyx/aasrepository-go:1.0.11
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

Use the same BaSyx release for every service sharing this database, including the Configuration Service, here `1.0.11`.

### Start and Check the Repository

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

For general handling of OIDC trustlist and ABAC access-rules files (config keys, env vars, startup behavior), see [Security Configuration Files (Common)](../common/configuration#security-files).

For this component in Docker Compose, mount the security files into the container and configure `ABAC_ENABLED=true`, `ABAC_MODELPATH`, and `OIDC_TRUSTLISTPATH` if you enable ABAC.

## Using BaSyx Go Components without Docker
If you need to run the AAS Repository without Docker, build the binary from source for your target platform.

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
```

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
