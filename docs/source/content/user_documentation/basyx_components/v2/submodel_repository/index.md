# Submodel Repository

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-repository)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

## Features
- [Authorization](./features/authorization.md)

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

```properties
basyx.cors.allowed-origins=http://localhost:3000, http://localhost:4000
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


```{toctree}
:hidden:
:maxdepth: 1

features/registry-integration
features/operation-delegation
features/authorization
features/mqtt
```