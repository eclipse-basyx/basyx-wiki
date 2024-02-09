# Storage Backend

## User Story & Use Case
*As AAS Components user*

*I want to configure the persistency backend*

*so that I can easily change where AAS/Submodels are stored and, depending on the backend, no data gets lost*


By using different kind of backends, the persistency layer of the AAS Server component can be tailored to specific use cases' needs.

## Feature Overview
The AAS Server components provides a default InMemory backend that can be utilized for development but does not persist any data between component starts. For use in production, additionally MongoDB support is provided.

Depending on the backend chosen, addition configuration may be necessary.

## Feature Configuration
By default, an empty InMemory server is started. The backend can be changed with the option

```
aas.backend=InMemory
```
Currently, the other valid option for the backend is **MongoDB** that persists the whole AAS together with its submodels in a MongoDB. If MongoDB is chosen as backend, the MongoDB backend connection has to be configured via [mongodb.properties file](../../mongodb.md).