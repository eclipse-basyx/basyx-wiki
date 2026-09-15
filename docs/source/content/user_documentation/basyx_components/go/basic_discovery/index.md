# Basic Discovery Component

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Basic Discovery component implements the Asset Administration Shell Basic Discovery API. It resolves Asset Administration Shell (AAS) identifiers from known asset identifiers and manages the asset links associated with an AAS identifier.

Discovery returns AAS identifiers. Clients use an AAS Registry to resolve those identifiers to service endpoints and an AAS Repository to access the AAS content.

## What Is an Asset Link?

An asset link identifies an asset by a name and value, such as `serialNumber` and `SN-001`. Discovery associates these identifiers with an AAS identifier so that a client can find the AAS from information it already knows about the asset.

For example:

- the AAS identifier is `urn:example:aas:1`;
- a specific asset identifier is `{"name":"serialNumber","value":"SN-001"}`;
- the global asset identifier can be represented as `{"name":"globalAssetId","value":"urn:example:asset:1"}`.

Registration accepts an array of `SpecificAssetId` objects. Lookup accepts an array of `AssetLink` objects; the examples use their `name` and `value` fields. The AAS identifier belongs in the registration URL, separately from the asset identifiers in the body.

## Discovery or Registry?

Use Basic Discovery when a client knows an asset identifier and needs the corresponding AAS identifier. Use the [AAS Registry](../aas_registry/index) to retrieve an AAS Descriptor containing service endpoints. Use the [AAS Repository](../aas_repository/index) to store, retrieve, or modify AAS content.

A typical discovery flow is:

1. A client submits an asset identifier to Basic Discovery.
2. Discovery returns matching AAS identifiers.
3. The client retrieves the corresponding descriptors from the AAS Registry.
4. The client follows a descriptor's endpoint to access the AAS in a Repository.

Registering asset links does not create AAS content or an endpoint descriptor. Maintain the corresponding Registry and Repository resources separately. The [Digital Twin Registry](../digital_twin_registry/index) combines AAS Registry and Basic Discovery APIs in one component.

See [Using Basic Discovery](usage) for registration, lookup, replacement, and deletion examples.

## Main Capabilities

The Basic Discovery component supports:

- creating or replacing the asset links associated with an AAS identifier;
- retrieving the registered asset links for an AAS identifier;
- resolving AAS identifiers by specific asset identifiers or a global asset identifier;
- cursor-based pagination of lookup results;
- deleting an AAS identifier's discovery registration;
- service self-description.

See [API Documentation](#api-documentation) for operation parameters, schemas, and responses.

## Important Behavior

### Identifier Encoding

Encode the AAS identifier in `/lookup/shells/{aasIdentifier}` as UTF-8 Base64URL. Asset-link names and values in JSON bodies remain unencoded. See [Identifiers and Encoding](../common/encoding).

### Lookup and Pagination

Use `POST /lookup/shellsByAssetLink` for new clients. `GET /lookup/shells` remains available but is deprecated in the specification; its `assetIds` query values are Base64URL-encoded JSON objects.

Lookup matches exact asset-link names and values. When multiple links are supplied, the AAS must match all of them. The reserved name `globalAssetId` selects a global asset identifier. An empty lookup array returns an empty result in the unsecured setup; it is not a request to list every AAS.

Lookup responses contain original, unencoded AAS identifier strings in `result`, with continuation information in `paging_metadata`. Follow [Pagination](../common/pagination), retaining the same lookup body for subsequent pages. Retrieving one AAS identifier's asset links instead returns a plain JSON array.

### Updates and Deletion

`POST /lookup/shells/{aasIdentifier}` creates or replaces the complete asset-link set and returns `201 Created` in both cases. Include every link that should remain registered. Each submitted entry must have a non-empty `name` and `value`.

`DELETE /lookup/shells/{aasIdentifier}` removes the discovery registration and its asset links. It does not delete AAS content from a Repository. Discovery and Registry services can share asset-identification data in the same database; coordinate updates when using them together.

### Database Schema

The component uses PostgreSQL and validates the shared BaSyx schema at startup. Initialize and migrate the schema with the BaSyx Configuration Service before starting Discovery. See [Setting Up Basic Discovery](setup) for the startup order.

## Configuration

See [General Configuration](../common/configuration) for server, database, and security settings. The [Compose setup](setup) exposes Discovery on port `8086`.

## API Documentation

Use the running **BaSyx Go Swagger UI** for the installed component's operations, parameters, schemas, and responses. The shipped OpenAPI document identifies API version `V3.2.0` and the Discovery Service Full Profile (`SSP-001`).

With an empty context path, the service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`;
- service self-description at `/description`.

A configured `server.contextPath` prefixes these locations. Swagger can be disabled through configuration. See [Swagger UI Docs](../common/swagger).

## Related Documentation

- [Setting Up Basic Discovery](setup)
- [Using Basic Discovery](usage)
- [AAS Registry](../aas_registry/index)
- [Digital Twin Registry](../digital_twin_registry/index)
- [General Configuration](../common/configuration)
- [Common / Shared Features](../common/shared_features)
- [Swagger UI Docs](../common/swagger)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
