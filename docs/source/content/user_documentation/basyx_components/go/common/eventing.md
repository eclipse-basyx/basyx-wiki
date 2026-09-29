# Eventing

```{warning}
Eventing is an experimental feature. Its configuration, event schemas, delivery behavior, and APIs may change.
```

BaSyx Go Eventing lets applications react to changes in AAS data without repeatedly polling the Repository APIs. The AAS Repository, Submodel Repository, and AAS Environment can produce CloudEvents for changes to Asset Administration Shells, asset information, Submodels, and Product Change Notification (PCN) records.

Run the [Configuration Service](../configuration_service/index) before enabling Eventing so PostgreSQL contains the required schema.

## Supported Components and Events

| Producer | Events |
| --- | --- |
| AAS Repository | AAS and asset changes, plus Submodel and PCN changes made through its AAS-scoped Submodel API |
| Submodel Repository | Submodel and PCN changes |
| AAS Environment | AAS, asset, Submodel, and PCN changes, including changes made through environment upload/import paths |

The following event types are emitted:

| Event family | CloudEvents `type` values |
| --- | --- |
| AAS | `io.admin-shell.aas.created.v1`, `io.admin-shell.aas.updated.v1`, `io.admin-shell.aas.deleted.v1` |
| Asset | `io.admin-shell.asset.created.v1`, `io.admin-shell.asset.updated.v1`, `io.admin-shell.asset.deleted.v1` |
| Submodel | `io.admin-shell.submodel.created.v1`, `io.admin-shell.submodel.updated.v1`, `io.admin-shell.submodel.deleted.v1` |
| PCN | `io.admin-shell.pcn.v1` |

An AAS mutation produces an AAS event and, when the captured AAS has a `globalAssetId`, a related asset event. Replacing asset information is therefore represented as an AAS update and an asset update. Submodel creation, replacement, deletion, Submodel Element changes, value updates, and File changes produce Submodel events. AAS thumbnail changes produce AAS and applicable asset events.

Adding records to a Submodel in the PCN semantic-ID family `0173-1#01-AHE582#003` produces a Submodel update and one PCN event for each new record. PCN matching uses the IRDI code segment, so the revision segment does not have to be `003`. The PCN event's regular payload contains the added record's value-only representation.

Reads do not create events. A transaction that rolls back leaves no change event, and an acknowledged PUT that does not change stored content creates no update event. Importing multiple resources or making a mutation with related AAS, asset, or PCN effects can create several events in one transaction.

## Delivery Options

| Delivery option | Use case |
| --- | --- |
| REST Event Feed | Poll retained events through the hosting BaSyx HTTP API without operating a message broker |
| MQTT 5 | Publish events to MQTT topics, with configurable QoS and retained-message behavior |
| Kafka | Publish all event families to one Kafka topic with entity-based record keys |
| AMQP 1.0 | Publish durable AMQP messages to a configured broker address |

All options use the same CloudEvents-based event model. The REST feed retains events for non-destructive HTTP reads. Broker delivery uses a transactional PostgreSQL outbox and transport-specific acknowledgements; it is not equivalent to polling the feed.

For broker delivery, the common environment variables are `BASYX_EVENTING_ENABLED`, `BASYX_EVENTING_FORMAT`, `BASYX_EVENTING_SINKS` (comma-separated), and `BASYX_EVENTING_OUTBOX_ENABLED`. The supported format is `cloudevents`.

## Event Format

Events use CloudEvents specification version `1.0` in structured JSON form.

| Field | Meaning |
| --- | --- |
| `id` | Unique event identifier. Use it for consumer deduplication. |
| `source` | Public API area that produced the event, such as `<sourceBaseUrl>/shells` or `<sourceBaseUrl>/submodels`. |
| `type` | Kind of resource change. |
| `subject` | Identifier of the affected AAS, asset, or Submodel. |
| `time` | UTC mutation timestamp. |
| `specversion` | CloudEvents version, currently `1.0`. |
| `datacontenttype` | Payload media type, `application/json`. |
| `dataschema` | URL of the versioned JSON Schema for `data`. |
| `data` | BaSyx event payload identifying the affected resource and related identifiers. |

For ordinary AAS, asset, and Submodel changes, `data` identifies the affected models; it is not a complete before/after representation and does not contain every changed value. For example, a regular Submodel update can look like this:

