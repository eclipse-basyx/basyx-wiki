# Setting Up the Submodel Repository
We provide example Set-Ups to get you started with the new BaSyx Go Components on our [GitHub Repository](https://github.com/eclipse-basyx/basyx-go-components).
But if you need to configure the service yourself, this page will guide you through.

## Using Docker Compose
The easiest way to use and set-up the Submodel Repository, is by using Docker Compose.

The minimal configuration includes two services:
1. PostgreSQL (>=15)
2. BaSyx Submodel Repository (Go)

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres_basyx
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: basyx
    command: ["postgres", "-c", "listen_addresses=*"]
    ports:
      - "6432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d basyx"]
      interval: 10s
      timeout: 5s
      retries: 5
  submodel_repository_it:
    image: eclipsebasyx/submodelrepository-go      
    environment:
      - SERVER_PORT=5004
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyx
      - POSTGRES_MAXOPENCONNECTIONS=500
      - POSTGRES_MAXIDLECONNECTIONS=500
      - POSTGRES_CONNMAXLIFETIMEMINUTES=5
    ports:
      - "5004:5004"
    depends_on:
      postgres:
        condition: service_healthy
```
*docker-compose.yml including PostgreSQL 18 and BaSyx Go Submodel Repository Snapshot*

If you need advanced configuration options, please refer to the [Configuration](configuration) section.
