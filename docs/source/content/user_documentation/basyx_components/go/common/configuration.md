# General Configuration

BaSyx Go components use a shared configuration model from `internal/common` and support configuration via YAML files plus environment variables.

## Configuration Source Precedence

The shared configuration loader applies the following precedence:

1. Environment variables
2. YAML configuration file
3. Built-in defaults

Environment variables override values from the YAML file. Nested keys use underscore notation (for example `server.port` -> `SERVER_PORT`).

## Common Configuration Sections

These configuration blocks are part of the shared config model and are reused across components:

- `server` (host, port, context path, cache settings, verification flags)
- `postgres` (database connection and pooling)
- `cors` (allowed origins/methods/headers and credentials)
- `general` (shared runtime feature flags)
- `oidc` (trustlist path for issuer validation)
- `abac` (ABAC enable flag and rule model path)
- `jws` (private key path for signing use cases)
- `swagger` (contact metadata for OpenAPI/Swagger UI)

## Security Files (OIDC Trustlist and ABAC Access Rules)

Components that use the shared OIDC/ABAC security setup may rely on these two file paths:

- `oidc.trustlistPath` (default: `config/trustlist.json`)
- `abac.modelPath` (default: `config/access_rules/access-rules.json`)

### What they are used for

- `oidc.trustlistPath`: JSON trustlist of allowed OIDC providers (issuer, audience, scopes)
- `abac.modelPath`: ABAC access-rules model used for authorization decisions

### How paths are configured

- YAML:
  - `oidc.trustlistPath`
  - `abac.modelPath`
- Environment variables (override YAML):
  - `OIDC_TRUSTLISTPATH`
  - `ABAC_MODELPATH`

### Startup behavior

- If `abac.enabled = false`, components using the shared security setup typically skip OIDC/ABAC initialization and do not require these files at startup.
- If `abac.enabled = true`, the trustlist file is read during startup. The ABAC model file is also read when `abac.modelPath` is set (default: set).
- Invalid path, unreadable file, or invalid JSON / invalid access model causes startup failure.

### Docker / Container handling

- Paths are resolved inside the container filesystem.
- Mount the files (or a directory containing them) into the container and point the config/env vars to the mounted paths.
- Example mount pattern: `./security_env:/security_env:ro`

## Example YAML (Shared Structure)

```yaml
server:
  host: 0.0.0.0
  port: 5004
  contextPath: ""

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

jws:
  privateKeyPath: ""

swagger:
  contactName: "Eclipse BaSyx"
  contactEmail: "basyx-dev@eclipse.org"
  contactUrl: "https://basyx.org"
```

## Notes

- Some components may ignore config blocks that are not relevant to their feature set.
- Individual component pages should document only component-specific options and behavior; shared options are documented here.
