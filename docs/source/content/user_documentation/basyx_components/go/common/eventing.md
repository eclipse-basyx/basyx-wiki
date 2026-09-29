# Eventing

```{warning}
Eventing is an experimental feature. Its configuration, event schemas, delivery behavior, and APIs may change.
```

BaSyx Go Eventing exposes changes to AAS and Submodel data as CloudEvents. Applications can read retained events through the REST Event Feed or receive events through MQTT 5, Kafka, or AMQP 1.0.

Eventing is supported by the AAS Repository, Submodel Repository, and AAS Environment. It covers changes to Asset Administration Shells, assets, and Submodels, including dedicated notifications for newly added Product Change Notification (PCN) records.

Eventing is disabled by default and must be enabled explicitly. Run the [Configuration Service](../configuration_service/index) before enabling it so that PostgreSQL contains the required database schema.

## Supported Components and Events

| Producer | Events |
| --- | --- |
| AAS Repository | AAS and asset changes, plus Submodel and PCN changes made through its AAS-scoped Submodel API |
| Submodel Repository | Submodel and PCN changes |
| AAS Environment | AAS, asset, Submodel, and PCN changes, including changes made through environment upload/import paths |

| Event family | CloudEvents `type` values |
| --- | --- |
| AAS | `io.admin-shell.aas.created.v1`, `io.admin-shell.aas.updated.v1`, `io.admin-shell.aas.deleted.v1` |
| Asset | `io.admin-shell.asset.created.v1`, `io.admin-shell.asset.updated.v1`, `io.admin-shell.asset.deleted.v1` |
| Submodel | `io.admin-shell.submodel.created.v1`, `io.admin-shell.submodel.updated.v1`, `io.admin-shell.submodel.deleted.v1` |
| PCN | `io.admin-shell.pcn.v1` |

Creating, updating, or deleting an AAS or Submodel produces the corresponding change event. Changes to nested Submodel Elements, values, and File attachments produce a Submodel update event. An AAS change can produce both an AAS event and a related asset event. Changes to asset information or thumbnails produce an AAS update event and can also produce a related asset update event.

Reads and rolled-back transactions do not produce events. A `PUT` that does not change the stored content also produces no update event. A single operation can produce multiple events when it affects multiple resources.

### Product Change Notifications

BaSyx recognizes Product Change Notification (PCN) Submodels by the ECLASS IRDI code `01-AHE582` used by the IDTA ProductChangeNotifications Submodel Template. Matching uses the code segment of an IRDI such as `0173-1#01-AHE582#003`, so the revision segment may vary.

When a mutation adds one or more PCN records, BaSyx produces the normal Submodel change event and one `io.admin-shell.pcn.v1` notification for each newly added record. The PCN event contains the added record in Value-Only representation. Other changes to a PCN Submodel produce only the normal Submodel event.

## Delivery Options

| Delivery option | Use case |
| --- | --- |
| REST Event Feed | Poll retained events through the hosting BaSyx HTTP API without operating a message broker |
| MQTT 5 | Publish events to MQTT topics, with configurable QoS and retained-message behavior |
| Kafka | Publish all event families to one Kafka topic with entity-based record keys |
| AMQP 1.0 | Publish durable AMQP messages to a configured broker address |

All four options use the same CloudEvents-based event model. The REST feed retains events for non-destructive HTTP reads, while the broker transports deliver events asynchronously through a transactional queue.

## Event Format

Events use CloudEvents specification version `1.0` in structured JSON form.

| Field | Meaning |
| --- | --- |
| `id` | Unique event identifier. Use it for consumer deduplication. |
| `source` | Logical BaSyx API area associated with the event, such as `<sourceBaseUrl>/shells`, `<sourceBaseUrl>/lookup/shells`, or `<sourceBaseUrl>/submodels`. |
| `type` | Kind of resource change. |
| `subject` | Identifier of the affected AAS, asset, or Submodel. |
| `time` | UTC mutation timestamp. |
| `specversion` | CloudEvents version, `1.0`. |
| `datacontenttype` | Payload media type, `application/json`. |
| `dataschema` | URL of the versioned JSON Schema for `data`. |
| `data` | BaSyx event payload identifying the affected resource and related identifiers. |

Ordinary AAS, asset, and Submodel payloads identify the affected models; they are not complete before/after representations. For example:

