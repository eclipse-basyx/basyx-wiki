# Submodel Registry

![Docker Pulls (log-mem)](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-registry-log-mem?label=Docker%20Pulls%20(log-mem))
![Docker Pulls (log-mongodb)](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-registry-log-mongodb?label=Docker%20Pulls%20(log-mongodb))
![Docker Pulls (kafka-mem)](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-registry-kafka-mem?label=Docker%20Pulls%20(kafka-mem))
![Docker Pulls (kafka-mongodb)](https://img.shields.io/docker/pulls/eclipsebasyx/submodel-registry-kafka-mongodb?label=Docker%20Pulls%20(kafka-mongodb))
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The Submodel Registry is a server that provides a REST API to register and search for Submodels based on their Submodel descriptors.

The server is based on the [Open-API specification](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRegistryServiceSpecification/V3.0_SSP-001) of the [German Plattform Industrie 4.0](https://www.plattform-i40.de/) and the [IDTA](https://industrialdigitaltwin.org/) in the specification document [Details of the Asset Administration Shell, Part 2](https://industrialdigitaltwin.org/wp-content/uploads/2023/04/IDTA-01002-3-0_SpecificationAssetAdministrationShell_Part2_API.pdf).

## Features

[basyx.submodelregistry-client-native](./features/client-native.md) can be used to interact with the backend to register or unregister descriptors and submodels or perform search operations.

[basyx.submodelregistry-service](./features/service.md) provides the application server to access the submodel descriptor storage and offers an API for REST-based communication.

[basyx.submodelregistry-service-basemodel](./features/service-basemodel.md) provides a base model implementation that should be used if you do not need specific model annotations for your storage. It is used for the in-memory storage implementation and you need to add it explicitly as dependency for your server deployment as it is defined as 'provided' dependency in the [basyx.submodelregistry-service](./features/service.md) POM.

[basyx.submodelregistry-service-basetests](./features/service-basetest.md) provides helper classes and abstract test classes that can be extended in storage tests or integration tests. The abstract test classes already define test methods so that you will get a good test coverage without writing any additional test cases.

[basyx.submodelregistry-service-mongodb-storage](./features/mongodb-storage.md) provides a registry-storage implementation based on mongoDB that could be used as storage for [submodelregistry-service](./features/service.md). It comes with java-based model classes, annotated with mongoDB annotations.

[basyx.submodelregistry-service-inmemory-storage](./features/inmemory-storage.md) provides a non-persistent registry-storage implementation where instances are stored in hash maps. It can be used as storage for [submodelregistry-service](./features/service.md).

[basyx.submodelregistry-service-kafka-events](./features/kafka-events.md) extends basyx.submodelregistry-service with a registry-event-sink implementation that delivers shell descriptor and submodel registration events using Apache Kafka. The default provided by submodelregistry-service just logs the events.

[basyx.submodelregistry-service-release-kafka-mongodb](./features/kafka-mongodb.md) is used to combine the server artifacts to a release image that uses [Apache Kafka](https://kafka.apache.org/) as event sink and [MongoDB](https://www.mongodb.com/) as storage.

[basyx.submodelregistry-service-release-kafka-mem](./features/kafka-mem.md) is used to combine the server artifacts to a release image that uses Apache Kafka as event sink and an in-memory storage.

[basyx.submodelregistry-service-release-log-mongodb](./features/log-mongodb.md) is used to combine the server artifacts to a release image that logs registry events and uses MongoDB as data storage.

[basyx.submodelregistry-service-release-log-mem](./features/log-mem.md) is used to combine the server artifacts to a release image that logs registry events and an in-memory storage.

## Server Configuration

### Backend Configuration
There is no separate configuration for a backend. To use a specific backend, you must use the appropriate storage implementation.

However, if you are using a MongoDB module, you will need to set the connection uri for the MongoDB storage implementation:
```properties
spring:
  data:
    mongodb:
      uri: mongodb://mongoAdmin:mongoPassword@mongo:27017
```
---

### CORS Configuration
Configure CORS settings to specify allowed origins and methods.

```properties
basyx:
  cors:
    allowed-origins: '*'
    allowed-methods: GET,POST,PATCH,DELETE,PUT,OPTIONS,HEAD
```

### Configure Favicon
```{note}
A favicon is a small 16×16 or 32×32 pixel icon, symbol or logo used by web browsers to identify a website in a recognizable way
```
To configure the favicon, mount your favicon to the `static` directory of the component using Docker:
```
docker run --name=submodel-registry -p:8081:8081 -v C:/path/to/favicon.ico:/application/static/favicon.ico eclipsebasyx/submodel-registry-log-mem:2.0.0-SNAPSHOT
```
or
```yaml
submodel-registry:
    image: eclipsebasyx/submodel-registry-log-mem:2.0.0-SNAPSHOT
    container_name: submodel-registry
    volumes:
      - ./basyx/submodel-registry.properties:/application/application.properties
	  - ./basyx/static/favicon.ico:/application/static/favicon.ico
    ports:
      - '8080:8080'
```

## Docker
The following example demonstrate how to use the Submodel Registry with Docker Compose:

```yml
sm-registry:
    image: eclipsebasyx/submodel-registry-log-mongodb:2.0.0-SNAPSHOT
    container_name: sm-registry
    ports:
      - '8083:8080'
    environment:
      - SERVER_PORT=8080
    volumes:
      - ./basyx/sm-registry.yml:/workspace/config/application.yml
    restart: always
```

**Warning:** When running this component inside Docker, **do not modify the port configuration**.  
Changing the port setting may prevent the service from being accessible from outside the container.

## Virtual Machine
Eclipse BaSyx provides the Submodel Registry as a virtual machine image for Oracle VirtualBox and VMware Workstation Player. At the moment, only the version that logs registry events and uses an in-memory storage is available as a virtual machine image. So, it is not possible to use Apache Kafka as event sink or MongoDB as storage.

The image can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu). How to use it is described [here](../../../user_tutorials/virtualmachines/alpine_virtualmachine_setup_use.md).


## Build Resources

To build the images run these commands from this folder or for the parent project pom:

Install maven generate jars:

``` shell 
mvn clean install
```

In order to build the docker images, you need to specify *docker.namespace* and *docker.password* properties (here without running tests):

``` shell
MAVEN_OPS='-Xmx2048 -Xms1024' mvn clean install -DskipTests -Ddocker.namespace=eclipsebasyx -Ddocker.password=""
```

You can now check your images from command-line and push the images:
``` shell 
docker images   ...
```
Or you can directly push them from maven. 

``` shell 
MAVEN_OPS='-Xmx2048 -Xms1024' mvn deploy -Ddocker.registry=docker.io -Ddocker.namespace=eclipsebasyx -Ddocker.password=pwd
```
In addition, maven deploy will also deploy your maven artifacts, so you can do everything in one step.

Have a look at the *docker-compose* sub-folder to see how the created images could be referenced in docker-compose files.

Consider updating the [image name pattern](pom.xml#L16) if you want a different image name.

## Swagger UI
In the Swagger UI, you can find the API documentation for the Submodel Registry.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoints is available at:

	http://{host}:{port}/swagger-ui/index.html


```{toctree}
:hidden:
:maxdepth: 1

features/client-native
features/service
features/service-basemodel
features/service-basetests
features/mongodb-storage
features/inmemory-storage
features/kafka-events
features/kafka-mongodb
features/kafka-mem
features/log-mongodb
features/log-mem
```
