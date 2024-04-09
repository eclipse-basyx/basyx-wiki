# Simple MQTT Eventing
## User Story & Use Case
>As AAS Components user
>I want simple MQTT topics of the AAS Registry Component
>so that I can receive MQTT events without having to worry about subscribing to detailed topics

If the hierarchical topics presented in [Hierarchical MQTT Eventing](hierarchical-mqtt.md) are too complicated, this feature will support event-driven use cases.

## Feature Overview
Information about what events will be published can be found in the [eventing extension](../../../../developer/basyx_java_v1/extensions/eventing.md).

## Feature Configuration
Eventing via MQTT is disabled by default. It can be enabled in the registry.properties file as well. This will publish events for every action to a separately specified server:
```
registry.events=MQTT
registry.events=None
```
The MQTT broker endpoint can be configured via [**mqtt.properties** file](../../general_configuration/mqtt.md)