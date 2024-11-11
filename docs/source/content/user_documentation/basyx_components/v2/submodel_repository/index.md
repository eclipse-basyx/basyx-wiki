# Submodel Repository

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-repository)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The Submodel Repository is a component that provides a REST API to interact with Submodels. It allows the creation, retrieval, update, and deletion of Submodels.

## Features
- [Authorization](./features/authorization.md)
- [MQTT](./features/mqtt.md)
- [Operation Delegation](./features/operation-delegation.md)
- [Registry Integration](./features/registry-integration.md)

## Configuration
### Server Configuration ![Required](https://img.shields.io/badge/required-true-red)
This section configures the server port, application name and Submodel Repository Name for the Submodel Repository.
```properties
server.port=8081

spring.application.name=Submodel Repository
basyx.smrepo.name = sm-repo
```
---

### Backend Configuration ![Required](https://img.shields.io/badge/required-true-red)
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
spring.data.mongodb.database=submodels
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=mongoAdmin
spring.data.mongodb.password=mongoPassword
```
---


### CORS Configuration ![Default](https://img.shields.io/badge/default-false-blue) ![Required](https://img.shields.io/badge/required-false-red)
Configure CORS settings to specify allowed origins and methods.

```{warning}
To use the component with the [BaSyx Web GUI](../../web_ui/index.md) this configuration is required.

To do this, you need to add the URL of the Web GUI to the allowed origins.
```

This is what an example configuration looks like:

```properties
basyx.cors.allowed-origins=http://localhost:3000, https://my-url/*
basyx.cors.allowed-methods=GET,POST,PATCH,DELETE,PUT,OPTIONS,HEAD
```
---

### [Authorization](./features/authorization.md) ![Default](https://img.shields.io/badge/default-false-blue) ![Required](https://img.shields.io/badge/required-false-red)
Enable and configure authorization features, such as Role-Based Access Control (RBAC) and JWT Bearer Token Provider.
```properties
basyx.feature.authorization.enabled = true
basyx.feature.authorization.type = rbac
basyx.feature.authorization.jwtBearerTokenProvider = keycloak
basyx.feature.authorization.rbac.file = classpath:rbac_rules.json
spring.security.oauth2.resourceserver.jwt.issuer-uri= http://localhost:9096/realms/BaSyx

```
---

### [Registry Integration](./features/registry-integration.md) ![Required](https://img.shields.io/badge/default-false-blue) ![Default](https://img.shields.io/badge/required-false-red)
These settings allow the configuration of registry integration and the external URL of the repository.
```properties
basyx.submodelrepository.feature.registryintegration = http://localhost:8060
basyx.externalurl = http://localhost:8081
```
---

### [MQTT configuration](./features/mqtt.md)
This section provides the configuration for enabling MQTT.

```properties
basyx.submodelrepository.feature.mqtt.enabled = true
mqtt.clientId=TestClient
mqtt.hostname = localhost
mqtt.port = 1883
```
---

### [Operation Delegation](./features/operation-delegation.md) ![Required](https://img.shields.io/badge/default-true-blue) ![Default](https://img.shields.io/badge/required-false-red)
This feature is enabled by default and to disable this the following property should be defined:
```properties
basyx.submodelrepository.feature.operation.delegation.enabled = false
```

## Docker

Eclipse BaSyx provides the Submodel Repository as off-the-shelf component via DockerHub. The following command pulls the image and creates a container for the Submodel Repository:

```bash
docker run --name=sm-repo -p:8081:8081 -v C:/path/to/application.properties:/application/application.properties eclipsebasyx/submodel-repository:2.0.0-SNAPSHOT
```

## Virtual Machine
Eclipse BaSyx provides the Submodel Repository as a virtual machine image for Oracle VirtualBox and VMware Workstation Player. 

The image can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu). How to use it is described [here](../../../user_tutorials/virtualmachines/alpine_virtualmachine_setup_use.md).

## Swagger UI
In the Swagger UI, you can find the API documentation for the Submodel Repository.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoints is available at:

	http://{host}:{port}/swagger-ui/index.html

```{toctree}
:hidden:
:maxdepth: 1

features/registry-integration
features/operation-delegation
features/authorization
features/mqtt
```