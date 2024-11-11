# Concept Description Repository

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/conceptdescription-repository)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The ConceptDescription Repository is a component that provides a REST API to interact with ConceptDescriptions. It allows the creation, retrieval, update, and deletion of ConceptDescriptions.

## Features
- [Authorization](./features/authorization.md)

## Configuration

### Server Configuration
The following shows how to configure the server port, application name and ConceptDescription Repository Name.

```properties
server.port = 8081
spring.application.name = Concept Description Repository
basyx.cdrepo.name = cd-repo
```

### Backend Configuration ![Default](https://img.shields.io/badge/required-true-red)
By default, it uses InMemory. Optionally, you can configure MongoDB.

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
spring.data.mongodb.database=conceptdescription
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
basyx.cors.allowed-origins = http://localhost:3000, https://my-url/*
basyx.cors.allowed-methods = GET,POST,PATCH,DELETE,PUT,OPTIONS,HEAD
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
```{note}
A favicon is a small 16×16 or 32×32 pixel icon, symbol or logo used by web browsers to identify a website in a recognizable way
```
To configure the favicon, mount your favicon to the `static` directory of the component using Docker:
```
docker run --name=cd-repo -p:8081:8081 -v C:/path/to/favicon.ico:/application/static/favicon.ico eclipsebasyx/conceptdescription-repository:2.0.0-SNAPSHOT
```
or
```yaml
aas-env:
    image: eclipsebasyx/conceptdescription-repository:2.0.0-SNAPSHOT
    container_name: cd-repo
    volumes:
      - ./basyx/cd-repo.properties:/application/application.properties
	  - ./basyx/static/favicon.ico:/application/static/favicon.ico
    ports:
      - '8081:8081'
```

## Docker

Eclipse BaSyx provides the Concept Description Repository as off-the-shelf component via DockerHub. The following command pulls the image and starts a container for the ConceptDescription Repository:

```bash
docker run --name=cd-repo -p:8081:8081 -v C:/path/to/application.properties:/application/application.properties eclipsebasyx/conceptdescription-repository:2.0.0-SNAPSHOT
```

## Virtual Machine
Eclipse BaSyx provides the Concept Description Repository as a virtual machine image for Oracle VirtualBox and VMware Workstation Player. 

The image can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu). How to use it is described [here](../../../user_tutorials/virtualmachines/alpine_virtualmachine_setup_use.md).

## Swagger UI
In the Swagger UI, you can find the API documentation for the Concept Description Repository.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoints is available at:

	http://{host}:{port}/swagger-ui/index.html



```{toctree}
:hidden:
:maxdepth: 1

features/authorization
```