```json
{
  "datacontenttype": "application/json",
  "specversion": "1.0",
  "id": "019b7ca9-8c88-7001-8f3a-123456789abc",
  "time": "2026-01-02T03:04:05Z",
  "subject": "urn:example:submodel:1",
  "type": "io.admin-shell.submodel.updated.v1",
  "source": "https://example.com/api/v3/submodels",
  "dataschema": "https://example.com/api/v3/.well-known/event-feed/schemas/metamodel-submodelChangeEvent.v1.schema.json",
  "data": {
    "submodelId": "urn:example:submodel:1",
    "globalAssetIds": ["urn:example:asset:1"],
    "semanticId": {
      "type": "ExternalReference",
      "keys": [
        {"type": "GlobalReference", "value": "urn:example:semantic:1"}
      ]
    }
  }
}
```

## REST Event Feed

The Event Feed requires no external message broker. Enable it independently of broker sinks:

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  feed:
    enabled: true
```

The following routes are relative to the service's configured context path:

| Route | Purpose |
| --- | --- |
| `GET /events` | Read a retained page of events. |
| `GET /.well-known/event-feed.json` | Discover event types, filters, presentations, schemas, retention, and page limits. |
| `GET /.well-known/event-feed/schemas/{schema}` | Retrieve a versioned event-payload JSON Schema. |

The feed and discovery routes are absent when the feed is disabled. Schema routes also remain available when a broker transport is enabled so broker consumers can follow `dataschema` links.

### Feed Configuration

| Setting | Environment variable | Default and purpose |
| --- | --- | --- |
| `eventing.feed.enabled` | `BASYX_EVENTING_FEED_ENABLED` | `false`; enables the Event Feed routes and retention. |
| `eventing.feed.maxAgeDays` | `BASYX_EVENTING_FEED_MAX_AGE_DAYS` | `30`; visible retention period measured from event time. |
| `eventing.feed.hardDeleteGraceDays` | `BASYX_EVENTING_FEED_HARD_DELETE_GRACE_DAYS` | `10`; additional time before expired rows are physically deleted. `0` removes the grace period. |
| `eventing.feed.maxPageSize` | `BASYX_EVENTING_FEED_MAX_PAGE_SIZE` | `100`; default and maximum `limit`. |
| `eventing.feed.sourceBaseUrl` | `BASYX_EVENTING_FEED_SOURCE_BASE_URL` | Compatibility override for the event source base URL. Prefer shared `eventing.sourceBaseUrl`. |
| `eventing.feed.schemaBaseUrl` | `BASYX_EVENTING_FEED_SCHEMA_BASE_URL` | Compatibility override for schema URLs. Prefer shared `eventing.schemaBaseUrl`. |
| `eventing.feed.cleanupIntervalHours` | `BASYX_EVENTING_FEED_CLEANUP_INTERVAL_HOURS` | `24`; interval between physical retention cleanup runs. Cleanup also runs at startup. |
| `eventing.feed.publishIntervalMillis` | `BASYX_EVENTING_FEED_PUBLISH_INTERVAL_MILLIS` | `250`; interval for assigning committed events their feed order. It affects visibility latency, not mutation durability. |

### Read and Resume

Without a filter or checkpoint, `GET /events` scans from the earliest retained events in publication order; records within each returned page are sorted chronologically. Reading is non-destructive. Follow the opaque `cursor` until the response no longer contains one. A cursor preserves the original `since`, `filter`, and `presentation`; omit those parameters on subsequent requests or repeat the same values.

Use `lastEventId` to resume after an event that the consumer has processed. Resume operations can replay events, so consumers must deduplicate by CloudEvents `id`. Use `since` as an inclusive RFC 3339 timestamp filter for an initial query. It cannot be combined with `lastEventId`, and it is not a durable polling checkpoint: a transaction can commit later with an earlier mutation time.

The response's `updated` value is the newest mutation timestamp in that page, not a continuation token. Events eventually leave the feed according to retention settings; after a retention gap, read current state from the Repository APIs before resuming event processing.

`REGULAR` is the default presentation and returns the regular payload. `COMPACT` returns its identification subset; PCN compact events omit `record`. `FULL` is accepted as a deprecated compatibility alias for `REGULAR`.

### Filter Events

The `filter` parameter supports RSQL with the prefix `rsql:`. Supported fields are `event.type`, `event.subject`, `event.source`, and `event.dataschema`. Supported operators are `==`, `!=`, `=in=`, and `=out=`. Semicolon means AND, comma means OR, AND has higher precedence, and parentheses group expressions. Expressions are limited to 16 KiB and 32 levels of nesting.

For example, read compact events for one Submodel:

```bash
curl --get 'https://example.com/api/v3/events' \
  --data-urlencode 'filter=rsql:event.subject==urn:example:submodel:1' \
  --data-urlencode 'presentation=COMPACT' \
  --data-urlencode 'limit=10'
