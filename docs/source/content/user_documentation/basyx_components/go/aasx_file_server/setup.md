# Setting Up the AASX File Server

The following local setup runs the AASX File Server with PostgreSQL and the BaSyx Configuration Service.

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

Use matching BaSyx versions for the Configuration Service and every database-backed BaSyx component sharing this database.

```{warning}
This local example uses demonstration credentials, disables access control, and does not define a persistent PostgreSQL volume. Recreating the database container can therefore make stored packages unavailable. Do not expose this setup to an untrusted network or use it unchanged for persistent data. See [Persistent State](../common/deployment.md#persistent-state) before configuring a durable deployment.
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
| `POSTGRES_MAXOPENCONNECTIONS` | Maximum writer-pool connections. Default: `50`; SSP-002 requires at least `2`. |
| `POSTGRES_READER_HOST`, `POSTGRES_READER_PORT`, `POSTGRES_READER_USER`, `POSTGRES_READER_PASSWORD`, `POSTGRES_READER_DBNAME` | Optional read-replica connection. |
| `GENERAL_UPLOADMAXSIZEBYTES` | Maximum uploaded file content size. Default: `134217728` (128 MiB). |
| `GENERAL_AASXMAXPARTCOUNT` | Maximum package part count. Default: `10000`. |
| `GENERAL_AASXMAXOPCMETADATASIZEBYTES` | Maximum expanded OPC metadata size. Default: `16777216` (16 MiB). |
| `GENERAL_AASXMAXPARTEXPANDEDSIZEBYTES` | Maximum expanded size of one part. Default: `134217728` (128 MiB). |
| `GENERAL_AASXMAXTOTALEXPANDEDSIZEBYTES` | Maximum total expanded package size. Default: `536870912` (512 MiB). |
| `GENERAL_AASXMAXTHUMBNAILSIZEBYTES` | Maximum expanded thumbnail size. Default: `16777216` (16 MiB). |

Omit the complete `postgres.reader` configuration to reuse the writer connection for reads. When a replica is configured, list and download operations may briefly be eventually consistent after an upload or replacement.

### Asynchronous Upload Profile

Asynchronous package processing requires at least two writer-pool connections. Setting `POSTGRES_MAXOPENCONNECTIONS=1` disables SSP-002 and leaves only the synchronous SSP-001 routes. Check `GET /description` for the SSP-002 profile before using `/packages-async`. The default writer-pool configuration in this example provides sufficient capacity.

The service limits concurrent asynchronous work. When no execution slot is available, `POST /packages-async` returns `429 Too Many Requests`. Retry the submission later.

### Secured Setup

The Compose example is unsecured. The File Server supports OIDC authentication, ABAC authorization, and experimental [ReBAC](../common/rebac). To enable ABAC, set `ABAC_ENABLED=true`, mount an access-rule model and OIDC trust list, and configure their container paths. The effective default policy import mode is `if_missing`. See the [`oidc` and `abac`](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files) sections for setup details.

When ABAC/OIDC security is enabled, every `/packages-async` submission, status request, and result request requires an authenticated caller. Use the same bearer-token identity throughout the workflow because operation handles are scoped to their owner. With access control disabled as in this local example, the asynchronous routes accept anonymous requests.

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