```json
{
  "specversion": "1.0",
  "id": "019b7ca9-8c88-7001-8f3a-123456789abc",
  "time": "2026-01-02T03:04:05Z",
  "subject": "urn:example:aas:1",
  "type": "io.admin-shell.aas.updated.v1",
  "source": "https://example.com/api/v3/shells",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/api/v3/.well-known/event-feed/schemas/metamodel-aasChangeEvent.v1.schema.json",
  "data": {
    "aasId": "urn:example:aas:1",
    "globalAssetId": "urn:example:asset:1",
    "submodels": []
  }
}
```

Broker transports publish the regular event payload. `REGULAR` and `COMPACT` presentations can be selected only when reading the REST Event Feed.

## Public Eventing URLs

Set `general.externalUrl` to the public API base URL that Eventing consumers can reach, including any reverse-proxy context path. BaSyx uses this URL when generating CloudEvents `source` and `dataschema` URLs.

Use `eventing.sourceBaseUrl` (`BASYX_EVENTING_SOURCE_BASE_URL`) or `eventing.schemaBaseUrl` (`BASYX_EVENTING_SCHEMA_BASE_URL`) only when Eventing must advertise different public URLs. These values come from configuration rather than incoming request host headers. A custom schema URL must serve the same versioned schemas advertised by the events.

## REST Event Feed

The Event Feed retains events in PostgreSQL and does not require an external message broker. The [Event Feed example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxEventFeedExample) provides a runnable local setup for normal Submodel changes and PCN notifications.

### Enable the Event Feed

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  feed:
    enabled: true
```

| Setting | Environment variable | Default and purpose |
| --- | --- | --- |
| `eventing.feed.enabled` | `BASYX_EVENTING_FEED_ENABLED` | `false`; enables the Event Feed and its discovery routes. |
| `eventing.feed.maxAgeDays` | `BASYX_EVENTING_FEED_MAX_AGE_DAYS` | `30`; visible retention period measured from event time. |
| `eventing.feed.maxPageSize` | `BASYX_EVENTING_FEED_MAX_PAGE_SIZE` | `100`; default and maximum `limit`. |

The following routes are relative to the hosting service's configured context path:

| Route | Purpose |
| --- | --- |
| `GET /events` | Read a retained page of events. |
| `GET /.well-known/event-feed.json` | Discover event types, filters, presentations, schemas, retention, and page limits. |
| `GET /.well-known/event-feed/schemas/{schema}` | Retrieve a versioned event-payload JSON Schema. |

The feed and discovery routes are absent when the feed is disabled. The schema route remains available when a broker transport is enabled so broker consumers can follow `dataschema` links.

### Read and Resume

`GET /events` returns the earliest retained events first. Reading events does not remove them. Follow the returned opaque `cursor` until no cursor is present to read the remaining pages. A cursor preserves the original `since`, `filter`, and `presentation`; omit those parameters on subsequent requests or repeat the same values. Conflicting values are rejected.

For continuous consumption, store the `id` of the last event your application processed and pass it as `lastEventId` when resuming. Events can be replayed, so consumers must deduplicate using the CloudEvents `id`.

The `since` parameter is an inclusive RFC 3339 time filter for an initial query. Do not use it as a durable checkpoint: transactions can commit later with an earlier mutation timestamp. `since` and `lastEventId` cannot be combined. The response's `updated` value is the newest mutation timestamp in that page, not a continuation token.

Events are retained only for the configured retention period. If a consumer falls behind that period, read the current resource state from the BaSyx APIs before resuming event processing.

### Filter Events

The `filter` parameter accepts RSQL prefixed with `rsql:`. It supports the fields `event.type`, `event.subject`, `event.source`, and `event.dataschema`, and the operators `==`, `!=`, `=in=`, and `=out=`. Semicolon means AND, comma means OR, AND has higher precedence, and parentheses group expressions. Filtering `data.*` fields is not supported.

For example, read compact events for one Submodel:

```bash
curl --get 'https://example.com/api/v3/events' \
  --data-urlencode 'filter=rsql:event.subject==urn:example:submodel:1' \
  --data-urlencode 'presentation=COMPACT' \
  --data-urlencode 'limit=10'
```

Expressions are limited to 16 KiB and 32 levels of nesting. Quote values containing reserved RSQL characters.

### Presentations

`REGULAR` is the default and returns the regular payload. `COMPACT` returns its identification subset; compact PCN events omit `record`. `FULL` is accepted only as a deprecated compatibility alias for `REGULAR`.

## Broker Delivery

Broker-based Eventing requires Eventing and the transactional delivery queue to be enabled. Add each required transport to `eventing.sinks` and configure its connection settings as described below:

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  enabled: true
  outboxEnabled: true
  sinks: [mqtt]
```