```

Filtering `data.*` fields is not supported. Quote values containing reserved RSQL characters.

## MQTT 5

Enable broker delivery with the common Eventing switches and select the MQTT sink:

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  enabled: true
  format: cloudevents
  sinks: [mqtt]
  outboxEnabled: true
  topicPrefix: basyx
  mqtt:
    broker: mqtt://localhost:1883
    clientId: basyx-instance-1
```

`eventing.enabled`, a `mqtt` entry in `eventing.sinks`, and `eventing.outboxEnabled` are all required. Each message contains one regular CloudEvent. MQTT 5 Content Type is `application/cloudevents+json`.

| MQTT setting | Environment variable | Default or requirement |
| --- | --- | --- |
| `eventing.mqtt.broker` | `BASYX_EVENTING_MQTT_BROKER` | Required `mqtt://host:port` or `tls://host:port`; do not embed credentials. |
| `eventing.mqtt.clientId` | `BASYX_EVENTING_MQTT_CLIENT_ID` | Required and unique for each process connected to the broker. |
| `eventing.mqtt.sinkId` | `BASYX_EVENTING_MQTT_SINK_ID` | `mqtt`; stable outbox destination identifier. |
| `eventing.mqtt.qos` | `BASYX_EVENTING_MQTT_QOS` | `1`; accepts `0`, `1`, or `2`. |
| `eventing.mqtt.retained` | `BASYX_EVENTING_MQTT_RETAINED` | `false`; when enabled, the broker retains only the latest message for each topic. |
| `eventing.mqtt.username`, `password` | `BASYX_EVENTING_MQTT_USERNAME`, `BASYX_EVENTING_MQTT_PASSWORD` | Optional broker credentials. |
| `eventing.mqtt.usernameFile`, `passwordFile` | `BASYX_EVENTING_MQTT_USERNAME_FILE`, `BASYX_EVENTING_MQTT_PASSWORD_FILE` | Mounted alternatives to inline credentials. Do not configure both forms for one value. |
| `eventing.mqtt.caFile` | `BASYX_EVENTING_MQTT_CA_FILE` | Optional private CA bundle for `tls://`; otherwise system trust is used. |
| `eventing.mqtt.certificateFile`, `keyFile` | `BASYX_EVENTING_MQTT_CERTIFICATE_FILE`, `BASYX_EVENTING_MQTT_KEY_FILE` | Optional client certificate and key pair for mutual TLS. |

`eventing.topicPrefix` is configured through `BASYX_EVENTING_TOPIC_PREFIX` and defaults to `basyx`.

| Event family | Default topic |
| --- | --- |
| AAS | `basyx/aasrepository/aas/{created,updated,deleted}` |
| Asset | `basyx/aasrepository/asset/{created,updated,deleted}` |
| Submodel | `basyx/submodelrepository/submodel/{created,updated,deleted}` |
| PCN | `basyx/submodelrepository/pcn/notification` |

QoS 1 and 2 wait for broker acknowledgement and provide at-least-once delivery from BaSyx. A process failure after acknowledgement but before outbox cleanup can cause the same event ID to be delivered again. QoS 0 has no broker acknowledgement and weakens this guarantee.

## Kafka

Provision the topic before starting BaSyx, then configure the Kafka sink:

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  enabled: true
  format: cloudevents
  sinks: [kafka]
  outboxEnabled: true
  kafka:
    brokers: [localhost:9092]
    topic: basyx.events
