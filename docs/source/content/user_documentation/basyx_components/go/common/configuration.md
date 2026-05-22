# General Configuration

BaSyx Go components use a shared configuration model from `internal/common`. Configuration can be provided through a YAML file and overridden with environment variables.

## Configuration Source Precedence

The shared configuration loader applies the following precedence:

1. Environment variables
2. YAML configuration file
3. Built-in defaults

Environment variables override YAML values. Nested keys use underscore notation, for example `server.port` becomes `SERVER_PORT`.

## Common Configuration Sections

These sections are part of the shared configuration model. Components ignore settings that are not relevant to their feature set.

### `server`

| Key | Default | Purpose |
| --- | --- | --- |
| `host` | `0.0.0.0` | Host used for the HTTP server and generated Swagger server URL. |
| `port` | `5004` | HTTP server port. |
| `contextPath` | `""` | Base path for API, Swagger, and health endpoints. |
| `cacheEnabled` | `false` | Enables descriptor persistence caches where supported. |
| `strictVerification` | `permissive` | Semantic verification mode: `off`, `permissive`, or `strict`. |
| `verificationEndpointAvailable` | `true` | Enables the `/verify` endpoint and Swagger entry where supported. |

### `postgres`

| Key | Default | Purpose |
| --- | --- | --- |
| `host` | `db` | PostgreSQL host. |
| `port` | `5432` | PostgreSQL port. |
| `user` | `admin` | Database user. |
| `password` | `admin123` | Database password. |
| `dbname` | `basyxTestDB` | Database name. |
| `maxOpenConnections` | `50` | Maximum number of open DB connections. |
| `maxIdleConnections` | `50` | Maximum number of idle DB connections. |
| `connMaxLifetimeMinutes` | `5` | Maximum DB connection lifetime in minutes. |

### `cors`

| Key | Default | Purpose |
| --- | --- | --- |
| `allowedOrigins` | `[]` | Allowed CORS origins. |
| `allowedMethods` | `[GET, POST, PUT, PATCH, DELETE, OPTIONS]` | Allowed HTTP methods. |
| `allowedHeaders` | `[]` | Allowed request headers. |
| `allowCredentials` | `false` | Enables credentialed CORS requests. |

### `oidc` and `abac`

| Key | Default | Purpose |
| --- | --- | --- |
| `oidc.trustlistPath` | `config/trustlist.json` | JSON trustlist of accepted OIDC providers. |
| `abac.enabled` | `false` | Enables OIDC authentication and ABAC authorization middleware. |
| `abac.modelPath` | `config/access_rules/access-rules.json` | ABAC access-rules model. |

If `abac.enabled` is `false`, the shared security setup is skipped. If it is `true`, the trustlist is required and the ABAC model is loaded when `abac.modelPath` is set.

### `general`

| Key | Default | Purpose |
| --- | --- | --- |
| `enableImplicitCasts` | `true` | Allows implicit casts in ABAC/query expression evaluation. |
| `enableDescriptorDebug` | `false` | Enables descriptor query debug output. |
| `discoveryIntegration` | `false` | Enables discovery-specific descriptor behavior; some services set this internally. |
| `enableCustomMiddlewareHeaderInjection` | `false` | Enables custom claim/header middleware where supported. |
| `supportsSingularSupplementalSemanticId` | `false` | Accepts singular `supplementalSemanticId` compatibility format. |
| `aasRegistryIntegration` | `false` | Enables AAS repository to AAS registry synchronization. |
| `submodelRegistryIntegration` | `false` | Enables Submodel repository to Submodel registry synchronization. |
| `externalUrl` | `""` | Public base URL used to generate synchronized registry endpoint descriptors. Multiple URLs can be comma-separated. |
| `uploadMaxSizeBytes` | `134217728` | Maximum upload size for repository/environment upload endpoints. |
| `aasPreconfigPaths` | `[]` | AAS Environment startup import sources. Supports files or folders with `.aasx`, `.json`, or `.xml` files. |

When registry synchronization is enabled, `general.externalUrl` must be set to at least one absolute URL with scheme and host.

### `jws` and `swagger`

| Key | Default | Purpose |
| --- | --- | --- |
| `jws.privateKeyPath` | `""` | RSA private key used by Submodel Repository and AAS Environment signing use cases. |
| `swagger.contactName` | `Eclipse BaSyx` | Contact name injected into OpenAPI/Swagger docs. |
| `swagger.contactEmail` | `basyx-dev@eclipse.org` | Contact email injected into OpenAPI/Swagger docs. |
| `swagger.contactUrl` | `https://basyx.org` | Contact URL injected into OpenAPI/Swagger docs. |

## Example YAML

```yaml
server:
  host: 0.0.0.0
  port: 5004
  contextPath: ""
  cacheEnabled: false
  strictVerification: permissive
  verificationEndpointAvailable: true

postgres:
  host: db
  port: 5432
  dbname: basyxTestDB
  user: admin
  password: admin123
  maxOpenConnections: 50
  maxIdleConnections: 50
  connMaxLifetimeMinutes: 5

cors:
  allowedOrigins: []
  allowedMethods: [GET, POST, PUT, PATCH, DELETE, OPTIONS]
  allowedHeaders: []
  allowCredentials: false

oidc:
  trustlistPath: "config/trustlist.json"

abac:
  enabled: false
  modelPath: "config/access_rules/access-rules.json"

general:
  enableImplicitCasts: true
  enableDescriptorDebug: false
  discoveryIntegration: false
  enableCustomMiddlewareHeaderInjection: false
  supportsSingularSupplementalSemanticId: false
  aasRegistryIntegration: false
  submodelRegistryIntegration: false
  externalUrl: ""
  uploadMaxSizeBytes: 134217728
  aasPreconfigPaths: []

jws:
  privateKeyPath: ""

swagger:
  contactName: "Eclipse BaSyx"
  contactEmail: "basyx-dev@eclipse.org"
  contactUrl: "https://basyx.org"
```

## Environment Variables

Use uppercase names with underscores:

```bash
SERVER_PORT=5004
SERVER_CONTEXTPATH=/api
SERVER_STRICTVERIFICATION=permissive
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DBNAME=basyxTestDB
ABAC_ENABLED=false
OIDC_TRUSTLISTPATH=config/trustlist.json
GENERAL_EXTERNALURL=https://example.org/aas
GENERAL_UPLOADMAXSIZEBYTES=134217728
```

`GENERAL_AAS_PRECONFIG_PATHS` is parsed as a comma-separated list and overrides `general.aasPreconfigPaths`:

```bash
GENERAL_AAS_PRECONFIG_PATHS=file:/data/example.aasx,/data/preconfigured-aas
```

## Security Files

Components that use shared OIDC/ABAC security may rely on these paths:

- `oidc.trustlistPath`
- `abac.modelPath`

In containers, paths are resolved inside the container filesystem. Mount the files or their parent directory and point the YAML value or environment variable to the mounted path.

## Notes

- The BaSyx Configuration Service mainly uses the `postgres` section.
- Repository and environment services use `general.uploadMaxSizeBytes` for upload limits.
- AAS Environment additionally supports `general.aasPreconfigPaths`.
- AAS Repository, Submodel Repository, and AAS Environment use the registry synchronization settings when enabled.
