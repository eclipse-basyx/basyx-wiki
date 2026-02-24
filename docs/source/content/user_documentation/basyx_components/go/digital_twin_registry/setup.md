# Setting Up the Digital Twin Registry
We provide example Set-Ups to get you started with the BaSyx Go Components on our [GitHub Repository](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples).
But if you need to configure the service yourself, this page will guide you through.

## Using Docker Compose
The easiest way to use and set-up the Digital Twin Registry is Docker Compose.

The minimal configuration includes two services:
1. PostgreSQL (>=15)
2. BaSyx Digital Twin Registry (Go)

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

  digital_twin_registry:
    image: eclipsebasyx/digitaltwinregistry-go:SNAPSHOT
    environment:
      - SERVER_PORT=5004
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
      - ABAC_ENABLED=false
    ports:
      - "YOURPORT:5004"
    depends_on:
      postgres:
        condition: service_healthy
```
*docker-compose.yml including PostgreSQL 18 and BaSyx Go Digital Twin Registry*

For a secured setup example (including Keycloak), see `examples/BaSyxDigitalTwinRegistryExample`.

### Access Rules and Trustlist Files (Secured Setup)

For general handling of OIDC trustlist and ABAC access-rules files (config keys, env vars, startup behavior), see [Security Configuration Files (Common)](../common/configuration#security-files-oidc-trustlist-and-abac-access-rules).

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
- [Go (>=1.20; 1.25 recommended)](https://golang.org/dl/)
- [Git](https://git-scm.com/)

### Cloning the Repository
```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
```

### Building the Binary
```bash
cd basyx-go-components/cmd/digitaltwinregistryservice
go build -o digitaltwinregistryservice
```

### Running the Service
Before running the service, ensure PostgreSQL is available and configure the connection via environment variables or a `config.yaml`.

```bash
./digitaltwinregistryservice -config ./config.yaml -databaseSchema ../../basyxschema.sql
```
