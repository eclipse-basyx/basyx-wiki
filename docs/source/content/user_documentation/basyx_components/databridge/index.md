# DataBridge Component
The DataBridge supports integrating various protocols with Asset Administration Shells. Data can be acquired from various endpoints, be transformed and pushed into SubmodelElements. By being provided as easy-to-use off-the-shelf component on [DockerHub](https://hub.docker.com/r/eclipsebasyx/databridge), it can easily be integrated in own use cases. For a comprehensive example, see the[ Asset Integration Scenario](../../../scenarios/device-integration.md).

## Download
The DataBridge image is made available via [Docker Hub](https://hub.docker.com/r/eclipsebasyx/databridge) and can be pulled by:
```
docker pull eclipsebasyx/databridge:1.0.0-SNAPSHOT
```
Alternatively, the command described in Startup section will download the image.

## Startup
To easily start the DataBridge component, you can use the following command:
```
docker run --name=databridge -p 8085:8085 -v C:/tmp:/usr/share/config eclipsebasyx/databridge:1.0.0-SNAPSHOT
```
The host port 8085 is mapped to container port 8085. The configuration files are located in **C:/tmp** and are available to the docker container at **/usr/share/config** via volume mapping. Alternatively, the DataBridge can be configured by passing the configuration files via environment variables.

## Configuration via Environment Variables
The DataBridge expects the environment variables to follow the same naming scheme and content as the config files. For example, for routes configuration, "routes.json" environment variable needs to be defined with the content described in the [routes.json](./features/routes-configuration.md) documentation. Additionally, the name of the JSONata transformation files need to be explicitly configured as JSON array via *jsonatatransformers* variable, e.g., *jsonatatransformers = ["jsonataA.json", "jsonataB.json"]*.

[Note]:

* Either volume mapping or environment variable configuration is mandatory because if there are no configuration files defined/mapped, then running the image would throw an exception.
* Make sure that other components such as Data Source, Transformer, and Data Sink components defined in the configuration are up and running before starting the DataBridge component.
* Please use the latest version of the DataBridge image.

# [Features](./features/index.md)