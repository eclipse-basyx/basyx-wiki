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
| `readHeaderTimeoutSeconds` | `15` | Maximum time in seconds to read HTTP request headers. |
| `readTimeoutSeconds` | `300` | Maximum time in seconds to read an entire HTTP request, including its body. |
| `writeTimeoutSeconds` | `300` | Maximum time in seconds to write an HTTP response. |
| `idleTimeoutSeconds` | `60` | Maximum time in seconds to wait for the next request on an idle keep-alive connection. |
| `shutdownTimeoutSeconds` | `10` | Maximum time in seconds to wait for in-flight requests during graceful shutdown. |

All HTTP timeout values must be greater than `0`. When a service receives an interrupt or termination signal, it stops accepting new connections and allows in-flight requests to finish for up to `shutdownTimeoutSeconds`.

### `postgres`

| Key | Default | Purpose |
| --- | --- | --- |
| `dsn` | `""` | Complete PostgreSQL connection string. When non-empty, it replaces the individual connection fields listed below. |
| `host` | `db` | PostgreSQL host. |
| `port` | `5432` | PostgreSQL port. |
| `user` | `admin` | Database user. |
| `password` | `admin123` | Database password. |
| `dbname` | `basyxTestDB` | Database name. |
| `sslmode` | `disable` | PostgreSQL TLS verification mode: `disable`, `allow`, `prefer`, `require`, `verify-ca`, or `verify-full`. |
| `sslcert` | `""` | Path to the client certificate used for certificate-based PostgreSQL authentication. |
| `sslkey` | `""` | Path to the private key belonging to `sslcert`. |
| `sslrootcert` | `""` | Path to the root CA certificate used to verify the PostgreSQL server certificate. |
| `connectTimeoutSeconds` | `0` | Connection timeout in seconds. Must not be negative; `0` leaves the timeout unspecified. |
| `applicationName` | `""` | PostgreSQL `application_name` reported for the connection. |
| `fallbackApplicationName` | `""` | Fallback application name used when no primary application name is supplied. |
| `searchPath` | `""` | PostgreSQL schema search path for new sessions. |
| `options` | `""` | Additional PostgreSQL server startup options. |
| `timezone` | `""` | PostgreSQL session time zone. |
| `maxOpenConnections` | `50` | Maximum number of open DB connections. |
| `maxIdleConnections` | `50` | Maximum number of idle DB connections. |
| `connMaxLifetimeMinutes` | `5` | Maximum DB connection lifetime in minutes. |

When `postgres.dsn` is non-empty, do not explicitly configure `host`, `port`, `user`, `password`, `dbname`, TLS, timeout, application-name, search-path, options, or time-zone fields in YAML or environment variables. The service rejects this ambiguous combination. Connection-pool settings can still be used with a DSN.

The DSN and database credentials are sensitive and should normally be supplied through a secret rather than committed to YAML.

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
| `abac.policyFileImport` | `""` | Controls startup import of `modelPath`: `always`, `if_missing`, or `never`. An empty value lets the service choose its default behavior. |
| `abac.policyScope` | `""` | Optional database namespace for stored ABAC policies. An empty value uses the service's built-in scope. |
| `abac.managementApi.enabled` | `false` | Enables the protected API for managing the active ABAC policy at runtime. |

If `abac.enabled` is `false`, the shared security setup is skipped. If it is `true`, the trustlist is required. `policyFileImport` determines whether the policy file is loaded on every start, only if the database has no active policy, or never. `policyScope` controls the database-backed ABAC policy namespace; use different scopes to isolate deployments that share a database, and share a scope only when services should intentionally use the same active policy.

When set, `policyScope` is trimmed, must not exceed 255 characters, and may contain ASCII letters, digits, `_`, `-`, `.`, and `:`.

#### OIDC trustlist provider fields

The source also defines the following provider fields for entries read from the JSON file at `oidc.trustlistPath`. They are not additional keys in the main YAML `oidc` section.

