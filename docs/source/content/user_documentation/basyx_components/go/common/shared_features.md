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

## Logging and Request Correlation

All commands use structured, severity-filtered logging on standard error. HTTP
services also provide canonical request and correlation IDs and emit one
access-log event per request. See [Observability](observability) for the logging
contract and header behavior.

## Optional OpenTelemetry Telemetry

HTTP services can create OpenTelemetry server spans and correlate contextual
logs with trace and span IDs. They can also export shared PostgreSQL
connection-pool metrics. Tracing and metrics are disabled independently by
default and configured through standard OpenTelemetry environment variables.
See [Observability](observability) for activation, propagation, sampling,
metric interpretation, and backend integration.

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
- `postgres.applicationName`
- `postgres.maxOpenConnections`
- `postgres.maxIdleConnections`
- `postgres.connMaxLifetimeMinutes`
- `postgres.connMaxIdleTimeMinutes`

```{note}
The pool behavior in this section requires BaSyx Go 1.0.5 or later.
```

Each service process or Kubernetes pod owns a separate pool. The common defaults are:

| Setting | Default | Zero value |
| --- | --- | --- |
| `maxOpenConnections` | `50` | Uses the default. |
| `maxIdleConnections` | `25` | Uses the default, capped at a smaller explicit open limit. |
| `connMaxLifetimeMinutes` | `5` | Uses the default. |
| `connMaxIdleTimeMinutes` | `0` | Disables idle-time recycling. |

An explicitly configured idle limit greater than the effective open limit is rejected at startup. Size each PostgreSQL primary independently: add the open limits of every BaSyx pod and other application pool connected to that primary, using the maximum concurrent replica count during rolling updates. Reserve capacity for administration, monitoring, schema migration, and failover.

If `applicationName` and the DSN do not define a PostgreSQL `application_name`, the service name is used automatically. Explicit values are preserved. This makes per-service connections visible in `pg_stat_activity`.

See [General Configuration](configuration) for the full PostgreSQL configuration and budgeting guidance.

## Optional PostgreSQL Reader Routing

BaSyx Go 1.0.7 and later can open an independent PostgreSQL reader pool for
eligible reads. Without reader configuration, the writer pool is reused and
the behavior remains unchanged. With a reader configured, mutations and
consistency-sensitive work stay on the writer while eligible reads can be
served by a standby or other read endpoint.

Reader routing is based on consistency requirements, not on how many database
queries a request executes. Results from a replicated reader are eventually
consistent between requests, including authorization-relevant resource changes.
When one response requires multiple SQL queries, those queries use one
read-only repeatable-read transaction so that the response is assembled from
one reader snapshot. See
[General Configuration](configuration#optional-postgresql-reader) for the
supported components, routing guarantees, security considerations, connection
variables, and independent pool-sizing guidance.
