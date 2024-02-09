# Storage Backend

## User Story & Use Case
*As AAS Components user*

*I want to configure the persistency backend*

*so that I can easily change where AAS/Submodels Descriptors are stored and, depending on the backend, no data gets lost*


By using different kind of backends, the persistency layer of the AAS Registry component can be tailored to specific use cases' needs.

## Feature Overview
The AAS Registry components provides a default InMemory backend that can be utilized for development but does not persist any data between component starts. For use in production, additionally MongoDB and SQL support is provided.

Depending on the backend chosen, addition configuration may be necessary.

## Feature Configuration
By default, an empty InMemory server is started. The backend can be changed in the registry.properties with the option

```
registry.backend=InMemory
```
Currently, the other valid option for the backend is **MongoDB** and **SQL**.

If MongoDB or SQL is chosen as backend, the MongoDB connection has to be configured via mongodb.properties file for MongoDB or sql.properties file for SQL.