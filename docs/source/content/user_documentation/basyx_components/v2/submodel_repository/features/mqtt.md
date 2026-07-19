# MQTT Eventing

The Submodel Repository can publish hierarchical MQTT events for repository operations and operations on an individual Submodel.

```{warning}
Starting with **BaSyx Java Server SDK Milestone 14**, several MQTT topics and event behaviors change. Submodel identifiers use unpadded UTF-8 Base64URL encoding, `$value` PATCH events use a dedicated `value/updated` topic, and Submodel Service element topics include the encoded submodel identifier.

This is a breaking subscription change. Events are not also published on the legacy topics, so existing subscribers must update their topic filters when upgrading to Milestone 14. Milestone 14 also adds Submodel Service bulk-patch and attachment events.
```

## Configuration

Enable MQTT eventing in the standalone Submodel Repository component with:

```properties
basyx.submodelrepository.feature.mqtt.enabled=true
mqtt.clientId=submodel-repository
mqtt.hostname=localhost
mqtt.port=1883
```

`mqtt.clientId` must be unique among clients connected to the broker. The connection scheme defaults to `tcp`. The complete connection configuration is:

| Property | Required | Default | Description |
| --- | --- | --- | --- |
| `mqtt.clientId` | Yes | - | MQTT client identifier |
| `mqtt.hostname` | Yes | - | MQTT broker host name |
| `mqtt.port` | Yes | - | MQTT broker port |
| `mqtt.protocol` | No | `tcp` | Connection URI scheme, for example `tcp` or `ws` |
| `mqtt.username` | No | Empty | Broker user name |
| `mqtt.password` | No | Empty | Broker password |

Credentials are applied only when both `mqtt.username` and `mqtt.password` are set. Automatic reconnect is enabled.

The available feature switches are:

| Property | Events enabled |
| --- | --- |
| `basyx.submodelrepository.feature.mqtt.enabled=true` | Submodel repository events; this module is included in the standalone Submodel Repository component |
| `basyx.submodelservice.feature.mqtt.enabled=true` | Events for operations on an individual Submodel; add `basyx.submodelservice-feature-mqtt` when composing a custom SDK application |
| `basyx.feature.mqtt.enabled=true` | Every MQTT feature available on the application's classpath |

## Topic placeholders

| Placeholder | Meaning |
| --- | --- |
| `$repoId` | Repository name configured with `basyx.smrepo.name`; it is not encoded |
| `$submodelIdBase64Url` | Submodel identifier encoded as unpadded UTF-8 Base64URL |
| `$idShortPath` | Dot-separated path to the element; it is not encoded |

For example, the identifier `https://example.com/submodels/temperature` becomes `aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWJtb2RlbHMvdGVtcGVyYXR1cmU`. Base64URL uses `-` and `_` instead of `+` and `/` and omits trailing `=` padding.

For a nested element, `$idShortPath` identifies the actual child, for example `Motor.Measurements.Temperature`. Starting with Milestone 14, nested creation in collections and lists publishes this child path and the created child's JSON payload rather than the parent path and payload.

## Submodel repository events

| Event | Topic | Payload |
| --- | --- | --- |
| Submodel created | `sm-repository/$repoId/submodels/created` | Created Submodel JSON |
| Submodel updated | `sm-repository/$repoId/submodels/updated` | Updated Submodel JSON |
| Submodel deleted | `sm-repository/$repoId/submodels/deleted` | Deleted Submodel JSON |
| SubmodelElement created | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/created` | Created SubmodelElement JSON |
| SubmodelElement replaced | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/updated` | Updated SubmodelElement JSON |
| SubmodelElement value updated | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/value/updated` | Updated SubmodelElement JSON |
| SubmodelElement deleted | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/deleted` | Deleted SubmodelElement JSON |
| SubmodelElements patched | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/patched` | Patched SubmodelElements JSON |
| File value updated | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/attachment/updated` | Updated SubmodelElement JSON |
| File value deleted | `sm-repository/$repoId/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/attachment/deleted` | Deleted SubmodelElement JSON |

The repository name in these topics is the configured `basyx.smrepo.name`, including when authorization, registry-integration, or search decorators are enabled.

## Submodel service events

These events are provided by the Java SDK's `basyx.submodelservice-feature-mqtt` module. When composing a custom application with this module, enable it with `basyx.submodelservice.feature.mqtt.enabled=true` or the global switch described above. The module is not bundled in the standalone Submodel Repository component.

| Event | Topic | Payload |
| --- | --- | --- |
| SubmodelElement created | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/created` | Created SubmodelElement JSON |
| SubmodelElement replaced | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/updated` | Updated SubmodelElement JSON |
| SubmodelElement value updated | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/value/updated` | Updated SubmodelElement JSON |
| SubmodelElement deleted | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/deleted` | Deleted SubmodelElement JSON |
| SubmodelElements patched | `sm-service/submodels/$submodelIdBase64Url/submodelElements/patched` | Patched SubmodelElements JSON |
| File value updated | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/attachment/updated` | Updated SubmodelElement JSON |
| File value deleted | `sm-service/submodels/$submodelIdBase64Url/submodelElements/$idShortPath/attachment/deleted` | Deleted SubmodelElement JSON |

The bulk-patch and file attachment events in this table are new in Milestone 14.

## Payload values

By default, SubmodelElement payloads include the element value. To omit supported value fields from serialized MQTT payloads, add this qualifier to the element:

```json
{
  "type": "emptyValueUpdateEvent",
  "value": "true"
}
```

## Milestone 14 migration

| Event or behavior | Before Milestone 14 | Starting with Milestone 14 |
| --- | --- | --- |
| Submodel Repository `$value` PATCH | `.../$idShortPath/updated` | `.../$idShortPath/value/updated` |
| Submodel Service element events | Topic omitted the submodel identifier | Topic includes `$submodelIdBase64Url` |
| Submodel Service `$value` PATCH | Legacy `updated` topic | `.../$idShortPath/value/updated` |
| Nested element creation | Could publish the parent path and payload or fail after creation | Publishes the created child path and payload |
| Configured repository name with decorators | Could fall back to `sm-repo` | Preserves `basyx.smrepo.name` |
| Submodel Service bulk patch | No MQTT event | `.../submodelElements/patched` |
| Submodel Service attachment update/delete | No MQTT event | `.../attachment/updated` and `.../attachment/deleted` |

A broad subscriber can use `sm-repository/$repoId/#` for repository topics and `sm-service/submodels/+/submodelElements/#` for Submodel Service topics. Consumers that parse submodel identifier segments must Base64URL-decode the segment as UTF-8.

Direct Java callers must also update calls to `MqttSubmodelServiceTopicFactory`: its element create, update, and delete topic methods now require the submodel identifier.
