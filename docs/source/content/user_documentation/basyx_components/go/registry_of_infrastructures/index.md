# Registry of Infrastructures

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

The BaSyx Registry of Infrastructures (RoI) is a component that can be used in Dataspaces (e.g., in MX Port Leo), to find Endpoints for AAS infrastructure components, such as AAS Servers or other Registries. It acts as a centralized directory where different components, e.g., registries and repositories, can register themselves, allowing clients to discover available components and their endpoints. The component supports filtering based on company names, enabling users to retrieve RoI descriptors specific to a particular company, as well as filtering based on the type of infrastructure component.

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

- `GET /infrastructure-descriptors`: Retrieves all registered AAS infrastructure components. It supports the optional query parameters 
  - `company` to filter the results based on the company name and
  - `endpointInterface` to filter the results based on the type of infrastructure component.
- `GET /infrastructure-descriptors/{id}`: Retrieves a specific AAS infrastructure component identified by its unique ID.
- `POST /infrastructure-descriptors`: Registers a new AAS infrastructure component by accepting a Infrastructure Descriptor in the request body.
- `DELETE /infrastructure-descriptors/{id}`: Deletes a registered AAS infrastructure component identified by its unique ID.
- `PUT /infrastructure-descriptors/{id}`: Updates an existing AAS infrastructure component identified by its unique ID with the new Infrastructure Descriptor provided in the request body.


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