# Basic Discovery Component

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.1.1-yellow)

## Contents
* [Creating your own Set-Up](setup)

The BaSyx Basic Discovery component implements the Asset Administration Shell Basic Discovery API. It is used to resolve Asset Administration Shell (AAS) identifiers from asset links (including the global asset ID) and to manage the discoverable asset links of a specific AAS.

## API Endpoints

The component exposes the following Basic Discovery endpoints:

- `GET /lookup/shells` (deprecated): Returns AAS IDs linked to asset identifiers or a global asset ID. Supports pagination (`limit`, `cursor`).
- `POST /lookup/shellsByAssetLink`: Returns AAS IDs linked to the provided asset links in the request body. Supports pagination (`limit`, `cursor`).
- `GET /lookup/shells/{aasIdentifier}`: Returns the specific asset identifiers linked to an AAS.
- `POST /lookup/shells/{aasIdentifier}`: Creates or replaces all asset links for an AAS.
- `DELETE /lookup/shells/{aasIdentifier}`: Deletes all asset links for an AAS.

## Component-Specific Notes

- The `POST /lookup/shellsByAssetLink` endpoint is the preferred lookup endpoint (the `GET /lookup/shells` variant is deprecated in the specification).
- Global asset ID lookup is supported by using an asset link with `name = "globalAssetId"`.
- AAS identifiers used in path parameters must be UTF8 base64 URL encoded.

## Common Documentation

This component uses shared BaSyx Go infrastructure for Swagger/OpenAPI and configuration. For components using the shared security setup, OIDC trustlist and ABAC access-rules handling is documented in the shared docs:

- [General Configuration](../common/configuration)
- [Swagger UI Docs](../common/swagger)
- [Security Configuration Files (OIDC trustlist and ABAC access-rules)](../common/configuration#security-files-oidc-trustlist-and-abac-access-rules)
- [Common / Shared Features](../common/shared_features)

```{toctree}
:hidden:
:maxdepth: 1

setup
```