| Field | Purpose |
| --- | --- |
| `issuer` | OIDC issuer URL whose tokens are accepted. |
| `audience` | Optional required token audience. Audience validation is skipped when this is empty. |
| `scopes` | Scopes that an accepted token must provide. |
| `discoveryUrl` | Optional non-standard OpenID Provider discovery URL. |
| `scopeClaims` | Optional JSON pointers identifying claims from which OAuth scopes are read. |
| `claimMappings` | Optional rules that map provider-specific claims into canonical BaSyx claims. |

Each `claimMappings` entry contains:

| Field | Purpose |
| --- | --- |
| `target` | Target claim name without the `basyx.` prefix. The mapped claim is exposed as `basyx.<target>`. |
| `mode` | Mapping mode: `list` collects values as a list, while `scalar` produces a single value. |
| `sources` | Provider claim paths used as mapping inputs. |

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
| `trustProxyHeaders` | `false` | Allows trusted reverse proxies to supply the public request scheme, host, and client information through `Forwarded` or `X-Forwarded-*` headers. |
| `trustedProxyCIDRs` | `[]` | CIDR allowlist of proxy source addresses whose forwarded headers may be trusted. |
| `uploadMaxSizeBytes` | `134217728` | Maximum upload size for repository/environment upload endpoints. |
| `aasPreconfigPaths` | `[]` | AAS Environment startup import sources. Supports files or folders with `.aasx`, `.json`, or `.xml` files. |
| `bulkBatchLimit` | `1000` | Maximum row count per generated bulk SQL statement. Must be greater than `0`. |

When registry synchronization is enabled, `general.externalUrl` must be set to at least one absolute URL with scheme and host.

### `jws` and `swagger`

| Key | Default | Purpose |
| --- | --- | --- |
| `jws.privateKeyPath` | `""` | RSA private key used by Submodel Repository and AAS Environment signing use cases. |
| `jws.certificateChainPath` | `""` | PEM-encoded X.509 certificate chain included as the JWS `x5c` certificate chain where signing supports it. |
| `swagger.enabled` | `true` | Enables Swagger UI and OpenAPI specification endpoints. |
| `swagger.contactName` | `Eclipse BaSyx` | Contact name injected into OpenAPI/Swagger docs. |
| `swagger.contactEmail` | `basyx-dev@eclipse.org` | Contact email injected into OpenAPI/Swagger docs. |
| `swagger.contactUrl` | `https://basyx.org` | Contact URL injected into OpenAPI/Swagger docs. |

### `history`

History settings control API history, audit metadata, and optional external evidence storage. A component must implement history handling for these settings to have a runtime effect.

| Key | Default | Purpose |
| --- | --- | --- |
| `mode` | `off` | History mode: `off`, `api`, or `audit`. |
| `retentionDays` | `0` | Requested database-history retention. Only `0` (keep forever) is currently accepted; automatic deletion is not implemented. |
| `fullSnapshotInterval` | `1` | Number of history rows between full snapshots. Must be at least `1`; `1` stores every row as a full snapshot. |
| `immutability` | `none` | Immutability mode: `none`, `postgres_guarded`, or the reserved `external_anchor`. |
| `auditIdentityMode` | `none` | Identity detail stored with audit entries: `none`, `minimal`, or `extended`. |
| `integrityAnchor.provider` | `none` | External integrity-anchor backend. Only `none` is currently implemented. |

`external_anchor` cannot currently be used: it requires a non-`none` integrity-anchor provider, while no such provider is implemented yet.

#### `history.evidence`

Evidence storage writes WORM-compatible history artifacts to object storage.

