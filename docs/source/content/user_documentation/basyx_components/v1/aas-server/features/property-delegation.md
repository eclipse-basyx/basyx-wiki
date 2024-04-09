# Property Delegation
## User Story & Use Case
*As data integrator*

*I want to delegate property value retrieval to arbitrary endpoints with a defined interface*

*so that I can integrate arbitrary third-party data sources by creating gateways*


This feature enables easy integration of third-party HTTP/REST data sources and is a central building block to the Delegator approach utilized by the [BaSyx DataBridge](https://github.com/eclipse-basyx/basyx-databridge) . If a non HTTP/REST data source needs to be integrated, the BaSyx DataBridge can be used for data integration and data transformation.

## Feature Overview
By annotating properties with Qualifiers containing an HTTP/REST endpoint, the AAS Component is ordered to delegate the property retrieval to the URL contained in the qualifier (see 'Feature Configuration' below for details). This delegation mechanism is completely transparent on all GET endpoints. Please note that a delegated property can not be written as of today.


The HTTP/REST endpoint delegated to is expected to return a value on HTTP-GET that can be directly returned as valid Property value without the need for any transformation.

## Feature Configuration
The delegation feature can be enabled (Enabled) or disabled (Disabled) via the aas.properties file.
```
aas.delegation=Enabled
```
Additional to the overall feature activation, properties need to be annotated via a Qualifier with type delegatedTo and a valid HTTP/REST URL as value.