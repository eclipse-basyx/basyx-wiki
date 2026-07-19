# MQTT Eventing

The AAS Repository can publish hierarchical MQTT events for repository operations and operations on an individual Asset Administration Shell.

```{warning}
Starting with **BaSyx Java Server SDK Milestone 14**, MQTT uses canonical topics with unpadded UTF-8 Base64URL-encoded identifier segments. Submodel-reference topics no longer contain the raw submodel identifier, and AAS service topics no longer contain a raw or URL-percent-encoded shell identifier.

This is a breaking subscription change. Events are not also published on the legacy topics, so existing subscribers must update their topic filters when upgrading to Milestone 14.
```

## Configuration

Enable MQTT eventing in the standalone AAS Repository component with:

```properties
basyx.aasrepository.feature.mqtt.enabled=true
mqtt.clientId=aas-repository
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
| `basyx.aasrepository.feature.mqtt.enabled=true` | AAS repository events; this module is included in the standalone AAS Repository component |
| `basyx.aasservice.feature.mqtt.enabled=true` | Events for operations on an individual AAS; add `basyx.aasservice-feature-mqtt` when composing a custom SDK application |
| `basyx.feature.mqtt.enabled=true` | Every MQTT feature available on the application's classpath |

## Topic placeholders

| Placeholder | Meaning |
| --- | --- |
| `$repoId` | Repository name configured with `basyx.aasrepo.name`; it is not encoded |
| `$shellIdBase64Url` | AAS identifier encoded as unpadded UTF-8 Base64URL |
| `$submodelIdBase64Url` | Submodel identifier encoded as unpadded UTF-8 Base64URL |

For example, the identifier `https://example.com/aas/1` becomes `aHR0cHM6Ly9leGFtcGxlLmNvbS9hYXMvMQ`. Base64URL uses `-` and `_` instead of `+` and `/` and omits trailing `=` padding.

## AAS repository events

| Event | Topic | Payload |
| --- | --- | --- |
| AAS created | `aas-repository/$repoId/shells/created` | Created AAS JSON |
| AAS updated | `aas-repository/$repoId/shells/updated` | Updated AAS JSON |
| AAS deleted | `aas-repository/$repoId/shells/deleted` | Deleted AAS JSON |
| Submodel reference created | `aas-repository/$repoId/shells/submodels/$submodelIdBase64Url/created` | Created AAS JSON |
| Submodel reference deleted | `aas-repository/$repoId/shells/submodels/$submodelIdBase64Url/deleted` | Deleted AAS JSON |

## AAS service events

These events are provided by the Java SDK's `basyx.aasservice-feature-mqtt` module. When composing a custom application with this module, enable it with `basyx.aasservice.feature.mqtt.enabled=true` or the global switch described above. The module is not bundled in the standalone AAS Repository component.

| Event | Topic | Payload |
| --- | --- | --- |
| Asset information set | `aas-repository/$repoId/shells/$shellIdBase64Url/assetInformation/updated` | Updated AssetInformation JSON |
| Submodel reference added | `aas-repository/$repoId/shells/$shellIdBase64Url/submodelReferences/created` | Created SubmodelReference JSON |
| Submodel reference removed | `aas-repository/$repoId/shells/$shellIdBase64Url/submodelReferences/deleted` | Deleted SubmodelReference JSON |

## Milestone 14 migration

| Event | Before Milestone 14 | Starting with Milestone 14 |
| --- | --- | --- |
| Repository submodel-reference create/delete | Raw submodel ID in the topic | `$submodelIdBase64Url` |
| AAS service operations | Raw or URL-percent-encoded shell ID | `$shellIdBase64Url` |

Repository names remain unchanged. A broad subscriber can use `aas-repository/$repoId/#`; consumers that parse identifier segments must Base64URL-decode the relevant segment as UTF-8.

![MQTT Feature](./images/mqtt-feature.png)
