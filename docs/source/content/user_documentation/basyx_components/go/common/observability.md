# Observability

BaSyx Go provides structured application logging, request correlation, and
optional OpenTelemetry tracing through shared runtime infrastructure. The
features described on this page are available in `SNAPSHOT` images and in
BaSyx Go `1.0.4` or newer.

The application remains independent of a particular observability backend:

```text
BaSyx JSON stderr --> platform log collector --> Loki or another log store
BaSyx OTLP traces --> OpenTelemetry Collector --> Tempo, Jaeger, or another trace store
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

```env
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

## OpenTelemetry Tracing

Tracing is optional and environment-only. It is disabled when
`OTEL_TRACES_EXPORTER` is unset, empty, or `none`, or when
`OTEL_SDK_DISABLED=true`.

The typical Collector configuration is:

```env
OTEL_TRACES_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.observability.svc:4318
OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=production
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```

The `console` exporter is available for local diagnostics. The default sampler
is parent-based and always-on, so high-volume deployments should configure an
appropriate sampling ratio.

BaSyx supports the standard OpenTelemetry Go environment variables for:

- OTLP endpoints, protocols, headers, compression, and timeouts
- `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES`
- trace sampling and batch span processing (`OTEL_TRACES_*` and `OTEL_BSP_*`)
- W3C Trace Context and Baggage propagation through `OTEL_PROPAGATORS`

The default trace resource `service.name` is the lowercase BaSyx command name,
for example `aasenvironmentservice`. An explicit `OTEL_SERVICE_NAME` overrides
it.

Each inbound HTTP request creates a server span. Valid W3C `traceparent` and
`tracestate` values are preserved, while requests without trace context start a
new trace. Delegated submodel-operation calls create client spans and propagate
the active W3C trace context. Other third-party clients, including OIDC
discovery, are not instrumented.

Export happens asynchronously in batches. An unavailable Collector does not
prevent service startup or fail HTTP requests; telemetry can be dropped while
the backend is unavailable. Shutdown uses a bounded flush period.

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
export, structured-log ingestion, trace-to-log correlation, and continued
service operation during a Collector outage.

For Kubernetes, the [BaSyx Helm
chart](https://github.com/eclipse-basyx/charts) exposes common logging and
tracing values. Its observability values example connects BaSyx workloads to an
existing Collector. The chart intentionally does not install Grafana, Loki,
Tempo, or Alloy because authentication, storage, retention, resource sizing,
and tenancy should be designed for the target cluster.

The local Compose stack is a development example, not a production deployment
reference. Production environments should use authenticated telemetry
endpoints, TLS, secret-backed OTLP headers, bounded retention, resource limits,
and least-privilege log collection.

## Current Scope

BaSyx Go currently provides traces, structured logs, and log-to-trace
correlation. It does not provide OpenTelemetry metrics, direct OTLP log export,
database spans, AAS-domain spans, arbitrary outbound HTTP propagation, or
runtime telemetry reconfiguration.
