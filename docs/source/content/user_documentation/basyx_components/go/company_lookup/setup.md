# Setting Up the Company Lookup

We provide example set-ups to get you started with the BaSyx Go Components in our [GitHub repository](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxCompanyLookup).
If you need to configure the service yourself, this page will guide you through the process.

## Using Docker Compose

The easiest way to set up the Company Lookup is with Docker Compose.

The minimal configuration includes three services:

1. PostgreSQL (>=15)
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
    image: eclipsebasyx/basyxconfigurationservice-go:SNAPSHOT
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxCompanyLookupDB
      - POSTGRES_MAXOPENCONNECTIONS=500
      - POSTGRES_MAXIDLECONNECTIONS=500
      - POSTGRES_CONNMAXLIFETIMEMINUTES=5
    depends_on:
      postgres:
        condition: service_healthy

  company-lookup:
    container_name: company-lookup
    image: eclipsebasyx/companylookup-go:SNAPSHOT
    ports:
      - 5080:5080
    environment:
      - SERVER_PORT=5080
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxCompanyLookupDB
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```

*docker-compose.yml including PostgreSQL 18, the BaSyx Configuration Service, and the BaSyx Go Company Lookup*

Replace `YOURPORT` with the port on which the Company Lookup should be available on the host, for example `5080`.

If you need advanced configuration options, see [General Configuration](../common/configuration).

## Using BaSyx Go Components without Docker

If you need to run the Company Lookup without Docker, build the binary from source for your target platform.

```{warning}
We recommend using the Docker images for production use cases, as they are preconfigured and optimized for production environments.
```

### Prerequisites

- [Go (>=1.20; 1.25 recommended)](https://golang.org/dl/)
- [Git](https://git-scm.com/)
- [PostgreSQL (>=15)](https://www.postgresql.org/)

### Cloning the Repository

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
```

### Building the Binary

Navigate to the Company Lookup command directory and build the binary:

```bash
cd basyx-go-components/cmd/companylookupservice
go build -o companylookupservice
```

### Running the Service

Before running the service, ensure PostgreSQL is available and configure the connection through environment variables or a `config.yaml`. 

```bash
./companylookupservice -config ./config.yaml -databaseSchema ../../basyxschema.sql
```
