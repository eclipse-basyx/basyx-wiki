# Tagged Directory

## User Story & Use Case
>As AAS Components user>
>I want to tag AAS & Submodel descriptors>
>so that I can search for combinations of tags without the need of exploring the complete AAS & Submodel structure>

The tagged directory enables users to perform a discovery of existing AAS & Submodels based on customizable tags. For example, all AAS representing products can be tagged with >product>.

## Feature Overview
This feature enables users to tag AAS Descriptors & AAS Submodels with customizable tags. Tags are arbitrary strings like *product*, *OPC UA* or *CNC mill*. Both AAS Descriptors and Submodel Descriptors can be retrieved by specifying a set of tags. If multiple tags are specified, only descriptors matching all tags are returned.

The TaggedDirectory feature extends the existing HTTP/REST API of the Registry with additional endpoints for working with tags.

## Feature Configuration
The TaggedDirectory is disabled by default. It can be enabled in the registry.properties:
```
 registry.taggedDirectory=Enabled
```