# Registry of Infrastructures

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

The BaSyx Registry of Infrastructures (RoI) is a component that can be used in Dataspaces (e.g., in MX Port Leo), to find Endpoints for infrastructure components, such as AAS Servers or other Registries. It acts as a centralized directory where different components, e.g., registries and repositories, can register themselves, allowing clients to discover available components and their endpoints. The component supports filtering based on company names, enabling users to retrieve RoI descriptors specific to a particular company, as well as filtering based on the type of infrastructure component.

## Infrastructure Descriptor

As part of the Registry of Infrastructures the following new kind of Descriptor, the so-called Infrastructure Descriptor is introduced. Similar to AAS Descriptor and Submodel Descriptor it inherits from [Descriptor](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1/specification/interfaces-payload.html#descriptor).

| Attribute      | Explanation                                                    | Type                      | Card. |
|----------------|----------------------------------------------------------------|---------------------------|-------|
| administration | Administrative information of the infrastructure component     | AdministrativeInformation | 0..1  |
| endpoint       | Endpoint of the network resource                               | Endpoint                  | 0..*  |
| idShort        | Short name of the infrastructure component                     | NameType                  | 0..1  |
| id             | Globally unique identification of the infrastructure component | Identifier                | 1     |
| company        | Identifier of the company enabling filtering                   | Identifier                | 1     |


## API Endpoints

The Registry of Infrastructures has the following API endpoints:

- `GET /infrastructure-descriptors`: Retrieves all registered infrastructure components. It supports the optional query parameters 
  - `company` to filter the results based on the company name and
  - `endpointInterface` to filter the results based on the type of infrastructure component.
- `GET /infrastructure-descriptors/{id}`: Retrieves a specific infrastructure component identified by its unique ID.
- `POST /infrastructure-descriptors`: Registers a new infrastructure component by accepting a Infrastructure Descriptor in the request body.
- `DELETE /infrastructure-descriptors/{id}`: Deletes a registered infrastructure component identified by its unique ID.
- `PUT /infrastructure-descriptors/{id}`: Updates an existing infrastructure component identified by its unique ID with the new Infrastructure Descriptor provided in the request body.

The ID used in the path parameter and special characters in the URL must be base64 URL encoded. For example, "Fraunhofer IESE" should be "Fraunhofer%20IESE".

### Filtering Parameters

The `GET /infrastructure-descriptors` endpoint supports optional query parameters to narrow down the results.

#### company
The `company` parameter allows filtering infrastructure descriptors by the company or institution that owns or operates the infrastructure component. This enables clients to retrieve only those components that belong to a specific organization. For example, the infrastructure components operated by Fraunhofer IESE can be retrieved as follows:
```
GET /infrastructure-descriptors?company=Fraunhofer%20IESE
```

#### endpointInterface
The `endpointInterface` parameter allows filtering infrastructure descriptors based on the type of infrastructure component exposed by the endpoint. This information is stored in the `interface` attribute of the [endpoint](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1/specification/interfaces-payload.html#_endpoint) attribute of the Infrastructure Descriptor. This filter is useful when clients are only interested in a specific kind of service. Infrastructure components may include other BaSyx components, such as an AAS Registry, or other services, such as MQTT brokers. For example, the endpoint of an AAS Registry operated by Fraunhofer IESE can be retrieved as follows:
```
GET /infrastructure-descriptors?company=Fraunhofer%20IESE&endpointInterface=AAS-REGISTRY-3.0
```

## Swagger UI

In the [Swagger UI](swagger), you can find the API documentation for the Registry of Infrastructures. Furthermore, you can directly execute API calls from Swagger UI.

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

swagger
configuration
```