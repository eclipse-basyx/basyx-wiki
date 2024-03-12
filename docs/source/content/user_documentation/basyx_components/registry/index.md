# Registry Component

The Registry is a central component to the Asset Administration Shell (AAS) infrastructure for looking up available AAS and their contained submodels. Hence, it is realized as a separate component that can also be containerized. Currently, there exists a single Registry component that can be configured to utilize different types of backends.

## Download
The registry image is made available via [Docker Hub](https://login.docker.com/u/login/identifier?state=hKFo2SBScEFyNlVtcEc5T3RaWlZPbUpmMG9CRWlaWEtpbHduRqFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIF9pNFppTVFMbTVSYUYwMk9jWmhUVXY0Z3JiSHFUTVRMo2NpZNkgbHZlOUdHbDhKdFNVcm5lUTFFVnVDMGxiakhkaTluYjk) and can be pulled by:
```
docker pull eclipsebasyx/aas-registry:1.5.1
```
Alternatively, the command described in Startup section will download the image.

## Startup
To easily start the registry component, you can use the following command:
```
docker run --name=registry -p 8082:4000 eclipsebasyx/aas-registry:1.5.1
```
Next, the HTTP/REST endpoint of the Registry is accessible via
```
http://localhost:8082/registry/api/v1/registry
```
If no AAS/SM is registered, an empty JSON list "[]" will be returned.

And the container can be stopped, started and removed using its name (see --name):
```
docker stop registry
docker start registry
docker rm registry
```
## Context Configuration
As with the other components, the registry's context can be customized using the [context configuration](../context-config.md ).

## AAS Registry Configuration
For the AAS Registry component, a multitude of features can be configured via the registry.properties file. By default, this configuration file is assumed to be located at *"/usr/share/config/registry.properties"* within the container.

Thus, another configuration file can be set by mounting a local configuration file into the container during startup. As an example, a local folder containing the configuration files can be mounted using:
```
docker run --name=registry -p 8082:4000 -v C:/tmp:/usr/share/config eclipsebasyx/aas-registry:1.5.1
```
In this example, the **registry.properties** file is located in C:/tmp/

The features of the AAS Registry component are documented on their own page: [Features](./features/index.md)

## Java Implementation
Within the project, the component can be found in the Java repository at [Java](https://git.eclipse.org/r/plugins/gitiles/basyx/basyx/+/master/components/basys.components/basyx.components.docker/basyx.components.registry/src/main/java/org/eclipse/basyx/components/registry/executable/). In this project, the executable can take the parameter **BASYX_REGISTRY** to configure the path of the registry configuration file. For example, you can specify the path of the registry configuration file via
```
java -jar -DBASYX_REGISTRY="C:/tmp/registry.properties" registry.jar
```

## [Features](./features/index.md)