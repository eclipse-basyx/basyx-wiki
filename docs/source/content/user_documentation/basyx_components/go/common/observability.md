# Observability

BaSyx Go provides structured application logging, request correlation, optional
OpenTelemetry tracing, and PostgreSQL connection-pool metrics through shared
runtime infrastructure. Logging and tracing are available in BaSyx Go `1.0.4`
or newer. The pool metrics require BaSyx Go `1.0.6` or newer.

The application remains independent of a particular observability backend:

```text
BaSyx JSON stderr --> platform log collector --> Loki or another log store
BaSyx OTLP traces --> OpenTelemetry Collector --> Tempo, Jaeger, or another trace store
BaSyx OTLP metrics --> OpenTelemetry Collector --> Prometheus or another metric store
```

BaSyx does not contain direct clients for Grafana, Loki, Tempo, or Jaeger.

## Structured Logging

Every BaSyx command writes diagnostic logs to standard error. The default is
human-readable text at `info` level:

```yaml
logging:
  format: text
  level: info
```

The equivalent environment variables are:

```text
LOGGING_FORMAT=text
LOGGING_LEVEL=info
```

`LOGGING_FORMAT` accepts `text` or `json`. `LOGGING_LEVEL` accepts `debug`,
`info`, `warn`, or `error`. Environment variables override YAML values.

JSON output is recommended for container deployments:

```json
{"time":"2026-07-25T10:00:01Z","level":"INFO","msg":"HTTP request completed","service.name":"aasenvironmentservice","request.id":"request-42","correlation.id":"workflow-7","http.request.method":"GET","url.path":"/shells","http.route":"/shells","http.response.status_code":200,"http.response.body.size":421,"duration_ms":3.725}
```

Configuration logs contain only curated, non-sensitive attributes. Passwords,
DSNs, access tokens, object-store credentials, private-key material, request
bodies, and response bodies are not logged.

Logs remain available through the platform's normal process-log mechanism:

```bash
docker logs -f <container>
kubectl logs -f <pod> [-c <container>]
journalctl -f -u <unit>
```

BaSyx does not write application log files or provide log rotation, retention,
or a `/logs` endpoint. Collect standard error with the platform agent of your
choice, for example Grafana Alloy, Fluent Bit, or an OpenTelemetry Collector.

## HTTP Request and Correlation IDs

Every BaSyx Go HTTP service emits one `HTTP request completed` event for each
request. Normal requests are logged at `info`; `GET` health probes are logged at
`debug` to avoid filling the default log stream.

Clients and trusted ingress controllers may provide:

- `X-Request-ID`
- `X-Correlation-ID`

The legacy `Request-ID` and `Correlation-ID` names are accepted as input
aliases. Accepted IDs contain 1 to 128 ASCII letters, digits, or `._:/-`.
Missing or invalid request IDs are replaced with a generated `req-` identifier.
A missing or invalid correlation ID defaults to the request ID.

BaSyx returns the two canonical headers and automatically permits and exposes
them through its CORS middleware. Request and correlation IDs are useful for
searching logs, but they are not authenticated identity data and must not be
used for authorization decisions.

Access records contain the method, path, resolved route, response status and
size, and request duration. Query strings, arbitrary headers, request and
response bodies, authorization values, tokens, user agents, and client IP
addresses are not recorded.

## OpenTelemetry Tracing and Metrics

Tracing and metrics are optional and configured independently through standard
OpenTelemetry environment variables. They are not BaSyx YAML configuration
keys.

- Tracing is disabled when `OTEL_TRACES_EXPORTER` is unset, empty, or `none`.
- Metrics are disabled when `OTEL_METRICS_EXPORTER` is unset, empty, or `none`.
- `OTEL_SDK_DISABLED=true` disables both signals.

The typical Collector configuration is:

```text
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.observability.svc:4318
OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=production
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```

Either signal can be enabled without the other. The `console` exporter is
available for local diagnostics. Supported explicit exporter values are
`otlp`, `console`, and `none`.

The default trace sampler is parent-based and always-on, so high-volume
deployments should configure an appropriate sampling ratio.

BaSyx supports the standard OpenTelemetry Go environment variables for:

- the generic OTLP endpoint, protocol, headers, compression, and timeout:
  `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`,
  `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_COMPRESSION`, and
  `OTEL_EXPORTER_OTLP_TIMEOUT`
- trace-specific overrides:
  `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`,
  `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`,
  `OTEL_EXPORTER_OTLP_TRACES_HEADERS`,
  `OTEL_EXPORTER_OTLP_TRACES_COMPRESSION`, and
  `OTEL_EXPORTER_OTLP_TRACES_TIMEOUT`
- metric-specific overrides:
  `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`,
  `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`,
  `OTEL_EXPORTER_OTLP_METRICS_HEADERS`,
  `OTEL_EXPORTER_OTLP_METRICS_COMPRESSION`, and
  `OTEL_EXPORTER_OTLP_METRICS_TIMEOUT`
- `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES`
- trace sampling and batch span processing (`OTEL_TRACES_*` and `OTEL_BSP_*`)
- the metric export interval and timeout through
  `OTEL_METRIC_EXPORT_INTERVAL` and `OTEL_METRIC_EXPORT_TIMEOUT`
- W3C Trace Context and Baggage propagation through `OTEL_PROPAGATORS`

The signal-specific endpoint, protocol, headers, compression, and timeout
override their generic counterparts for that signal. The export interval and
timeout are positive integer values in milliseconds. If no endpoint is
specified, the OpenTelemetry SDK's normal OTLP defaults apply.

