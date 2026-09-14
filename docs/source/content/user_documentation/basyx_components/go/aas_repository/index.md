# AAS Repository

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go AAS Repository stores and serves Asset Administration Shells (AASs). An AAS identifies an asset, contains asset information, and references the Submodels that describe aspects of that asset.

## Repository or Registry?

Use the Repository to create, retrieve, and modify AAS content. The [AAS Registry](../aas_registry/index) stores descriptors that advertise where clients can access that content. Registering a descriptor does not create an AAS.

An AAS contains Submodel references, not inline Submodel content. This Go component also exposes AAS-scoped Submodel routes backed by Submodel storage in the same database. Adding a reference alone does not create that content or fetch it from another service. See [Using the AAS Repository](usage) for both workflows.

## Main Capabilities

- Create, retrieve, replace, and delete AASs.
- List AASs with filters and [cursor-based pagination](../common/pagination).
- Retrieve and replace asset information independently of the complete AAS.
- Manage Submodel references and access Submodel content through an AAS.
- Optionally synchronize AAS Descriptors through [Registry Integration](registry_integration).
- Expose service self-description and runtime API documentation.

## Important Behavior

### Identifiers and Updates

Path identifiers use UTF-8 Base64URL encoding; identifiers in JSON bodies remain unencoded. PUT creates a missing AAS or replaces an existing one. The body identifier must match the decoded path identifier. Submit the complete AAS, including the references and metadata that should remain.

### References and Submodel Content

Removing a Submodel reference unlinks it from the AAS. Deleting through an AAS-scoped Submodel route removes the reference and the stored Submodel content. These are different operations, especially when several AASs refer to the same Submodel. See [AAS-scoped Submodel Access](usage.md#aas-scoped-submodel-access).

### Database Schema

The Repository uses PostgreSQL. The BaSyx Configuration Service must initialize the shared schema before startup. The Repository validates it and does not initialize it itself. See [Setup](setup).

## Configuration

See [General Configuration](../common/configuration) for server, database, and security settings. [Registry Integration](registry_integration) explains the component-specific integration flag and public endpoint generation.

## API Documentation and Availability

With an empty context path, Swagger UI is available at `/swagger`, the OpenAPI document at `/api-docs/openapi.yaml`, and service self-description at `/description`. A configured `server.contextPath` prefixes these paths. See [Swagger UI Docs](../common/swagger).

The component ships an API v3.2 OpenAPI document. Use the running Swagger UI together with the behavior documented here to determine the installed service's capabilities. The [IDTA API specification v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html) defines standardized operations and the [metamodel specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/index.html) defines AAS payloads.

The standalone AAS Repository does not support the `/serialization` endpoint. For full environment import/export, use the AAS Environment's implemented `/serialization` and `/upload` APIs.

## Related Documentation

- [Setting Up the AAS Repository](setup)
- [Using the AAS Repository](usage)
- [Registry Integration](registry_integration)
- [Submodel Repository](../submodel_repository/index)
- [Common / Shared Features](../common/shared_features)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
registry_integration
```
