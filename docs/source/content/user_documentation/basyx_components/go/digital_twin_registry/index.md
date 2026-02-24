# Digital Twin Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.1.1-yellow)

## Contents
* [Creating your own Set-Up](setup)

The BaSyx Digital Twin Registry combines Asset Administration Shell Registry and Basic Discovery capabilities in one component. In this repository, it exposes a combined API and adds Digital Twin Registry-specific query/filter extensions on top of the standard endpoints.

## Included API Areas

- [AAS Registry](../aas_registry/index) endpoints (`/shell-descriptors`, including AAS-scoped submodel descriptor endpoints)
- [Basic Discovery Component](../basic_discovery/index) endpoints (`/lookup/shells`, `/lookup/shellsByAssetLink`, `/lookup/shells/{aasIdentifier}`)
- Description endpoint (`/description`)

## Digital Twin Registry Extensions

### Query Endpoint for AAS Descriptors

- `POST /query/shell-descriptors`: Queries AAS Descriptors using the query language and supports pagination (`limit`, `cursor`).

### Additional Filtering for Discovery Search

- `POST /lookup/shellsByAssetLink` supports an additional optional query parameter `createdAfter` (RFC3339 date-time).
- If `createdAfter` is invalid, the service returns `400 Bad Request`.

### Optional Header for Filtering / Access Control Integration

- `Edc-Bpn` (optional request header): Used by the Digital Twin Registry API for query filtering / access control integration in the combined API.

## Common Documentation

This component uses shared BaSyx Go infrastructure for Swagger/OpenAPI and configuration. For components using the shared security setup, OIDC trustlist and ABAC access-rules handling is documented in the shared docs:

- [General Configuration](../common/configuration)
- [Swagger UI Docs](../common/swagger)
- [Security Configuration Files (OIDC trustlist and ABAC access-rules)](../common/configuration#security-files-oidc-trustlist-and-abac-access-rules)
- [Common / Shared Features](../common/shared_features)

## Component-Specific Notes

- The Digital Twin Registry service in this repository always runs with discovery integration enabled.
- Path identifiers (`aasIdentifier`, `submodelIdentifier`) must be UTF8 base64 URL encoded.

```{toctree}
:hidden:
:maxdepth: 1

setup
```
