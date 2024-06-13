# AAS Environment

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-environment)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The AAS Environment aggregates the AAS Repository, Submodel Repository and ConceptDescription Repository into a single component.

```{note}
Additionally, the AAS Environment supports the following endpoint defined in DotAAS Part 2 V3 - Serialization Interface:
- GenerateSerializationByIds
```

## Features
All Features of the AAS Repository, Submodel Repository and ConceptDescription Repository are also available in the AAS Environment.
### Default Features
These features are always enabled:
- [Upload Endpoint](./features/upload.md) for AASX/JSON/XML files

### Optional Features
These features can be activated in the configuration files as required
- [Authorization Feature](./features/authorization.md)


## Configuration

```{note}
If you are using the AAS Environment, all configuration for the aggregated repositories is done in the AAS Environment configuration.
```

The AAS Environment Component supports the preconfiguration of AAS Packages (XML, JSON, AASX).
- [Preconfiguration of AAS Packages](./features/preconfiguration.md)

### Server Configuration
This section configures the server port and application name for the AAS Environment.
```properties
server.port=8081
spring.application.name=AAS Environment
```

### Backend Configuration ![Default](https://img.shields.io/badge/required-true-red)
Configure the backend storage. By default, it uses InMemory. Optionally, you can configure MongoDB.
#### InMemory ![Default](https://img.shields.io/badge/default-true-blue)
```properties
basyx.backend = InMemory
```
#### MongoDB ![Default](https://img.shields.io/badge/default-false-blue)
```properties
basyx.backend = MongoDB
spring.data.mongodb.host=mongo
spring.data.mongodb.host=127.0.0.1
spring.data.mongodb.port=27017
spring.data.mongodb.database=aasenvironments
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=mongoAdmin
spring.data.mongodb.password=mongoPassword
```
---

### CORS Configuration ![Default](https://img.shields.io/badge/default-false-blue) ![Default](https://img.shields.io/badge/required-false-red)
Configure CORS settings to specify allowed origins and methods.

```{warning}
To use the component with the [BaSyx Web GUI](../../web_ui/index.md) this configuration is required.

To do this, you need to add the URL of the Web GUI to the allowed origins.
```

```properties
basyx.cors.allowed-origins=http://localhost:3000, http://localhost:4000
basyx.cors.allowed-methods=GET,POST,PATCH,DELETE,PUT,OPTIONS,HEAD
```
---

### Authorization Configuration ![Default](https://img.shields.io/badge/default-false-blue) ![Default](https://img.shields.io/badge/required-false-red)
> Enable and configure authorization features, such as Role-Based Access Control (RBAC) and JWT Bearer Token Provider.
```properties
basyx.feature.authorization.enabled = true
basyx.feature.authorization.type = rbac
basyx.feature.authorization.jwtBearerTokenProvider = keycloak
basyx.feature.authorization.rbac.file = classpath:rbac_rules.json
spring.security.oauth2.resourceserver.jwt.issuer-uri= http://localhost:9096/realms/BaSyx

```
---

### Operation Delegation ![Default](https://img.shields.io/badge/default-true-blue) ![Default](https://img.shields.io/badge/required-false-red)
> For configration, see and utilize the [Submodel Repository Configuration](../submodel_repository/index.md) and the [AAS Repository Configuration](../aas_repository/index.md).

---

### MQTT Configuration ![Default](https://img.shields.io/badge/default-false-blue) ![Default](https://img.shields.io/badge/required-false-red)
> For configration, see and utilize the [Submodel Repository Configuration](../submodel_repository/index.md) and the [AAS Repository Configuration](../aas_repository/index.md)

---

### File Upload Configuration ![Default](https://img.shields.io/badge/default-true-blue) ![Default](https://img.shields.io/badge/required-false-red)
> Set the maximum file size and request size for file uploads. The default values are 1 MB for file size and 10 MB for request size.
```properties
spring.servlet.multipart.max-file-size=128KB
spring.servlet.multipart.max-request-size=128KB
```
---

## Docker

Eclipse BaSyx provides the AAS Environment as off-the-shelf component via DockerHub. The following command pulls the image and creates a container for the AAS Environment:

```bash
docker run --name=aas-env -p:8081:8081 -v C:/tmp/application.properties:/application/application.properties eclipsebasyx/aas-environment:2.0.0-SNAPSHOT
```

## Swagger UI
In the Swagger UI, you can find the API documentation for the AAS Environment.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoint is available at:

	http://{host}:{port}/swagger-ui/index.html
