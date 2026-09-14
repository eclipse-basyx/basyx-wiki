# Submodel Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Submodel Registry implements the Asset Administration Shell Submodel Registry Service. It stores Submodel Descriptors as standalone registry entries so that clients can discover where Submodels are available.

The Registry manages descriptive and routing metadata. It does not store or serve the Submodel content itself.

## What Is a Submodel Descriptor?

A Submodel Descriptor identifies a Submodel and describes how clients can reach it. Depending on the deployment and use case, it can contain information such as:

- the Submodel identifier and `idShort`;
- semantic identification information;
- endpoints at which the Submodel can be accessed;
- supplemental semantic IDs and other discovery metadata.

A complete list of Submodel Descriptor attributes is found in the [Specification of the Asset Administration Shell](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/specification/interfaces-payload.html#_submodeldescriptor).

## Registry or Repository?

Use the Submodel Registry when a client needs to discover a Submodel or determine which service endpoint provides it. Use a [Submodel Repository](../submodel_repository/index) when a client needs to store, retrieve, or modify the actual Submodel content.

A typical deployment uses both components:

1. A Submodel Repository stores and serves a Submodel.
2. The Submodel Registry stores a descriptor containing the Submodel identifier and the Repository endpoint.
3. A client searches the Registry and receives the descriptor.
4. The client follows the advertised endpoint to interact with the Submodel in the Repository.

The Registry and Repository do not have to run in the same process or at the same network location. This separation allows one Registry to advertise Submodels provided by multiple services or organizations.

Alternatively, the BaSyx AAS Environment combines the Submodel Registry and Submodel Repository capabilities in a single component.

See [Using the Submodel Registry](usage) for a walkthrough from descriptor registration to lookup, update, and deletion.

## Main Capabilities

The Submodel Registry supports management of standalone Submodel Descriptors. It provides operations for listing, creating, retrieving, updating, and deleting descriptors.

It also supports:

- cursor-based pagination for descriptor collections;
- filtering Submodel Descriptors by creation and update timestamps;
- structured queries for more expressive descriptor searches;
- asynchronous bulk creation, update, and deletion of Submodel Descriptors;
- polling the status and result of asynchronous bulk operations;
- service self-description.

See [API Documentation](#api-documentation) for the authoritative list of operations, parameters, schemas, and responses.

## Important Behavior

### Standalone Submodel Descriptors

Submodel Descriptors in this component are managed independently of an AAS Descriptor. Clients address a descriptor using only its Submodel identifier. Use the [AAS Registry](../aas_registry/index) when Submodel Descriptors should be managed as part of an AAS Descriptor.

### Identifier Encoding

Submodel identifiers used in request paths must be encoded as UTF-8 Base64 URL values. Encode the original identifier with the URL-safe Base64 alphabet before placing it in a path. Do not send an arbitrary Submodel identifier directly as a path segment, because identifiers can contain characters that have a special meaning in URLs.

When an operation also has a request body, the body continues to contain the original, unencoded identifier. Query JSON and bulk-delete identifier arrays also use original identifiers.

### Pagination and Filters

Collection requests use [cursor-based pagination](../common/pagination). See the shared guide for page size, response structure, and continuation requests.

`createdFrom` and `updatedFrom` filter the descriptor's persisted `administration.createdAt` and `administration.updatedAt`. The Registry does not generate or update these values on writes; the registering application must maintain them. Bounds are inclusive, and when both timestamp filters are supplied, either condition can match.

Use [Structured Queries](usage#structured-queries) to search descriptor fields such as semantic identification. The ordinary descriptor-list endpoint supports `limit`, `cursor`, `createdFrom`, and `updatedFrom`; it does not provide a `semanticId` filter parameter.

### Updates

PUT creates a missing descriptor and replaces an existing descriptor. The body identifier must match the decoded path identifier. Submit the complete descriptor, including endpoints and metadata that should remain; PUT is not a partial update. Replacing or deleting a descriptor does not modify the Submodel content in a Repository.

### Bulk Operations

Bulk descriptor creation, update, and deletion are asynchronous. Submit the request to the bulk endpoint, then use the returned handle to poll the bulk status and result endpoints. Bulk processing is atomic: if one descriptor operation fails, the complete transaction is rolled back.

Retrieving a completed result consumes the handle, including for failed jobs. See [Bulk Operations](usage#bulk-operations) for submission, polling, result retrieval, expiry, and failure behavior.

### Database Schema

The Registry uses PostgreSQL and expects the shared BaSyx database schema to be initialized and migrated by the BaSyx Configuration Service. The Registry validates the schema during startup and does not initialize it itself. See [Setting Up the Submodel Registry](setup) for the required startup order.

## Configuration

See [General Configuration](../common/configuration) for the configuration parameters supported by BaSyx Go components.

## API Documentation

Use the following API documentation depending on whether you need the behavior of a running BaSyx component or the standardized API definition:

- **BaSyx Go Swagger UI** describes the API actually exposed by the running component, including its configured base path and runtime OpenAPI adjustments. It contains the complete operation list, parameters, request and response schemas, status codes, and interactive requests.
- **[IDTA Submodel Registry Swagger UI v3.2.0](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=..%2FSubmodelRegistryServiceSpecification%2FV3.2_SSP-001.yaml&version=v3.2.0)** presents the standardized Submodel Registry Full Profile interactively.
- **[IDTA Specification of the Asset Administration Shell, Part 2: Application Programming Interfaces v3.2.0](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html)** is the normative specification for the standardized operations, service specifications, profiles, and serialization behavior on which this component is based.

The OpenAPI document shipped with the current BaSyx Go Submodel Registry identifies API version 3.2.0 and declares the Submodel Registry Full, Bulk, and Query profiles (`SSP-001`, `SSP-003`, and `SSP-004`). Use the Swagger UI of the running component to determine its actual exposed contract and configuration.

With the default empty context path, the service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`.

When `server.contextPath` is configured, both locations are served below that context path. Swagger can also be disabled through configuration. See [Swagger UI Docs](../common/swagger) for details.

## Related Documentation

- [Setting Up the Submodel Registry](setup)
- [Using the Submodel Registry](usage)
- [General Configuration](../common/configuration)
- [Common / Shared Features](../common/shared_features)
- [Swagger UI Docs](../common/swagger)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