The only supported `eventing.format` value is `cloudevents`, which is also the default. Broker messages contain structured CloudEvents with the regular event payload.

```{important}
Kafka, AMQP, and MQTT with QoS 1 or 2 use at-least-once delivery. Consumers must use the CloudEvents `id` to detect duplicate deliveries. MQTT QoS 0 does not provide this guarantee.
```

## Delivery Guarantees and Retries

Event creation and the corresponding model change are committed in the same PostgreSQL transaction. A failure before commit produces neither the model change nor its events. Broker publication occurs after commit, so a temporary broker outage does not prevent a model mutation from committing once its event is durably queued.

Failed publications remain pending and are retried with exponential backoff and jitter until delivered. Pending broker events do not expire automatically. Allow enough database capacity for the expected outage duration.

BaSyx preserves order per mutated AAS or Submodel. A failed event blocks later events for that entity while unrelated entities can progress; there is no global event order. Broker acknowledgements can be followed by a process or database failure before queue cleanup, so the same event can be delivered again with the same `id`.

The REST Event Feed uses separate retained storage. Reading the feed does not acknowledge broker deliveries, and feed retention does not expire pending broker events.

## MQTT 5

```yaml
eventing:
  sinks: [mqtt]
  mqtt:
    broker: mqtt://localhost:1883
    clientId: basyx-instance-1
```

| MQTT setting | Default or requirement |
| --- | --- |
| `eventing.mqtt.broker` | Required `mqtt://host:port` or `tls://host:port`; do not embed credentials. |
| `eventing.mqtt.clientId` | Required and unique for each process connected to the broker. |
| `eventing.mqtt.sinkId` | `mqtt`; stable delivery-queue destination identifier. |
| `eventing.mqtt.qos` | `1`; accepts `0`, `1`, or `2`. |
| `eventing.mqtt.retained` | `false`; when enabled, the broker retains only the latest message for each topic. |
| `eventing.mqtt.username`, `password` | Optional credentials; `usernameFile` and `passwordFile` are mounted-file alternatives. |
| `eventing.mqtt.caFile`, `certificateFile`, `keyFile` | Optional private CA and mutual-TLS material for `tls://`. |

`eventing.topicPrefix` defaults to `basyx`. It produces these topic families:

| Event family | Default topic |
| --- | --- |
| AAS | `basyx/aasrepository/aas/{created,updated,deleted}` |
| Asset | `basyx/aasrepository/asset/{created,updated,deleted}` |
| Submodel | `basyx/submodelrepository/submodel/{created,updated,deleted}` |
| PCN | `basyx/submodelrepository/pcn/notification` |

QoS 1 and 2 wait for broker acknowledgement. QoS 0 has no broker acknowledgement and therefore provides weaker delivery behavior. See the runnable [MQTT example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxMQTTExample).

## Kafka

Create the Kafka topic before starting BaSyx:

```yaml
eventing:
  sinks: [kafka]
  kafka:
    brokers: [localhost:9092]
    topic: basyx.events
```

| Kafka setting | Default or requirement |
| --- | --- |
| `eventing.kafka.brokers` | Required bootstrap `host:port` list. |
| `eventing.kafka.topic` | `basyx.events`; receives all event families. |
| `eventing.kafka.sinkId` | `kafka`; stable delivery-queue destination identifier. |
| `eventing.kafka.clientId` | `basyx`. |
| `eventing.kafka.producerBatchMaxBytes` | `0` uses the client default; align larger values with broker and topic limits. |
| `eventing.kafka.tlsEnabled`, `caFile`, `certificateFile`, `keyFile` | TLS and optional mutual-TLS settings. |
| `eventing.kafka.saslMechanism` | Empty disables SASL; supports `PLAIN`, `SCRAM-SHA-256`, and `SCRAM-SHA-512`. |
| `eventing.kafka.username`, `password` | Required when SASL is enabled; file-based alternatives are also supported. |

Kafka record values contain the structured CloudEvent and use `content-type: application/cloudevents+json`. Records use the key `aas_history:<AAS ID>` or `submodel_history:<Submodel ID>`; related asset and PCN events share their parent entity's key. Events for one entity therefore use the same partition and remain ordered while the topic's partition count is stable. There is no ordering guarantee across partitions. Kafka requires acknowledgement from all in-sync replicas before BaSyx marks a publication as delivered.

