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

The AAS identifier in the request path is Base64URL-encoded. Identifiers in JSON request bodies remain unencoded. PUT creates the AAS if it does not exist or replaces the existing AAS. The identifier in the request body must match the decoded path identifier. The request body must contain the complete AAS, including all references and metadata that should be retained.

### References and Submodel Content

Removing a Submodel reference unlinks it from the AAS. Deleting through an AAS-scoped Submodel route removes the reference and the stored Submodel content. These are different operations, especially when several AASs refer to the same Submodel. See [AAS-scoped Submodel Access](usage.md#aas-scoped-submodel-access).

### Database Schema

The Repository uses PostgreSQL. The BaSyx Configuration Service must initialize the shared schema before startup. The Repository validates it and does not initialize it itself. See [Setup](setup).

## Configuration

See [General Configuration](../common/configuration) for server and database settings. For authentication, authorization, supported executables, and policy persistence, see [Runtime Security](../common/security). [Registry Integration](registry_integration) explains the component-specific integration flag and public endpoint generation.

## API Documentation and Availability

Use the following API documentation depending on whether you need the behavior of a running BaSyx component or the standardized API definition:

- **BaSyx Go Swagger UI** describes the running component's API, including its configured base path and runtime OpenAPI adjustments. It provides operation parameters, request and response schemas, status codes, and interactive requests. Consult the availability notes below alongside the runtime contract.
- **[IDTA AAS Repository Swagger UI v3.2.0](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=..%2FAssetAdministrationShellRepositoryServiceSpecification%2FV3.2_SSP-001.yaml&version=v3.2.0)** presents the standardized AAS Repository Full Profile interactively.
- **[IDTA Specification of the Asset Administration Shell, Part 2: Application Programming Interfaces v3.2.0](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html)** defines the standardized operations, service specifications, profiles, and serialization behavior. The [metamodel specification v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/index.html) defines AAS payloads.

The OpenAPI document shipped with the current BaSyx Go AAS Repository identifies API version `V3.2.0` and declares profiles `SSP-001`, `SSP-003`, `SSP-004`, `SSP-005`, and `SSP-006`. These declarations describe the shipped specification; use the running component's Swagger UI and the availability notes below to determine the installed service's supported operations.

With the default empty context path, the service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`;
- service self-description at `/description`.

When `server.contextPath` is configured, these locations are served below that context path. Swagger can also be disabled through configuration. See [Swagger UI Docs](../common/swagger) for details.

### Availability Notes

The standalone AAS Repository does not support the `/serialization` endpoint. For full environment import/export, use the combined [AAS Environment](../aas_environment/index), which implements `/serialization` and `/upload`. Its Repository-to-Registry synchronization still depends on explicit integration flags; merely using the combined executable does not make every Repository write synchronize automatically.

## Related Documentation

- [Setting Up the AAS Repository](setup)
- [Using the AAS Repository](usage)
- [Registry Integration](registry_integration)
- [AAS Environment](../aas_environment/index)
- [Runtime Security](../common/security)
- [Submodel Repository](../submodel_repository/index)
- [Common / Shared Features](../common/shared_features)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
registry_integration
```