| Key | Default | Purpose |
| --- | --- | --- |
| `enabled` | `false` | Enables external evidence artifact writing. Requires `history.mode` to be `api` or `audit`. |
| `provider` | `none` | Evidence backend. Accepted values are `none` and `s3`; enabled evidence requires `s3`. |
| `bucket` | `""` | S3 bucket that receives evidence artifacts. Required when evidence is enabled. |
| `prefix` | `basyx-history-evidence` | Object-key prefix used inside the bucket. |
| `region` | `us-east-1` | S3 region. Required when evidence is enabled. |
| `endpoint` | `""` | Optional custom S3-compatible endpoint, for example a MinIO endpoint. |
| `accessKeyId` | `""` | Optional explicit S3 access-key ID. Configure it together with `secretAccessKey`. |
| `secretAccessKey` | `""` | Optional explicit S3 secret access key. Configure it together with `accessKeyId`. |
| `pathStyle` | `false` | Uses path-style S3 addressing instead of virtual-hosted bucket addressing. Often needed for local S3-compatible services. |
| `retentionMode` | `""` | S3 Object Lock mode: `governance` or `compliance`. Required when evidence is enabled. |
| `retentionDays` | `0` | Object-lock retention period. Must be at least `1` when evidence is enabled. |
| `writeTimeoutSeconds` | `10` | Timeout for writing an evidence artifact. Must be at least `1`. |
| `signing.privateKeyPath` | `""` | Private key used to sign evidence manifests. If empty, `jws.privateKeyPath` is used as the fallback signing key. |
| `signing.publicKeyPath` | `""` | Public key used for evidence-signature verification. |
| `signing.required` | `false` | Requires signing material. At least a signing private key, the JWS fallback key, or a public key must be configured. |

Credentials are sensitive. Prefer secret-backed environment variables or mounted secret files over committing them to YAML.

### `eventing`

The eventing configuration is reserved for future publishing and outbox support.

| Key | Default | Purpose |
| --- | --- | --- |
| `enabled` | `false` | Requests event publishing. Currently rejected because event publishing is not implemented. |
| `format` | `cloudevents` | Reserved event serialization format. |
| `sinks` | `[]` | Reserved list of event sink destinations. A non-empty list is currently rejected. |
| `outboxEnabled` | `false` | Requests transactional outbox processing. Currently rejected. |
| `topicPrefix` | `basyx` | Reserved prefix for generated event topics. |

Keep `enabled` and `outboxEnabled` set to `false` and `sinks` empty until eventing support is implemented.

## Example YAML

```yaml
server:
  host: 0.0.0.0
  port: 5004
  contextPath: ""
  cacheEnabled: false
  strictVerification: permissive
  verificationEndpointAvailable: true
  readHeaderTimeoutSeconds: 15
  readTimeoutSeconds: 300
  writeTimeoutSeconds: 300
  idleTimeoutSeconds: 60
  shutdownTimeoutSeconds: 10

postgres:
  dsn: ""
  host: db
  port: 5432
  dbname: basyxTestDB
  user: admin
  password: admin123
  sslmode: disable
  sslcert: ""
  sslkey: ""
  sslrootcert: ""
  connectTimeoutSeconds: 0
  applicationName: ""
  fallbackApplicationName: ""
  searchPath: ""
  options: ""
  timezone: ""
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
  policyFileImport: ""
  policyScope: ""
  managementApi:
    enabled: false

general:
  enableImplicitCasts: true
  enableDescriptorDebug: false
  discoveryIntegration: false
  enableCustomMiddlewareHeaderInjection: false
  supportsSingularSupplementalSemanticId: false
  aasRegistryIntegration: false
  submodelRegistryIntegration: false
  externalUrl: ""
  trustProxyHeaders: false
  trustedProxyCIDRs: []
  uploadMaxSizeBytes: 134217728
  aasPreconfigPaths: []
  bulkBatchLimit: 1000

jws:
  privateKeyPath: ""
  certificateChainPath: ""

swagger:
  enabled: true
  contactName: "Eclipse BaSyx"
  contactEmail: "basyx-dev@eclipse.org"
  contactUrl: "https://basyx.org"

history:
  mode: off
  retentionDays: 0
  fullSnapshotInterval: 1
  immutability: none
  auditIdentityMode: none
  evidence:
    enabled: false
    provider: none
    bucket: ""
    prefix: basyx-history-evidence
    region: us-east-1
    endpoint: ""
    accessKeyId: ""
    secretAccessKey: ""
    pathStyle: false
    retentionMode: ""
    retentionDays: 0
    writeTimeoutSeconds: 10
    signing:
      privateKeyPath: ""
      publicKeyPath: ""
      required: false
  integrityAnchor:
    provider: none

eventing:
  enabled: false
  format: cloudevents
  sinks: []
  outboxEnabled: false
  topicPrefix: basyx
```