See the runnable [Kafka example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxKafkaExample).

## AMQP 1.0

Provision the target address before starting BaSyx:

```yaml
eventing:
  sinks: [amqp]
  amqp:
    broker: amqp://localhost:5672
    address: /queues/basyx.events
```

| AMQP setting | Default or requirement |
| --- | --- |
| `eventing.amqp.broker` | Required `amqp://host[:port]` or `amqps://host[:port]`. |
| `eventing.amqp.address` | Required target address. BaSyx does not create broker queues, exchanges, or bindings. |
| `eventing.amqp.sinkId` | `amqp`; stable delivery-queue destination identifier. |
| `eventing.amqp.hostName` | Optional AMQP connection hostname. With RabbitMQ, `vhost:<name>` selects a virtual host. |
| `eventing.amqp.username`, `password` | Optional SASL PLAIN credentials; file-based alternatives are also supported. |
| `eventing.amqp.caFile`, `certificateFile`, `keyFile` | Optional private CA and mutual-TLS material for `amqps`. |

Messages are durable and use `application/cloudevents+json`. Only an AMQP `Accepted` outcome completes a publication; other or ambiguous outcomes are retried. BaSyx preserves per-entity queue order, but broker redelivery and consumer concurrency can affect observed processing order.

This transport implements AMQP 1.0, not AMQP 0-9-1. The runnable [AMQP/RabbitMQ example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxAMQPExample) shows the required RabbitMQ setup.

## Security

The REST Event Feed inherits the hosting service's HTTP authentication and authorization. It has no separate authentication model, and ABAC controls which events a caller can read. If BaSyx cannot safely authorize all information in an event, the complete event is hidden.

HTTP authorization does not filter MQTT, Kafka, or AMQP subscribers. Protect broker delivery independently with TLS where appropriate, secret-backed credentials, and least-privilege topic or address ACLs.

### Authorization Details

With ABAC enabled, callers need `READ` access to the feed and schema routes. AAS events require unrestricted read access to the referenced AAS. Submodel and PCN events require unrestricted read access to the Submodel and, when asset identifiers are present, every contributing AAS. Asset events require access to the owning AAS. Row or field restrictions that prevent safe evaluation cause the complete event to be hidden.

## Advanced Configuration and Operations

The normal Event Feed settings are sufficient for most deployments. These settings control cleanup, visibility latency, or compatibility behavior:

| Setting | Environment variable | Default and purpose |
| --- | --- | --- |
| `eventing.feed.hardDeleteGraceDays` | `BASYX_EVENTING_FEED_HARD_DELETE_GRACE_DAYS` | `10`; delay between feed expiry and physical deletion. `0` removes the delay. |
| `eventing.feed.cleanupIntervalHours` | `BASYX_EVENTING_FEED_CLEANUP_INTERVAL_HOURS` | `24`; physical cleanup interval. Cleanup also runs at startup. |
| `eventing.feed.publishIntervalMillis` | `BASYX_EVENTING_FEED_PUBLISH_INTERVAL_MILLIS` | `250`; interval for making newly committed feed events visible. |
| `eventing.feed.sourceBaseUrl`, `schemaBaseUrl` | `BASYX_EVENTING_FEED_SOURCE_BASE_URL`, `BASYX_EVENTING_FEED_SCHEMA_BASE_URL` | Feed-specific compatibility aliases. Prefer the shared Eventing URL settings. |

Each configured broker transport has an independent queue identified by its `sinkId`; transports used together must have distinct IDs. Replicas sharing a database should use the same sink ID and destination settings, while MQTT client IDs must remain unique per process. Drain pending deliveries before changing a sink ID, broker, topic, address, or other routing setting.

Broker retries start after approximately one second and back off to at most one minute. Re-enabling the same sink resumes its pending queue.

## Observability

Monitor pending deliveries, the age of the oldest pending event, repeated delivery failures, and broker connectivity. Broker delivery exposes these OpenTelemetry metrics with a `sink` attribute:

| Signal | Metrics |
| --- | --- |
| Delivery results | `basyx.eventing.delivered`, `basyx.eventing.delivery.failures` |
| Queue size | `basyx.eventing.pending`, `basyx.eventing.retry.pending` |
| Delivery delay | `basyx.eventing.pending.oldest.age` |
| Broker state | `basyx.eventing.broker.connected` |

See [Observability](observability) for general OpenTelemetry configuration.
