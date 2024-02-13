# Hierarchical MQTT Eventing
## User Story & Use Case
>As AAS Components user
>I want hierarchical MQTT topics in the AAS Registry Component
>so that I can subscribe precisely to the topics of interest without having to filter on client side

MQTT supports hierarchical topics with [wildcard subscription support](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/). For example, if the topics *a/b/x* and *a/b/y* exist, subscribing to *a/b/+* subscribes to all events broadcasted on both topics.

## Feature Overview
The following hierarchical topics with their respective payloads are implemented:

* aas-registry/<reg-id>/shells/created
* aas-registry/<reg-id>/shells/updated
   * Payload: New AAS-Descriptor

* aas-registry/<reg-id>/shells/removed
   * payload: Old AAS-Descriptor

* aas-registry/<reg-id>/submodels/added
* aas-registry/<reg-id>/submodels/updated
   * Payload: New SM-Descriptor

* aas-registry/<reg-id>/submodels/deleted
   * Payload: Old SM-Descriptor

* aas-registry/<reg-id>/shells/<encoded-aas-identifier>/submodels/added
* aas-registry/<reg-id>/shells/<encoded-aas-identifier>/submodels/deleted
   * Payload: New SM-Descriptor

* /aas-registry/<reg-id>/shells/<encoded-aas-identifier>/submodels/deleted
   * Payload: Old SM-Descriptor

For AAS-Identifier encoding, [Base64URL encoding](https://www.base64url.com) and [URL encoding](https://en.wikipedia.org/wiki/Percent-encoding) are available.

## Feature Configuration
The feature can be configured in the *registry.properties* file by setting *registry.events = MQTTV2* for Base64URL encoding or *registry.events = MQTTV2_SIMPLE_ENCODING* for URL encoding. Additionally, the Registry id needs to be configured via *registry.id = <repo-id>.*

An example configuration for this feature could be:
```
registry.events = MQTTV2
registry.id = product-aas-registry
```
The MQTT broker connectivity is configured via [mqtt.properties](../../mqtt.md)