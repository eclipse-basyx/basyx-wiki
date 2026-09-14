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

PUT creates or replaces a complete resource, and its body identifier must agree with the path. Include all content that should remain. PATCH updates existing content according to the selected representation; it is not a generic JSON Patch endpoint. Use `$value` to change values while retaining metadata. See [Representations and Partial Updates](usage#representations-and-partial-updates).

### Database Schema

The Repository uses PostgreSQL and validates the shared schema at startup. Initialize it with the BaSyx Configuration Service before starting the Repository. See [Setup](setup).

## Configuration

See [General Configuration](../common/configuration) for server, database, and security settings. [Registry Integration](registry_integration) explains the component-specific integration flag, descriptor updates, and public endpoint generation.

## API Documentation and Availability

With an empty context path, the service exposes Swagger UI at `/swagger`, OpenAPI at `/api-docs/openapi.yaml`, and self-description at `/description`. Prefix these paths with `server.contextPath` when configured. Swagger can be disabled; see [Swagger UI Docs](../common/swagger).

The component ships an API v3.2 OpenAPI document. Consult the running Swagger UI for operations and payloads supported by the installed version, the [IDTA API specification v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html) for standardized behavior, and the [metamodel specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/index.html) for Submodel Element types and representations.

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
