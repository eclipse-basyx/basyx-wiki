
# AAS Server Component
The AAS server component provides an empty AAS server that can be used to host several AAS and Submodels. For its API usage see [Aggregator API](../../API/aas.md). Additionally, there's a video illustrating the configuration and usage in 5 minutes: [youtube](https://www.youtube.com/watch?v=nGRNg0sj1oY)

For a complete deployment of the AAS infrastructure, additionally to this server a registry is needed. For this registry, the [Registry Component](../registry/index.md) can be used.

For illustration on how to create an AAS on the server provided by the component and how to retrieve it see the [snippet](https://git.eclipse.org/r/plugins/gitiles/basyx/basyx/+/master/examples/basys.examples/src/test/java/org/eclipse/basyx/examples/snippets/aas/registry/ConnectToAASEndpoints.java) in the repository.

## Features
The AAS Server Components supports a multitude of  with a great range of configuration options.

Additionally, it is easy to implement new feature and integrate them into the AAS Server as shown in [this example](./simple-feature-decoration.md).

```{toctree}
:maxdepth: 0

features/storage-backend
features/preconfigured-aas-and-submodels.md
features/registry-integration
features/hierarchical-mqtt
features/simple-mqtt
features/authorization
features/aasx-upload
features/file-upload
features/operation-delegation
features/property-delegation
features/value-only-serialization
features/health-endpoint
features/simple-feature-decoration

```

## Download
The AAS Server image is made available via [Docker Hub](https://hub.docker.com/r/eclipsebasyx/aas-server) and can be pulled by:

``` 
docker pull eclipsebasyx/aas-server:1.5.0
```
Alternatively, the command described in Startup section will download the image.

## Startup
To easily start the AAS server component, you can use the following command:

```
docker run --name=aas -p 8081:4001 eclipsebasyx/aas-server:1.5.0
```
Next, the HTTP/REST endpoint of the server with its AAS is accessible via

```
http://localhost:8081/aasServer/shells/
```
If there's no AAS configured during startup, an empty JSON list "[]" will be returned.

And the container can be stopped, started and removed using its name (see --name):

```
docker stop aas
docker start aas
docker rm aas
```

## Configuration
As with the other components, the server's context can be customized using the [context configuration](../context-config.md).

For the AAS server component, a multitude of features can be configured via the aas.properties file. By default, this configuration file is assumed to be located at _"/usr/share/config/aas.properties"_ within the container.

Thus, another configuration file can be set by mounting a local configuration file into the container during startup. As an example, a local folder containing the configuration files can be mounted using:

```
docker run --name=aas -p 8081:4001 -v C:/tmp:/usr/share/config eclipsebasyx/aas-server:1.5.0
```
In this example, the **aas.properties** file is located in C:/tmp/. Similarly, the AAS source file also needs to be mounted into the docker container.

The features of the AAS Server component are documented on their own page: [Features](./features/index.md)

## Implementation
Within the project, the component can be found in the Java repository at [Java](https://git.eclipse.org/r/plugins/gitiles/basyx/basyx/+/master/components/basys.components/basyx.components.docker/basyx.components.AASServer/src/main/java/org/eclipse/basyx/components/aas/executable/). In this project, the executable can take the parameter **BASYX_AAS** to configure the path of the aas configuration file. For example, you can specify the path of the aas configuration file via

```
java -jar -DBASYX_AAS="C:/tmp/aas.properties" aas.jar
```
