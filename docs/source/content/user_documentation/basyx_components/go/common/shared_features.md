# Common / Shared Features

This page summarizes runtime features that are implemented in shared code and reused by multiple BaSyx Go components.

## Health Endpoint

The shared endpoint helper registers:

- `GET {contextPath}/health`

It returns HTTP `200` with:

```json
{"status":"UP"}
```

## CORS Middleware

Shared CORS middleware is configured from the `cors` config block:

- `allowedOrigins`
- `allowedMethods`
- `allowedHeaders`
- `allowCredentials`

## Context Path Handling

Components can be served below a configurable `server.contextPath`. Shared helpers use this base path when registering common endpoints (for example Swagger UI and health).

## Shared Configuration Loading

All components using `internal/common` benefit from:

- YAML + environment-variable configuration loading
- default values for common settings
- startup configuration logging with sensitive values redacted

## Shared Security Building Blocks

The common configuration and security packages provide reusable building blocks for:

- OIDC trustlist-based issuer configuration (`oidc.trustlistPath`)
- ABAC enablement and model configuration (`abac.*`)
- startup security middleware setup that reads trustlist / access-rules files when ABAC is enabled

## Shared PostgreSQL Configuration Pattern

Multiple components reuse the same PostgreSQL configuration structure and connection pool settings:

- `postgres.host`
- `postgres.port`
- `postgres.dbname`
- `postgres.user`
- `postgres.password`
- `postgres.maxOpenConnections`
- `postgres.maxIdleConnections`
- `postgres.connMaxLifetimeMinutes`
