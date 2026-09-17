# Setting Up the AASX File Server

The Docker example uses `latest` for both BaSyx Go images. For native builds, use one stable source release and its matching database assets as described in [Version Scope](../common/deployment.md#version-scope).

## Using Docker Compose

The minimal setup contains PostgreSQL, the one-time BaSyx Configuration Service database initializer, and the AASX File Server:

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres_basyx_aasx
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
    container_name: basyx_configuration_aasx
    image: eclipsebasyx/basyxconfigurationservice-go:latest
    pull_policy: always
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    depends_on:
      postgres:
        condition: service_healthy

  aasx_file_server:
    container_name: aasx_file_server
    image: eclipsebasyx/aasxfileserver-go:latest
    pull_policy: always
    environment:
      - SERVER_PORT=8087
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DBNAME=basyxTestDB
    ports:
      - "8087:8087"
    depends_on:
      basyx_configuration:
        condition: service_completed_successfully
```

Use the same image tag for every BaSyx Go service sharing this database.

```{warning}
This minimal example has no named PostgreSQL volume. Add and correctly mount one before storing packages that must survive container recreation. Backups and migrations must include PostgreSQL Large Objects because that is where the package bytes are stored. See [Persistent State](../common/deployment.md#persistent-state).
```

Save the example as `docker-compose.yml`, then start it:

```bash
docker compose up -d
curl -i http://localhost:8087/health
```

The Configuration Service is expected to exit with code `0`. A ready File Server returns HTTP `200` with `{"status":"UP"}`. Swagger UI is available at [http://localhost:8087/swagger](http://localhost:8087/swagger).

## Configuration File

The image contains a configuration file at `/config/config.yaml`. This representative configuration uses the Compose database and shows the release's package limits:

```yaml
server:
  port: 8087
  contextPath: ""
  host: 0.0.0.0

postgres:
  host: postgres
  port: 5432
  user: admin
  password: admin123
  dbname: basyxTestDB
  maxOpenConnections: 50
  maxIdleConnections: 25
  connMaxLifetimeMinutes: 5
  connMaxIdleTimeMinutes: 0

general:
  uploadMaxSizeBytes: 134217728
  aasxMaxPartCount: 10000
  aasxMaxOPCMetadataSizeBytes: 16777216
  aasxMaxPartExpandedSizeBytes: 134217728
  aasxMaxTotalExpandedSizeBytes: 536870912
  aasxMaxThumbnailSizeBytes: 16777216
```

Do not combine `postgres.dsn` with the individual connection fields. See [General Configuration](../common/configuration) for the complete shared model and mounting guidance.

### Environment Variables

| Environment variable | Purpose |
| --- | --- |
| `SERVER_PORT` | HTTP listen port. The checked-in default is `5004`; this example uses `8087`. |
| `SERVER_CONTEXTPATH` | Optional prefix for every service route. |
| `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DBNAME` | Writer database connection. |
| `POSTGRES_DSN` | Alternative complete writer connection string. Do not mix it with the individual connection fields. |
| `POSTGRES_READER_HOST`, `POSTGRES_READER_PORT`, `POSTGRES_READER_USER`, `POSTGRES_READER_PASSWORD`, `POSTGRES_READER_DBNAME` | Optional read-replica connection. |
| `GENERAL_UPLOADMAXSIZEBYTES` | Maximum compressed HTTP upload size. Default: `134217728` (128 MiB). |
| `GENERAL_AASXMAXPARTCOUNT` | Maximum package part count. Default: `10000`. |
| `GENERAL_AASXMAXOPCMETADATASIZEBYTES` | Maximum expanded OPC metadata size. Default: `16777216` (16 MiB). |
| `GENERAL_AASXMAXPARTEXPANDEDSIZEBYTES` | Maximum expanded size of one part. Default: `134217728` (128 MiB). |
| `GENERAL_AASXMAXTOTALEXPANDEDSIZEBYTES` | Maximum total expanded package size. Default: `536870912` (512 MiB). |
| `GENERAL_AASXMAXTHUMBNAILSIZEBYTES` | Maximum expanded thumbnail size. Default: `16777216` (16 MiB). |
| `ABAC_ENABLED`, `ABAC_MODELPATH`, `ABAC_POLICY_FILE_IMPORT` | Enable ABAC and configure its policy source/import behavior. |
| `OIDC_TRUSTLISTPATH` | Path to the mounted OIDC trust list. |

Omit the complete `postgres.reader` configuration to reuse the writer connection for reads. When a replica is configured, list and download operations may briefly be eventually consistent after an upload or replacement.

### Secured Setup

The Compose example is unsecured. The File Server supports the common OIDC and ABAC middleware. Set `ABAC_ENABLED=true`, mount an access-rule model and OIDC trust list, and set their container paths. The effective default policy import mode is `if_missing`; consult [Runtime Security](../common/security) before operating a secured deployment.

## Running without Docker

Use PostgreSQL initialized by a Configuration Service from the same release, then build the service from the release checkout:

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
git -C basyx-go-components checkout RELEASE_TAG
cd basyx-go-components/cmd/aasxfileserverservice
go build -o aasxfileserver
./aasxfileserver -config ./config.yaml
```

Replace `RELEASE_TAG` with the stable release you intend to build, and use the Configuration Service and SQL assets from that same checkout.

On Windows, build `aasxfileserver.exe` and run `./aasxfileserver.exe -config ./config.yaml` in PowerShell. The File Server validates the initialized database schema and does not create it itself.
