# Hierarchical MQTT Eventing
## User Story & Use Case
*As AAS Components user*

*I want hierarchical MQTT topics in the AAS Server Component*

*so that I can subscribe precisely to the topics of interest without having to filter on client side*


MQTT supports hierarchical topics with [wildcard subscription support](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/). For example, if the topics *a/b/x* and *a/b/y* exist, subscribing to *a/b/+* subscribes to all events broadcasted on both topics.


Please note, that this feature can not be combined with lambda properties due to them being only updated on query.

## Feature Overview
The following hierarchical topics with their respective payloads are implemented:

* aas-repository/<repo-id>/shells/created
    * Payload: Complete AAS (without ConceptDictionaries)
* aas-repository/<repo-id>/shells/deleted
    * Payload: Complete AAS (old, without ConceptDictionaries)
* aas-repository/<repo-id>/shells/updated
    * Payload: Complete AAS (without ConceptDictionaries)


* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/created
    * Payload: Submodels without SMEs
* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/deleted
    * Payload: Submodels without SMEs
* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/updated
    * Payload: Submodels without SMEs


* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/<encoded-sm-identifier>/submodelElements/<idShortPath>/created
    * Payload: SME without value (or value-equivalent)
* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/<encoded-sm-identifier>/submodelElements/<idShortPath>/deleted
    * Payload: old SME without value (or value-equivalent)
* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/<encoded-sm-identifier>/submodelElements/<idShortPath>/updated
    * Payload: SME without value (or value-equivalent)
* aas-repository/<repo-id>/shells/<encoded-aas-identifier>/submodels/<encoded-sm-identifier>/submodelElements/<idShortPath>/value
    * SME value, if not specified otherwise via qualifier


For AAS/SM-Identifier encoding, [Base64URL encoding](https://www.base64url.com) and [URL encoding](https://en.wikipedia.org/wiki/Percent-encoding) are available.

## Feature Configuration
The feature can be configured in the aas.properties file by setting aas.events = *MQTTV2* for Base64URL encoding or *aas.events = MQTTV2_SIMPLE_ENCODING* for URL encoding. Additionally, the repo id needs to be configured via *aas.id = <repo-id>*.

An example configuration for this feature could be:
```
aas.events = MQTTV2
aas.id = product-aas-repo
```
The MQTT broker connectivity is configured via [mqtt.properties](../../mqtt.md)

Additional to the overall event configuration, the payload send on the *../value* topic for updating a SubmodelElement's value can be tailored. For SubmodelElements containing huge values like Blobs, it may be sensible to disable sending their value's content. If this is the case, a qualifier with type *emptyValueUpdateEvent* and value set to *true* will configure empty value updates for the specific SubmodelElement (cf. [ObservableSubmodelAPIV2Helper](https://github.com/eclipse-basyx/basyx-java-sdk/blob/development/src/main/java/org/eclipse/basyx/submodel/restapi/observing/ObserableSubmodelAPIV2Helper.java#L62)).