The default telemetry resource `service.name` is the lowercase BaSyx command
name, for example `aasenvironmentservice`. An explicit `OTEL_SERVICE_NAME`
overrides it.

Each inbound HTTP request creates a server span. Valid W3C `traceparent` and
`tracestate` values are preserved, while requests without trace context start a
new trace. Delegated submodel-operation calls create client spans and propagate
the active W3C trace context. Other third-party clients, including OIDC
discovery, are not instrumented.

Export happens asynchronously in batches. An unavailable Collector does not
prevent service startup or fail HTTP requests; telemetry can be dropped while
the backend is unavailable. Shutdown uses a bounded flush period.

### PostgreSQL Connection-Pool Metrics

Each supported HTTP service registers its shared PostgreSQL writer pool once.
Metric collection reads Go's in-process `database/sql.DBStats()` and does not
run additional database queries.

| Metric | Type | Meaning |
| --- | --- | --- |
| `db.client.connection.max` | Up/down counter | Configured maximum number of open connections |
| `db.client.connection.count` with `db.client.connection.state=used` | Up/down counter | Connections currently in use |
| `db.client.connection.count` with `db.client.connection.state=idle` | Up/down counter | Connections currently idle |
| `basyx.db.client.connection.waits` | Cumulative counter | Requests that waited for a connection |
| `basyx.db.client.connection.wait_time` | Cumulative counter in seconds | Total time spent waiting for connections |
| `basyx.db.client.connection.closed` with `basyx.db.client.connection.close.reason=idle_limit` | Cumulative counter | Connections closed because of the idle-count limit |
| `basyx.db.client.connection.closed` with `basyx.db.client.connection.close.reason=idle_time` | Cumulative counter | Connections closed after their maximum idle time |
| `basyx.db.client.connection.closed` with `basyx.db.client.connection.close.reason=max_lifetime` | Cumulative counter | Connections closed after their maximum lifetime |

Open connections are the sum of the `used` and `idle` points on
`db.client.connection.count`. Every point has
`db.system.name=postgresql` and
`db.client.connection.pool.name=writer`. The `service.name` resource attribute
identifies the service instance.

Use rates rather than raw totals for the cumulative wait and closure counters.
A rising wait rate while the number of used connections approaches
`db.client.connection.max` indicates that the application pool is constraining
concurrency. Low utilization with slow requests points elsewhere, for example
to query execution, PostgreSQL capacity, or storage latency. Pool metrics show
client-side pressure; they do not measure query duration or increase database
capacity.

The metric attributes are intentionally bounded. Database names, hosts, users,
DSNs, SQL text, AAS identifiers, and request data are not recorded. Do not copy
such values into `OTEL_RESOURCE_ATTRIBUTES`, because resource attributes are
attached to every exported data point.

Pool metrics are available for these HTTP services:

- AAS Environment
- AAS Repository
- AAS Registry
- AASX File Server
- Basic Discovery
- Company Lookup
- Concept Description Repository
- Digital Product Passport API
- Digital Twin Registry
- Submodel Repository
- Submodel Registry

The Configuration Service and History Evidence Verifier remain logging-only
commands. They do not expose HTTP servers or long-running telemetry runtimes.

## Correlating Logs and Traces

Contextual logs produced inside an active span contain:

- `trace_id`
- `span_id`
- `trace_flags`

The `HTTP request completed` record is written before its server span ends, so
its identifiers match the exported span. A log backend can use `trace_id` to
link to a trace backend, and a trace backend can query logs for the same
service, time range, and trace ID.

Trace spans do not capture query strings, bodies, authorization values,
arbitrary headers, tokens, user agents, or client IP addresses. URL paths are
recorded, so secrets and sensitive personal data should never be placed in URL
path segments.

## Examples and Helm

The [BaSyx Go observability
example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxObservabilityExample)
provides a local development stack with an AAS Environment, BaSyx Web UI,
OpenTelemetry Collector, Tempo, Loki, Alloy, and Grafana. It verifies trace
and metric export, structured-log ingestion, trace-to-log correlation, and
continued service operation during a Collector outage.

For Kubernetes, the [BaSyx Helm
chart](https://github.com/eclipse-basyx/charts) exposes common logging and
telemetry values. Its observability values example connects BaSyx workloads to
an existing Collector:

```yaml
telemetry:
  tracesExporter: otlp
  metricsExporter: otlp
  endpoint: http://opentelemetry-collector.observability.svc.cluster.local:4318
  protocol: http/protobuf
  metricsExportInterval: "60000"
  metricsExportTimeout: "30000"
```

The generic endpoint and protocol apply to both signals. Signal-specific OTLP
overrides and credentials can be supplied through `environment.common` or
`telemetry.existingSecret`. Store OTLP authorization headers in a Secret rather
than a values file. The chart intentionally does not install Grafana, Loki,
Tempo, or Alloy because authentication, storage, retention, resource sizing,
and tenancy should be designed for the target cluster.

The local Compose stack is a development example, not a production deployment
reference. Production environments should use authenticated telemetry
endpoints, TLS, secret-backed OTLP headers, bounded retention, resource limits,
and least-privilege log collection.

## Current Scope

BaSyx Go currently provides traces, PostgreSQL pool metrics, structured logs,
and log-to-trace correlation. It does not provide direct OTLP log export,
database query spans, SQL statement capture, query-duration metrics,
AAS-domain spans, arbitrary outbound HTTP propagation, runtime telemetry
reconfiguration, or a built-in metrics endpoint.
