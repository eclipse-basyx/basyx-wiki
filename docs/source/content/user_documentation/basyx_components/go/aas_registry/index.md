# AAS Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx AAS Registry implements the Asset Administration Shell Registry Service. It stores AAS Descriptors and the Submodel Descriptors associated with a registered AAS so that clients can discover where AASs and their Submodels are available.

The Registry manages descriptive and routing metadata. It does not store or serve the AAS or Submodel content itself.

## What Is an AAS Descriptor?

An AAS Descriptor identifies an AAS and describes how clients can reach it. Depending on the deployment and use case, it can contain information such as:

- the AAS identifier and `idShort`;
- asset-identification information;
- endpoints at which the AAS can be accessed;
- Submodel Descriptors associated with that AAS.

A complete list of AAS Descriptor attributes is found in the [specification of the AAS](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/specification/interfaces-payload.html#_assetadministrationshelldescriptor). <br>
A Submodel Descriptor plays the same role for a Submodel: It identifies the Submodel and advertises endpoints and other discovery metadata. In the AAS Registry, Submodel Descriptors are scoped to their parent AAS Descriptor.

## Registry or Repository?

Use the AAS Registry when a client needs to discover an AAS or determine which service endpoint provides it. Use an AAS Repository when a client needs to store, retrieve, or modify the actual AAS content.

A typical deployment uses both components:

1. An AAS Repository stores and serves the AAS.
2. The AAS Registry stores a descriptor containing the AAS identifier and the Repository endpoint.
3. A client searches the Registry and receives the descriptor.
4. The client follows the advertised endpoint to interact with the AAS in the Repository.

The Registry and Repository do not have to run in the same process or at the same network location. This separation allows one Registry to advertise AASs provided by multiple services or organizations.

Alternatively, the BaSyx AAS Environment combines the AAS Registry and AAS Repository capabilities in a single component.

See [Using the AAS Registry](usage) for a walkthrough from descriptor registration to lookup, update, and deletion.

## Main Capabilities

The AAS Registry supports management of AAS Descriptors and their associated Submodel Descriptors. It provides operations for listing, creating, retrieving, updating, and deleting descriptors.

It also supports:

- cursor-based pagination for descriptor collections;
- filtering AAS Descriptors by asset-related properties and change timestamps;
- structured queries for more expressive descriptor searches;
- asynchronous bulk creation, update, and deletion of AAS Descriptors;
- service self-description.

See [API Documentation](#api-documentation) for the authoritative list of operations, parameters, schemas, and responses.

## Important Behavior

### AAS-scoped Submodel Descriptors

Submodel Descriptors in this component belong to an AAS Descriptor. Clients therefore address a Submodel Descriptor in the context of both its AAS identifier and its Submodel identifier. Use the standalone Submodel Registry when Submodel Descriptors must be managed independently of an AAS Descriptor.

### Identifier Encoding

Identifiers used in request paths must be encoded as UTF-8 Base64 URL values. Encode the original identifier with the URL-safe Base64 alphabet before placing it in a path. Do not send an arbitrary AAS or Submodel identifier directly as a path segment, because identifiers can contain characters that have a special meaning in URLs.

When an operation also has a request body, the body continues to contain the original, unencoded identifier. Some query parameters also require encoding: `assetType` is a Base64URL-encoded string, and each `assetIds` value is a Base64URL-encoded JSON `SpecificAssetId`.

### Pagination and Filters

Collection requests use [cursor-based pagination](../common/pagination). See the shared guide for page size, response structure, and continuation requests.

Asset-related filters help clients narrow discovery results before contacting a Repository. For example:

- `assetKind` limits results by the kind of asset represented by the AAS;
- `assetType` selects descriptors whose asset information uses a particular asset-type value;
- asset-identifier filters locate descriptors associated with known asset identifiers;
- `createdFrom` and `updatedFrom` select descriptors by their persisted administrative timestamps.

Timestamp filters use `administration.createdAt` and `administration.updatedAt` from the descriptor payload. The Registry does not generate or update these values on writes. Instead, the registering application must maintain them. The lower bounds are inclusive. When both timestamp filters are supplied, a descriptor matches if either bound is satisfied.

### Updates

PUT creates a descriptor when its identifier does not exist and replaces it when it does. The body identifier must match the decoded path identifier. Replacing an AAS Descriptor also replaces its nested Submodel Descriptors. Retain those entries in the submitted body when they should remain registered.

### Bulk Operations

Bulk creation, update, and deletion are asynchronous and atomic: if a descriptor operation fails, the complete transaction is rolled back. Submit a bulk request, poll its status, and retrieve the completed result once. Retrieving the completed result consumes the handle. See [Bulk Operations](usage.md#bulk-operations) for the response sequence, retention, and failure handling.

### Database Schema

The Registry uses PostgreSQL and expects the shared BaSyx database schema to be initialized and migrated by the BaSyx Configuration Service. The Registry validates the schema during startup and does not initialize it itself. See [Setting Up the AAS Registry](setup) for the required startup order.

## Configuration

See [General Configuration](../common/configuration) for the configuration parameters supported by BaSyx Go components.

## API Documentation

Use the following API documentation depending on whether you need the behavior of a running BaSyx component or the standardized API definition:

- **BaSyx Go Swagger UI** describes the API actually exposed by the running component, including its configured base path and runtime OpenAPI adjustments. It contains the complete operation list, parameters, request and response schemas, status codes, and interactive requests.
- **[IDTA AAS Registry Swagger UI v3.2.0](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=..%2FAssetAdministrationShellRegistryServiceSpecification%2FV3.2_SSP-001.yaml&version=v3.2.0)** presents the standardized AAS Registry Full Profile interactively.
- **[IDTA Specification of the Asset Administration Shell, Part 2: Application Programming Interfaces v3.2.0](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/index.html)** is the normative specification for the standardized operations, service specifications, profiles, and serialization behavior on which this component is based.

The OpenAPI document shipped with the current BaSyx Go AAS Registry identifies API version 3.2.0 and declares the AAS Registry Full, Bulk, and Query profiles (`SSP-001`, `SSP-003`, and `SSP-004`). Use the Swagger UI of the running component to determine its actual exposed contract and configuration.

With the default empty context path, the service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`.

When `server.contextPath` is configured, both locations are served below that context path. Swagger can also be disabled through configuration. See [Swagger UI Docs](../common/swagger) for details.

## Related Documentation

- [Setting Up the AAS Registry](setup)
- [Using the AAS Registry](usage)
- [General Configuration](../common/configuration)
- [Common / Shared Features](../common/shared_features)
- [Swagger UI Docs](../common/swagger)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
