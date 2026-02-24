# AAS Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.1.1-yellow)

## Contents
* [Creating your own Set-Up](setup)

The BaSyx AAS Registry implements the Asset Administration Shell Registry API. It stores and serves Asset Administration Shell Descriptors and the Submodel Descriptors associated with a registered AAS.

## API Endpoints

### AAS Descriptor Endpoints

- `GET /shell-descriptors`: Returns AAS Descriptors (supports pagination and filtering such as `assetKind` and `assetType`).
- `POST /shell-descriptors`: Registers a new AAS Descriptor.
- `GET /shell-descriptors/{aasIdentifier}`: Returns a specific AAS Descriptor.
- `PUT /shell-descriptors/{aasIdentifier}`: Creates or updates an AAS Descriptor.
- `DELETE /shell-descriptors/{aasIdentifier}`: De-registers an AAS Descriptor.

### AAS-scoped Submodel Descriptor Endpoints

- `GET /shell-descriptors/{aasIdentifier}/submodel-descriptors`: Returns Submodel Descriptors linked to the AAS.
- `POST /shell-descriptors/{aasIdentifier}/submodel-descriptors`: Registers a Submodel Descriptor under the AAS.
- `GET /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier}`: Returns a specific Submodel Descriptor of the AAS.
- `PUT /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier}`: Creates or updates a specific Submodel Descriptor of the AAS.
- `DELETE /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier}`: De-registers a specific Submodel Descriptor of the AAS.

## Component-Specific Notes

- `GET /shell-descriptors` supports cursor-based pagination (`limit`, `cursor`).
- `GET /shell-descriptors` additionally supports asset-based filtering (`assetKind`, `assetType`).
- Path identifiers (`aasIdentifier`, `submodelIdentifier`) must be UTF8 base64 URL encoded.

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
