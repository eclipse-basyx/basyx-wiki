# Digital Twin Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.2.0-yellow)

## Contents
* [Creating your own Set-Up](setup)

The BaSyx Digital Twin Registry combines Asset Administration Shell Registry and Basic Discovery capabilities in one component. In this repository, it exposes a combined API and adds Digital Twin Registry-specific query/filter extensions on top of the standard endpoints. The API badge describes the OpenAPI document shipped with BaSyx Go release `1.0.11`; see [Version Scope](../common/deployment.md#version-scope).

## Included API Areas

- [AAS Registry](../aas_registry/index) endpoints (`/shell-descriptors`, including AAS-scoped submodel descriptor endpoints)
- [Basic Discovery Component](../basic_discovery/index) endpoints (`/lookup/shells`, `/lookup/shellsByAssetLink`, `/lookup/shells/{aasIdentifier}`)
- Description endpoint (`/description`)

## Standalone and DTR Behavior

The combined service deliberately changes a few behaviors. Do not assume that every standalone Registry or Discovery behavior is identical in DTR.

| Operation/topic | Standalone behavior | DTR behavior | Client implication |
| --- | --- | --- | --- |
| `POST /lookup/shells/{aasIdentifier}` | Basic Discovery replaces the complete asset-link set: it removes the existing linked rows and inserts the submitted set. | Appends the submitted asset links to the existing rows. The append path does not detect or remove duplicates. | Send a complete desired set to standalone Discovery, but send only additions to DTR and avoid retrying blindly if duplicates matter. |
| Descriptor existence prerequisite | Standalone Discovery can register an AAS identifier without an existing descriptor. | The AAS descriptor must already exist or the asset-link POST returns `404 Not Found`. | Create the descriptor before adding asset links through DTR. |
| Path/body ID precedence on descriptor PUT | Standalone AAS Registry rejects an empty body ID or a body ID that differs from the decoded path ID. | For the verified AAS-descriptor and nested Submodel-descriptor PUT wrappers, the decoded path identifier is authoritative and replaces the corresponding body ID before the Registry operation runs. | Treat the path as the update target; a conflicting body ID does not select another resource. |
| Empty asset-link search result | Standalone Discovery returns a paged wrapper whose `result` is an empty array. | An empty DTR Discovery search can omit `result`; the response shape is `{"paging_metadata": {}}`. | Accept an absent `result` as an empty page instead of requiring `"result": []`. |

See [Using standalone Basic Discovery](../basic_discovery/usage) for its request flow and [Shared Registry Asset Identifiers](../basic_discovery/index.md#shared-registry-asset-identifiers) for the rows these mutations can affect.

## Digital Twin Registry Extensions

### Query Endpoint for AAS Descriptors

- `POST /query/shell-descriptors`: Queries AAS Descriptors using the query language and supports [pagination](../common/pagination) (`limit`, `cursor`).

### Additional Filtering for Discovery Search

- `POST /lookup/shellsByAssetLink` supports an additional optional query parameter `createdAfter` (RFC3339 date-time).
- If `createdAfter` is invalid, the service returns `400 Bad Request`.

## Edc-Bpn Trust Boundary

`Edc-Bpn` is an optional request header used for query filtering and access-control integration in the combined API. Header-to-claim injection is disabled by default and must be enabled explicitly.

```{warning}
A caller-supplied `Edc-Bpn` header is not authenticated identity. When header injection is enabled, its value is inserted into the claims evaluated by policy. Enabling injection without a trusted boundary therefore lets a direct caller attempt to supply another party's BPN.
```

If a trusted intermediary supplies the header, prevent clients from bypassing that intermediary and reaching DTR directly. The intermediary must strip or overwrite any incoming untrusted copy before setting the verified value. A safer arrangement is to keep header injection disabled and carry the BPN as a signed claim issued by a trusted identity provider. See [Runtime Security](../common/security) for the complete authentication, authorization, and policy workflow.

## Common Documentation

This component uses shared BaSyx Go infrastructure for Swagger/OpenAPI and configuration. For components using the shared security setup, OIDC trustlist and ABAC access-rules handling is documented in the shared docs:

- [General Configuration](../common/configuration)
- [Swagger UI Docs](../common/swagger)
- [Security Configuration Files (OIDC trustlist and ABAC access-rules)](../common/configuration.md#security-files)
- [Common / Shared Features](../common/shared_features)

## Component-Specific Notes

- The Digital Twin Registry service in this repository always runs with discovery integration enabled.
- If `abac.policyFileImport` is omitted, DTR defaults to `always`, so the configured policy file is imported on every start and supersedes the active database policy. Other participating services default to `if_missing`. Choose the mode deliberately; see [Policy Persistence and Restart Behavior](../common/security.md#policy-persistence-and-restart-behavior).
- Path identifiers (`aasIdentifier`, `submodelIdentifier`) must be UTF8 base64 URL encoded.

```{toctree}
:hidden:
:maxdepth: 1

setup
```
