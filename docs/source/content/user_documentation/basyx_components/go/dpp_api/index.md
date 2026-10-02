# Digital Product Passport API

[![GitHub](https://img.shields.io/badge/GitHub-BaSyx_Go-black?logo=github)](https://github.com/eclipse-basyx/basyx-go-components)
![AAS Metamodel](https://img.shields.io/badge/AAS_Metamodel-v3.2-yellow)
![DPP API specification](https://img.shields.io/badge/DPP_API_spec-v1.0.0-blue)

The BaSyx Go Digital Product Passport (DPP) API creates, retrieves, updates, and deletes Digital Product Passports through a dedicated HTTP API. Its OpenAPI document identifies the API as aligned with the DPP annexes of IDTA-01001 and IDTA-01002 v3.2.

## Data Model and Persistence

The DPP API maps each passport to AAS data in PostgreSQL:

- the DPP identifier is also the identifier of the owning AAS;
- the unique product identifier is stored as the AAS `globalAssetId`;
- DPP header fields are stored in a dedicated metadata Submodel;
- each submitted content section is persisted as a content Submodel.

`contentSpecificationIds` determines which content specifications, and therefore which matching content Submodels, are included when the API composes a DPP representation. An empty list can therefore produce a response containing only header metadata even though submitted content sections remain persisted as Submodels.

The DPP service accesses this shared persistence directly. It does not require a separately running AAS Environment, AAS Repository, or Submodel Repository. PostgreSQL must first be initialized or migrated by a release-compatible [Configuration Service](../configuration_service/index).

The DPP identifier uniquely identifies a passport. Each passport carries one unique product identifier, but the database does not make that product identifier unique across passports. Reading a passport by product identifier therefore returns `409 Conflict` when several passports use it.

## Capabilities

BaSyx Go provides:

- atomic creation and partial update of a DPP;
- compressed and expanded full read representations;
- lookup by DPP identifier or unique product identifier;
- paged bulk lookup by up to 100 product identifiers;
- retrieval of a recorded DPP state at a specified time;
- read and replacement of individual elements using RFC 9535 Normalized Paths;
- optional Registry synchronization, history recording, ABAC, and experimental ReBAC.

The write APIs accept only the compressed representation. Full representation writes return `501 Not Implemented`.

## Lifecycle Boundaries

Deleting a DPP removes its owning AAS and DPP metadata Submodel. Content Submodels are retained. If history was enabled before the mutations, states recorded before deletion remain available through the historical DPP endpoint.

The API does not determine whether legal or organizational retention requirements permit deletion. Apply those controls in the deployment and authorization policy.

## API Documentation

With the default empty context path, a running service exposes:

- Swagger UI at `/swagger`;
- the OpenAPI document at `/api-docs/openapi.yaml`;
- health status at `/health`.

Paths are relative to the configured service base URL. If `server.contextPath` is set, it prefixes these paths and all DPP routes.

## Get Started

1. [Set up the DPP API](setup).
2. [Create and use a Digital Product Passport](usage).

For common deployment, configuration, and security behavior, see [Deployment and Versions](../common/deployment), [General Configuration](../common/configuration), and [Runtime Security](../common/security).

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
