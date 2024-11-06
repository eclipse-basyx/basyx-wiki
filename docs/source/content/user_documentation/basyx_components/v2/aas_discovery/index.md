# AAS Discovery Service

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-discovery)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The AAS Discovery Service allows searching for Asset IDs of corresponding Asset Administration Shells, as well as finding Asset Administration Shell IDs based on given Asset IDs.

This is useful when working with the [Hierachical Structures enabling Bills of Material Submodel](https://industrialdigitaltwin.org/wp-content/uploads/2023/04/IDTA-02011-1-0_Submodel_HierarchicalStructuresEnablingBoM.pdf). You will be able to easily find and navigate to the Asset Administration Shells of the assets included in this Submodel.

## Features
- [Authorization](./features/authorization.md)

## Configuration

### Server Configuration ![Default](https://img.shields.io/badge/required-true-red)
This section configures the server port and application name for the AAS Environment.
```properties
server.port=8081
spring.application.name=AAS Discovery
```
---

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
spring.data.mongodb.database=aasdiscovery
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

Enable and configure authorization features, such as Role-Based Access Control (RBAC) and JWT Bearer Token Provider.
```json
{
  "basyx.feature.authorization.enabled": true,
  "basyx.feature.authorization.type": "<The type of authorization to enable>",
  "basyx.feature.authorization.jwtBearerTokenProvider": "<The Jwt token provider>",
  "basyx.feature.authorization.rbac.file": "<Class path of the Rbac rules file if authorization type is rbac>",
  "spring.security.oauth2.resourceserver.jwt.issuer-uri": "<URI of the resource server>"
}
```
---

### Configure Favicon
```{note}
A favicon is a small 16×16 or 32×32 pixel icon, symbol or logo used by web browsers to identify a website in a recognizable way
```
To configure the favicon, mount your favicon to the `static` directory of the component using Docker:
```
docker run --name=aas-discovery-service -p:8081:8081 -v C:/path/to/favicon.ico:/application/static/favicon.ico eclipsebasyx/aas-discovery:2.0.0-SNAPSHOT
```

## Docker
Eclipse BaSyx provides the Aas Discovery Service as off-the-shelf component:

docker run --name=aas-discovery-service -p:8081:8081 -v C:/tmp/application.properties:/application/application.properties eclipsebasyx/aas-discovery:2.0.0-SNAPSHOT 

```{note}
In this example, configuration files are located in `C:/tmp`
```

```{warning}
The binding of volume `C:/tmp/application.properties` to `/application/application.properties` is tested using Windows Powershell. Other terminals might run into an error.
```

## Virtual Machine
Eclipse BaSyx provides the AAS Discovery Service as a virtual machine image for Oracle VirtualBox and VMware Workstation Player. 

The image can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu). How to use it is described [here](../../../user_tutorials/virtualmachines/alpine_virtualmachine_setup_use.md).

## Swagger UI
In the Swagger UI, you can find the API documentation for the AAS Discovery Service.

You can also execute all the API calls directly from the Swagger UI.

The API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoints is available at:

	http://{host}:{port}/swagger-ui/index.html

It supports DotAAS Part 1 V3 and all HTTP/REST endpoints defined in [DotAAS Part 2 V3 - AasDiscovery Service](https://app.swaggerhub.com/apis/Plattform_i40/DiscoveryServiceSpecification/V3.0.1_SSP-001).
In addition, it supports InMemory as well as MongoDB backends. 

For a configuration example, see [application.properties](https://github.com/eclipse-basyx/basyx-java-server-sdk/basyx.aasdiscoveryservice.component/src/main/resources/application.properties)

Right now, no additional input parameters modifying the output (e.g., cursor, serializationModifier) are supported.

```{toctree}
:hidden:
:maxdepth: 1

features/authorization
```