```

| Kafka setting | Environment variable | Default or requirement |
| --- | --- | --- |
| `eventing.kafka.brokers` | `BASYX_EVENTING_KAFKA_BROKERS` | Required bootstrap `host:port` list; comma-separated in the environment. |
| `eventing.kafka.topic` | `BASYX_EVENTING_KAFKA_TOPIC` | `basyx.events`; receives all event families. |
| `eventing.kafka.sinkId` | `BASYX_EVENTING_KAFKA_SINK_ID` | `kafka`; stable outbox destination identifier. |
| `eventing.kafka.clientId` | `BASYX_EVENTING_KAFKA_CLIENT_ID` | `basyx`. |
| `eventing.kafka.producerBatchMaxBytes` | `BASYX_EVENTING_KAFKA_PRODUCER_BATCH_MAX_BYTES` | `0` uses the client default. Align larger values with broker and topic message limits. |
| `eventing.kafka.tlsEnabled` | `BASYX_EVENTING_KAFKA_TLS_ENABLED` | `false`; enables TLS 1.2 or later. |
| `eventing.kafka.caFile`, `certificateFile`, `keyFile` | `BASYX_EVENTING_KAFKA_CA_FILE`, `BASYX_EVENTING_KAFKA_CERTIFICATE_FILE`, `BASYX_EVENTING_KAFKA_KEY_FILE` | Optional private CA and mutual-TLS material. |
| `eventing.kafka.saslMechanism` | `BASYX_EVENTING_KAFKA_SASL_MECHANISM` | Empty disables SASL; supports `PLAIN`, `SCRAM-SHA-256`, and `SCRAM-SHA-512`. |
| `eventing.kafka.username`, `password` | `BASYX_EVENTING_KAFKA_USERNAME`, `BASYX_EVENTING_KAFKA_PASSWORD` | Required together when SASL is enabled. |
| `eventing.kafka.usernameFile`, `passwordFile` | `BASYX_EVENTING_KAFKA_USERNAME_FILE`, `BASYX_EVENTING_KAFKA_PASSWORD_FILE` | Mounted alternatives to inline credentials. |

Kafka record values are unchanged structured CloudEvents and carry `content-type: application/cloudevents+json`. Records use the key `aas_history:<AAS ID>` or `submodel_history:<Submodel ID>`; related asset and PCN events share their parent entity's key.

Kafka acknowledges a delivery only after all in-sync replicas acknowledge it. Delivery is at least once, so deduplicate by event ID. Events for one entity use the same key and remain ordered while the topic's partition count is stable. There is no ordering guarantee across partitions.

## AMQP 1.0

Provision the target address before starting BaSyx. This minimal example targets a queue exposed through AMQP 1.0:

```yaml
general:
  externalUrl: "https://example.com/api/v3"
eventing:
  enabled: true
  format: cloudevents
  sinks: [amqp]
  outboxEnabled: true
  amqp:
    broker: amqp://localhost:5672
    address: /queues/basyx.events
```

| AMQP setting | Environment variable | Default or requirement |
| --- | --- | --- |
| `eventing.amqp.broker` | `BASYX_EVENTING_AMQP_BROKER` | Required `amqp://host[:port]` or `amqps://host[:port]`. |
| `eventing.amqp.address` | `BASYX_EVENTING_AMQP_ADDRESS` | Required AMQP target address. BaSyx does not create queues, exchanges, or bindings. |
| `eventing.amqp.sinkId` | `BASYX_EVENTING_AMQP_SINK_ID` | `amqp`; stable outbox destination identifier. |
| `eventing.amqp.hostName` | `BASYX_EVENTING_AMQP_HOST_NAME` | Optional AMQP connection hostname. With RabbitMQ, `vhost:<name>` selects a virtual host; TLS still verifies the broker's network hostname. |
| `eventing.amqp.username`, `password` | `BASYX_EVENTING_AMQP_USERNAME`, `BASYX_EVENTING_AMQP_PASSWORD` | Optional SASL PLAIN credentials; configure both. |
| `eventing.amqp.usernameFile`, `passwordFile` | `BASYX_EVENTING_AMQP_USERNAME_FILE`, `BASYX_EVENTING_AMQP_PASSWORD_FILE` | Mounted alternatives to inline credentials. |
| `eventing.amqp.caFile` | `BASYX_EVENTING_AMQP_CA_FILE` | Optional private CA bundle for `amqps`. |
| `eventing.amqp.certificateFile`, `keyFile` | `BASYX_EVENTING_AMQP_CERTIFICATE_FILE`, `BASYX_EVENTING_AMQP_KEY_FILE` | Optional mutual-TLS certificate and key pair. |

The AMQP 1.0 data section contains the structured CloudEvent, the content type is `application/cloudevents+json`, and messages are marked durable. Only an AMQP `Accepted` outcome clears the pending outbox entry. Rejected, released, modified, failed, or ambiguous deliveries remain pending and are retried. Delivery is at least once; deduplicate by event ID. BaSyx preserves its per-entity outbox order, but consumer concurrency and broker redelivery can affect observed processing order.

