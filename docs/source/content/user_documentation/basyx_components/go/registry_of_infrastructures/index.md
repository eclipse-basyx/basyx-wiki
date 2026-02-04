# Registry of Infrastructures

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

The BaSyx Registry of Infrastructures (RoI) is a component that can be used in Dataspaces (e.g., in MX Port Leo), to find Endpoints for AAS Infrastructure components, such as AAS Servers or other Registries. It acts as a centralized directory where different components, e.g., registries and repositories, can register themselves, allowing clients to discover available components and their endpoints. The component supports filtering based on company names, enabling users to retrieve RoI descriptors specific to a particular company, as well as filtering based on the type of infrastructure component.

## Configuration
The Registry of Infrastructures can be either configured through a docker-compose file or a separate configuration file

- [Configuration](configuration)

## Docker
Eclipse BaSyx provides the Registry of Infrastructures as off-the-shelf component via DockerHub. The following command pulls the image and starts a container for the Registry of Infrastructures:

```bash
docker run --name=registry-of-infrastructures -p:8081:8081 eclipsebasyx/registryofinfrastructures-go:SNAPSHOT
```

```{toctree}
:hidden:
:maxdepth: 1

configuration
```