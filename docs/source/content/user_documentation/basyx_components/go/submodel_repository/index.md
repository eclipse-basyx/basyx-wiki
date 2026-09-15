# Submodel Repository

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go Submodel Repository stores and serves Submodels and their Submodel Elements. A Submodel describes an aspect of an asset, such as its nameplate, technical data, or operating values.

## Repository or Registry?

Use the Repository to create, retrieve, and modify Submodel content. The [Submodel Registry](../submodel_registry/index) stores descriptors containing discovery metadata and service endpoints. Creating a descriptor does not create its Submodel content.

A Submodel can exist independently of an AAS and can be referenced by multiple AASs. The [AAS Repository](../aas_repository/index) manages those references and supports AAS-scoped Submodel access. The standalone Submodel Repository addresses content directly by Submodel identifier.

## Main Capabilities

- Create, retrieve, replace, and delete complete Submodels.
- List Submodels with filters and [cursor-based pagination](../common/pagination).
- Create, read, update, and delete individual Submodel Elements.
- Read normal, value-only, metadata, reference, and path representations.
- Update existing values or metadata through the corresponding PATCH operations.
- Optionally synchronize descriptors through [Registry Integration](registry_integration).
- Expose service self-description and runtime API documentation.

See [Using the Submodel Repository](usage) for a walkthrough with Properties and a nested collection.

## Important Behavior

### Identifiers and Element Paths

The Submodel identifier in a request path is Base64URL-encoded. A Submodel Element is addressed by its `idShortPath`, such as `Nameplate.SerialNumber`; this path is not Base64URL-encoded. List members use zero-based indices. Identifiers in JSON bodies remain unencoded.

### Replacement and Partial Updates

PUT creates or replaces a complete resource, and its body identifier must agree with the path. Include all content that should remain. PATCH updates existing content according to the selected representation; it is not a generic JSON Patch endpoint. Use `$value` to change values while retaining metadata. See [Representations and Partial Updates](usage.md#representations-and-partial-updates).

### Database Schema

The Repository uses PostgreSQL and validates the shared schema at startup. Initialize it with the BaSyx Configuration Service before starting the Repository. See [Setup](setup).

## Configuration

See [General Configuration](../common/configuration) for server, database, and security settings. [Registry Integration](registry_integration) explains the component-specific integration flag, descriptor updates, and public endpoint generation.

## API Documentation and Availability

Use the following API documentation depending on whether you need the behavior of a running BaSyx component or the standardized API definition:

- **BaSyx Go Swagger UI** describes the running component's API, including its configured base path and runtime OpenAPI adjustments. It provides operation parameters, request and response schemas, status codes, and interactive requests. Consult the availability notes below alongside the runtime contract.
- **[IDTA Submodel Repository Swagger UI v3.2.0](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=..%2FSubmodelRepositoryServiceSpecification%2FV3.2_SSP-001.yaml&version=v3.2.0)** presents the standardized Submodel Repository Full Profile interactively.
- **[IDTA Specification of the Asset Administration Shell, Part 2: Application Programming Interfaces v3.2.0](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html)** defines the standardized operations, service specifications, profiles, and serialization behavior. The [metamodel specification v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/index.html) defines Submodels and Submodel Element types.

The OpenAPI document shipped with the current BaSyx Go Submodel Repository identifies API version `V3.2.0` and declares profiles `SSP-001`, `SSP-003`, `SSP-004`, `SSP-005`, `SSP-006`, and `SSP-007`. These declarations describe the shipped specification; use the running component's Swagger UI and the availability notes below to determine the installed service's supported operations.

With the default empty context path, the service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`;
- service self-description at `/description`.

When `server.contextPath` is configured, these locations are served below that context path. Swagger can also be disabled through configuration. See [Swagger UI Docs](../common/swagger) for details.

### Availability Notes

The standalone `/serialization` route currently returns `501 Not Implemented`. Reading a Submodel as JSON or in a different representation is separate from environment import/export. For full environment import/export, use the AAS Environment's implemented `/serialization` and `/upload` APIs. See the [Go API availability guide](https://github.com/eclipse-basyx/basyx-go-components/blob/main/docu/user/aas_api_v3_2.md).

## Related Documentation

- [Setting Up the Submodel Repository](setup)
- [Using the Submodel Repository](usage)
- [Registry Integration](registry_integration)
- [AAS Repository](../aas_repository/index)
- [Common / Shared Features](../common/shared_features)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
registry_integration
```