This sink implements AMQP 1.0, not AMQP 0-9-1. Broker-specific address conventions, permissions, and durability settings remain the operator's responsibility.

## Transactional Delivery and Outbox

Event creation and the model mutation use the same PostgreSQL transaction. If that transaction rolls back, neither the model change nor its Event Feed/outbox records are committed. A failure to write the required event record also rolls back the mutation.

Broker publication occurs after commit. If a broker is unavailable, validly configured services can continue accepting model mutations while pending deliveries remain in PostgreSQL. Failed deliveries retry indefinitely with exponential backoff and jitter, starting at one second and capped at one minute. Pending broker deliveries do not expire.

Delivery is ordered per mutated AAS or Submodel. A failed event blocks later events for the same entity while unrelated entities can progress. Acknowledged entries are removed from the outbox. The resulting guarantee is at least once, not exactly once: consumers must deduplicate using `id`.

Each configured transport has an independent queue identified by its `sinkId`. Sinks used together must have distinct IDs. Replicas sharing a database should use the same sink ID and destination settings; MQTT client IDs must still be unique per process. Drain pending deliveries before changing a sink ID, broker, topic, address, or other routing settings.

The REST Event Feed uses separate retained storage. Reading it never acknowledges or removes broker outbox entries, and feed retention does not expire pending broker deliveries.

## Security

The REST Event Feed inherits authentication and authorization from the hosting service; it has no separate authentication model. With ABAC disabled, it has the same access boundary as the hosting service. With ABAC enabled, callers need `READ` access to the feed and schema routes, and every returned event is checked against the resources represented in its payload.

AAS events require unrestricted read access to the AAS. Submodel and PCN events require unrestricted read access to the Submodel and, when asset identifiers are included, to every contributing AAS. Asset events require access to the owning AAS. If the service cannot establish access to all information in an event, including because row or field restrictions apply, it hides the complete event.

HTTP ABAC does not filter MQTT, Kafka, or AMQP subscribers. Broker consumers receive whatever their broker identity and topic/address permissions permit. Protect broker delivery with TLS where appropriate, secret-backed credentials, and least-privilege publish and subscribe ACLs. Transport TLS configuration requires TLS 1.2 or later. Treat event payloads and identifiers as Repository data when designing broker authorization.

## Public URLs and Schemas

Configure `general.externalUrl` with the public HTTP(S) API base URL, including any reverse-proxy context path. It supplies the default CloudEvents source and hosted schema URLs. `eventing.sourceBaseUrl` (`BASYX_EVENTING_SOURCE_BASE_URL`) and `eventing.schemaBaseUrl` (`BASYX_EVENTING_SCHEMA_BASE_URL`) override those values for Eventing.

Source selection uses the shared Eventing override, then the feed-specific compatibility override, then the first `general.externalUrl`, and finally the configured local server URL and context path. Unless overridden, schema URLs use the selected source followed by `/.well-known/event-feed/schemas`. These URLs are generated from configuration, not incoming request host headers, so explicit public values are important behind reverse proxies. A custom schema base URL must serve the same versioned schema documents advertised by the events.

## Observability

Broker outbox workers expose the following OpenTelemetry metrics with a `sink` attribute:

| Metric | Meaning |
| --- | --- |
| `basyx.eventing.delivered` | Broker-acknowledged deliveries |
| `basyx.eventing.delivery.failures` | Failed delivery attempts or worker database failures |
| `basyx.eventing.pending` | Pending outbox entries |
| `basyx.eventing.retry.pending` | Pending entries that have already failed at least once |
| `basyx.eventing.pending.oldest.age` | Age in seconds of the oldest pending entry |
| `basyx.eventing.broker.connected` | Latest broker connection state: `1` connected, `0` disconnected |

Queue gauges refresh every 15 seconds. Monitor a growing pending count, increasing oldest-event age, persistent failures, and broker connectivity. See [Observability](observability) for OpenTelemetry configuration.

## Runnable Examples

- [Event Feed example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxEventFeedExample)
- [MQTT example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxMQTTExample)
- [Kafka example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxKafkaExample)
- [AMQP example](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxAMQPExample)

Each example provides a runnable local topology and a smoke test for its delivery mechanism.