## Environment Variables

For regular settings, use the uppercase YAML path with dots replaced by underscores:

```bash
SERVER_PORT=5004
SERVER_CONTEXTPATH=/api
SERVER_STRICTVERIFICATION=permissive
SERVER_READ_HEADER_TIMEOUT_SECONDS=15
SERVER_READ_TIMEOUT_SECONDS=300
SERVER_WRITE_TIMEOUT_SECONDS=300
SERVER_IDLE_TIMEOUT_SECONDS=60
SERVER_SHUTDOWN_TIMEOUT_SECONDS=10
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DBNAME=basyxTestDB
POSTGRES_SSLMODE=disable
POSTGRES_CONNECTTIMEOUTSECONDS=10
ABAC_ENABLED=false
ABAC_POLICYFILEIMPORT=if_missing
ABAC_POLICY_SCOPE=aasregistryservice
ABAC_MANAGEMENTAPI_ENABLED=false
OIDC_TRUSTLISTPATH=config/trustlist.json
GENERAL_EXTERNALURL=https://example.org/aas
GENERAL_TRUSTPROXYHEADERS=false
GENERAL_UPLOADMAXSIZEBYTES=134217728
GENERAL_BULK_BATCH_LIMIT=1000
SWAGGER_ENABLED=true
```

`GENERAL_AAS_PRECONFIG_PATHS` is parsed as a comma-separated list and overrides `general.aasPreconfigPaths`:

```bash
GENERAL_AAS_PRECONFIG_PATHS=file:/data/example.aasx,/data/preconfigured-aas
```

The following explicit aliases are also supported:

| YAML setting | Environment variable |
| --- | --- |
| `server.readHeaderTimeoutSeconds` | `SERVER_READ_HEADER_TIMEOUT_SECONDS` or `BASYX_SERVER_READ_HEADER_TIMEOUT_SECONDS` |
| `server.readTimeoutSeconds` | `SERVER_READ_TIMEOUT_SECONDS` or `BASYX_SERVER_READ_TIMEOUT_SECONDS` |
| `server.writeTimeoutSeconds` | `SERVER_WRITE_TIMEOUT_SECONDS` or `BASYX_SERVER_WRITE_TIMEOUT_SECONDS` |
| `server.idleTimeoutSeconds` | `SERVER_IDLE_TIMEOUT_SECONDS` or `BASYX_SERVER_IDLE_TIMEOUT_SECONDS` |
| `server.shutdownTimeoutSeconds` | `SERVER_SHUTDOWN_TIMEOUT_SECONDS` or `BASYX_SERVER_SHUTDOWN_TIMEOUT_SECONDS` |
| `abac.policyFileImport` | `ABAC_POLICY_FILE_IMPORT` or `BASYX_ABAC_POLICY_FILE_IMPORT` |
| `abac.policyScope` | `ABAC_POLICY_SCOPE` or `BASYX_ABAC_POLICY_SCOPE` |
| `abac.managementApi.enabled` | `ABAC_MANAGEMENT_API_ENABLED`, `ABAC_MANAGEMENTAPI_ENABLED`, or `BASYX_ABAC_MANAGEMENT_API_ENABLED` |
| `general.bulkBatchLimit` | `GENERAL_BULK_BATCH_LIMIT` or `BASYX_GENERAL_BULK_BATCH_LIMIT` |
| `history.mode` | `BASYX_HISTORY_MODE` |
| `history.retentionDays` | `BASYX_HISTORY_RETENTION_DAYS` |
| `history.fullSnapshotInterval` | `BASYX_HISTORY_FULL_SNAPSHOT_INTERVAL` |
| `history.immutability` | `BASYX_HISTORY_IMMUTABILITY` |
| `history.auditIdentityMode` | `BASYX_AUDIT_IDENTITY_MODE` |
| `history.evidence.enabled` | `BASYX_HISTORY_EVIDENCE_ENABLED` |
| `history.evidence.provider` | `BASYX_HISTORY_EVIDENCE_PROVIDER` |
| `history.evidence.bucket` | `BASYX_HISTORY_EVIDENCE_BUCKET` |
| `history.evidence.prefix` | `BASYX_HISTORY_EVIDENCE_PREFIX` |
| `history.evidence.region` | `BASYX_HISTORY_EVIDENCE_REGION` |
| `history.evidence.endpoint` | `BASYX_HISTORY_EVIDENCE_ENDPOINT` |
| `history.evidence.accessKeyId` | `BASYX_HISTORY_EVIDENCE_ACCESS_KEY_ID` |
| `history.evidence.secretAccessKey` | `BASYX_HISTORY_EVIDENCE_SECRET_ACCESS_KEY` or `BASYX_HISTORY_EVIDENCE_SECRET_KEY` |
| `history.evidence.pathStyle` | `BASYX_HISTORY_EVIDENCE_PATH_STYLE` or `BASYX_HISTORY_EVIDENCE_USE_PATH_STYLE` |
| `history.evidence.retentionMode` | `BASYX_HISTORY_EVIDENCE_RETENTION_MODE` |
| `history.evidence.retentionDays` | `BASYX_HISTORY_EVIDENCE_RETENTION_DAYS` |
| `history.evidence.writeTimeoutSeconds` | `BASYX_HISTORY_EVIDENCE_WRITE_TIMEOUT_SECONDS` |
| `history.evidence.signing.privateKeyPath` | `BASYX_HISTORY_EVIDENCE_SIGNING_PRIVATE_KEY_PATH` |
| `history.evidence.signing.publicKeyPath` | `BASYX_HISTORY_EVIDENCE_SIGNING_PUBLIC_KEY_PATH` |
| `history.evidence.signing.required` | `BASYX_HISTORY_EVIDENCE_SIGNING_REQUIRED` |
| `history.integrityAnchor.provider` | `BASYX_HISTORY_INTEGRITY_ANCHOR_PROVIDER` |
| `eventing.enabled` | `BASYX_EVENTING_ENABLED` |
| `eventing.format` | `BASYX_EVENTING_FORMAT` |
| `eventing.sinks` | `BASYX_EVENTING_SINKS` (comma-separated) |
| `eventing.outboxEnabled` | `BASYX_EVENTING_OUTBOX_ENABLED` |
| `eventing.topicPrefix` | `BASYX_EVENTING_TOPIC_PREFIX` |

The legacy Viper-derived names without word-separating underscores, such as `SERVER_READTIMEOUTSECONDS`, remain supported. The explicit aliases are applied after normal environment-variable decoding and therefore take precedence when both forms are set.

To use a complete PostgreSQL DSN, set only `POSTGRES_DSN` for the connection details. Do not also set individual connection variables such as `POSTGRES_HOST` or `POSTGRES_SSLMODE`:

```bash
POSTGRES_DSN=postgres://admin:secret@db:5432/basyx?sslmode=require
POSTGRES_MAXOPENCONNECTIONS=50
POSTGRES_MAXIDLECONNECTIONS=50
```

## Security Files

The shared configuration may reference these security-sensitive files:

- `oidc.trustlistPath`
- `abac.modelPath`
- `jws.privateKeyPath`
- `jws.certificateChainPath`
- `history.evidence.signing.privateKeyPath`
- `history.evidence.signing.publicKeyPath`
- `postgres.sslcert`
- `postgres.sslkey`
- `postgres.sslrootcert`

In containers, paths are resolved inside the container filesystem. Mount the files or their parent directory and point the YAML value or environment variable to the mounted path.

## Notes

- The BaSyx Configuration Service mainly uses the `postgres` section.
- Repository and environment services use `general.uploadMaxSizeBytes` for upload limits.
- AAS Environment additionally supports `general.aasPreconfigPaths`.
- AAS Repository, Submodel Repository, and AAS Environment use the registry synchronization settings when enabled.
