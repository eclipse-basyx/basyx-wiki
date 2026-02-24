# Submodel Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.1.1-yellow)

## Contents
* [Creating your own Set-Up](setup)

The BaSyx Submodel Registry implements the Submodel Registry API. It stores and serves Submodel Descriptors as standalone registry entries.

## API Endpoints

- `GET /submodel-descriptors`: Returns all Submodel Descriptors (supports pagination via `limit` and `cursor`).
- `POST /submodel-descriptors`: Registers a new Submodel Descriptor.
- `GET /submodel-descriptors/{submodelIdentifier}`: Returns a specific Submodel Descriptor.
- `PUT /submodel-descriptors/{submodelIdentifier}`: Creates or updates a Submodel Descriptor.
- `DELETE /submodel-descriptors/{submodelIdentifier}`: De-registers a Submodel Descriptor.

## Component-Specific Notes

- The registry is focused on Submodel Descriptor lifecycle operations only (standalone submodel registration and lookup).
- Path identifiers (`submodelIdentifier`) must be UTF8 base64 URL encoded.

## Security Configuration Files

Handling of OIDC trustlist and ABAC access-rules files is documented in the shared docs:

- [General Configuration](../common/configuration#security-files-oidc-trustlist-and-abac-access-rules)
- [Common / Shared Features](../common/shared_features)

```{toctree}
:hidden:
:maxdepth: 1

setup
```
