# AAS Registry

![Docker Pulls (log-mem)](https://img.shields.io/docker/pulls/eclipsebasyx/aas-registry-log-mem?label=Docker%20Pulls%20(log-mem))
![Docker Pulls (log-mongodb)](https://img.shields.io/docker/pulls/eclipsebasyx/aas-registry-log-mongodb?label=Docker%20Pulls%20(log-mongodb))
![Docker Pulls (kafka-mem)](https://img.shields.io/docker/pulls/eclipsebasyx/aas-registry-kafka-mem?label=Docker%20Pulls%20(kafka-mem))
![Docker Pulls (kafka-mongodb)](https://img.shields.io/docker/pulls/eclipsebasyx/aas-registry-kafka-mongodb?label=Docker%20Pulls%20(kafka-mongodb))
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-java-server-sdk)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

This is a Java-based implementation of the Asset Administration Shell Registry server and client based on the corresponding [Open-API specification](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRegistryServiceSpecification/V3.0_SSP-001) of the German Plattform Industrie 4.0 and its specification document [Details of the Asset Administration Shell, Part 2](https://industrialdigitaltwin.org/wp-content/uploads/2023/04/IDTA-01002-3-0_SpecificationAssetAdministrationShell_Part2_API.pdf)

## Features

[basyx.aasregistry-client-native](features/client-native.md) can be used to interact with the backend to register or unregister descriptors and submodels or perform search operations.

[basyx.aasregistry-paths](features/paths.md) generates a builder class that can be used by the registry client to create search requests.

[basyx.aasregistry-plugins](features/plugins.md) contains maven plugins used by the other projects. 

[basyx.aasregistry-service](features/service.md) provides the application server to access the AAS descriptor storage and offers an API for REST-based communication.

[basyx.aasregistry-service-basemodel](features/service-basemodel.md) provides a base model implementation that should be used if you do not need specific model annotations for your storage. It is used for the in-memory storage implementation and you need to add it explicitly as dependency for your server deployment as it is defined as 'provided' dependency in the [basyx.aasregistry-service](basyx.aasregistry-service/README.md) POM.

[basyx.aasregistry-service-basetests](features/service-basetest.md) provides helper classes and abstract test classes that can be extended in storage tests or integration tests. The abstract test classes already define test methods so that you will get a good test coverage without writing any additional test cases.

[basyx.aasregistry-service-mongodb-storage](features/mongodb-storage.md) provides a registry-storage implementation based on mongoDB that could be used as storage for [aasregistry-service](basyx.aasregistry-service/README.md). It comes with java-based model classes, annotated with mongoDB annotations.

[basyx.aasregistry-service-inmemory-storage](features/inmemory-storage.md) provides a non-persistent registry-storage implementation where instances are stored in hash maps. It can be used as storage for [aasregistry-service](basyx.aasregistry-service/README.md).

[basyx.aasregistry-service-kafka-events](features/kafka-events.md) extends basyx.aasregistry-service with a registry-event-sink implementation that delivers shell descriptor and submodel registration events using Apache Kafka. The default provided by aasregistry-service just logs the events.

[basyx.aasregistry-service-release-kafka-mongodb](features/kafka-mongodb.md) is used to combine the server artifacts to a release image that uses [Apache Kafka](https://kafka.apache.org/) as event sink and [MongoDB](https://www.mongodb.com/) as storage.

[basyx.aasregistry-service-release-kafka-mem](features/kafka-mem.md) is used to combine the server artifacts to a release image that uses Apache Kafka as event sink and an in-memory storage.

[basyx.aasregistry-service-release-log-mongodb](features/log-mongodb.md) is used to combine the server artifacts to a release image that logs registry events and uses MongoDB as data storage.

[basyx.aasregistry-service-release-log-mem](features/log-mem.md) is used to combine the server artifacts to a release image that logs registry events and an in-memory storage.

A docker-compose file that illustrates the setup can be found in the [docker-compose](docker-compose/docker-compose.yml) folder.

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
To configure the favicon, mount your favicon to the `static` directory of the component using Docker:
```
docker run --name=aas-registry -p:8081:8081 -v C:/path/to/favicon.ico:/application/static/favicon.ico eclipsebasyx/aas-registry-log-mem:2.0.0-SNAPSHOT
```
or
```yaml
aas-registry:
    image: eclipsebasyx/aas-registry-log-mem:2.0.0-SNAPSHOT
    container_name: aas-registry
    volumes:
      - ./basyx/aas-registry.properties:/application/application.properties
	  - ./basyx/static/favicon.ico:/application/static/favicon.ico
    ports:
      - '8080:8080'
```

## Docker
The following example demonstrate how to use the AAS Registry with Docker Compose:

```yml
aas-registry:
    image: eclipsebasyx/aas-registry-log-mongodb:2.0.0-SNAPSHOT
    container_name: aas-registry
    ports:
      - '8083:8080'
    environment:
      - SERVER_PORT=8080
    volumes:
      - ./basyx/aas-registry.yml:/workspace/config/application.yml
    restart: always
```

```{important}
The REST API and the client implementation will not be modified - if not a SNAPSHOT version - until a new major version is released or an update of the openAPI definition. All server-side classes and the plugins are not intended to be used as programming library. They could be updated or removed then a new minor version is released.
```


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

Consider updating the [image name pattern](https://github.com/eclipse-basyx/basyx-java-server-sdk/blob/main/basyx.aasregistry/pom.xml#L16) if you want a different image name.

## Swagger UI
In the Swagger UI, you can find the API documentation for the AAS Registry.

You can also execute all the API calls directly from the Swagger UI.

The Aggregated API endpoint documentation is available at:

	http://{host}:{port}/v3/api-docs
	
The Aggregated Swagger UI for the endpoint is available at:

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
features/paths
features/plugins
```
