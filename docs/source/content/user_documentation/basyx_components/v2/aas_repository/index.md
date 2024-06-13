# AAS Repository

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-repository)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

## Features



## Configration

### Server Configuration
This section configures the server port, application name, error path and AAS Repo Name for the AAS Repository.
```properties
server.port=8081
server.error.path=/error
spring.application.name=AAS Repository
basyx.aasrepo.name=aas-repo
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
spring.data.mongodb.database=aas
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=mongoAdmin
spring.data.mongodb.password=mongoPassword
```
---

### [Registry Integration](./features/registry-integration.md)
These settings allow the configuration of registry integration and the external URL of the repository.

To enable this feature, the following two properties should be configured:
```
basyx.aasrepository.feature.registryintegration = {AAS-Registry-Base-Url}
basyx.externalurl = {AAS-Repo-Base-Url}
```

### [MQTT configuration](./features/mqtt.md)
This section provides the configuration for enabling MQTT.

```properties
basyx.aasrepository.feature.mqtt.enabled = true
mqtt.clientId=TestClient
mqtt.hostname = localhost
mqtt.port = 1883
```

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

### [Authorization Configuration](./features/authorization.md) ![Default](https://img.shields.io/badge/default-false-blue) ![Default](https://img.shields.io/badge/required-false-red)
Enable and configure authorization features, such as Role-Based Access Control (RBAC) and JWT Bearer Token Provider.
```properties
basyx.feature.authorization.enabled = true
basyx.feature.authorization.type = rbac
basyx.feature.authorization.jwtBearerTokenProvider = keycloak
basyx.feature.authorization.rbac.file = classpath:rbac_rules.json
spring.security.oauth2.resourceserver.jwt.issuer-uri= http://localhost:9096/realms/BaSyx

```
---

### Configure Favicon
To configure the favicon, mount your favicon to the `static` directory of the component using Docker:
```
docker run --name=aas-repo -p:8081:8081 -v C:/path/to/favicon.ico:/application/static/favicon.ico eclipsebasyx/aas-repository:2.0.0-SNAPSHOT
```
or
```yaml
aas-env:
    image: eclipsebasyx/aas-repository:2.0.0-SNAPSHOT
    container_name: aas-repo
    volumes:
      - ./basyx/aas-repo.properties:/application/application.properties
	  - ./basyx/static/favicon.ico:/application/static/favicon.ico
    ports:
      - '8081:8081'
```

## Docker

Eclipse BaSyx provides the AAS Repository as off-the-shelf component via DockerHub. The following command pulls the image and creates a container for the AAS Repository:

```bash
docker run --name=aas-repo -p:8081:8081 -v C:/path/to/application.properties:/application/application.properties eclipsebasyx/aas-repository:2.0.0-SNAPSHOT
```

## Swagger UI
In the Swagger UI, you can find the API documentation for the AAS Environment.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoint is available at:

	http://{host}:{port}/swagger-ui/index.html


```{toctree}
:hidden:
:maxdepth: 1

features/registry-integration
features/aasxupload
features/authorization
features/mqtt
```