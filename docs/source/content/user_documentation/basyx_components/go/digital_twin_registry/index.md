# Digital Twin Registry

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.1.1-yellow)
![API](https://img.shields.io/badge/API-v3.2.0-yellow)

## Contents

* [Creating your own Set-Up](setup)

The BaSyx Digital Twin Registry (DTR) combines the AAS Registry API and Basic Discovery API in one service. Registering an AAS descriptor also makes its asset identifiers available to Discovery, so clients normally do not have to maintain the same mapping through two services.

The API badge describes the OpenAPI document shipped with the component; see [Version Scope](../common/deployment.md#version-scope). The exact API for a running instance is available through its Swagger UI at `/swagger`.

## Standard APIs Included in the DTR

### AAS Registry API 3.2

The DTR includes the AAS Registry operations for:

- AAS descriptor CRUD and paged listing, including AAS-scoped Submodel Descriptors
- structured descriptor queries through `POST /query/shell-descriptors`
- asynchronous bulk creation, replacement, and deletion, including bulk status and result retrieval

`POST /query/shell-descriptors` is part of the standalone AAS Registry API as well; it is not a DTR-specific extension. See [AAS Registry](../aas_registry/index) for the Registry concepts and common behavior.

### Basic Discovery API

The DTR includes asset-link lookup and management from the [Basic Discovery Component](../basic_discovery/index):

- `POST /lookup/shellsByAssetLink` searches for AAS identifiers by AssetLinks.
- `POST /lookup/shells/{aasIdentifier}` adds AssetLinks to an existing DTR descriptor.
- `GET /lookup/shells/{aasIdentifier}` returns the AssetLinks associated with an AAS identifier.
- `GET /lookup/shells` remains supported but is **deprecated**. New integrations should use `POST /lookup/shellsByAssetLink`, whose request body carries the AssetLinks.

The service also exposes its API description through `GET /description`.

## Digital Twin Registry-Specific Behavior

### Registry and Discovery Synchronization

Discovery integration is always enabled in the DTR:

- Creating an AAS descriptor registers its `specificAssetIds` for Discovery.
- Updating a descriptor updates the Discovery mappings derived from the descriptor. Changed or removed descriptor AssetLinks therefore replace the corresponding synchronized mappings.
- Deleting a descriptor removes its descriptor-linked Discovery mappings.
- A non-empty descriptor `globalAssetId` is also represented as a generated AssetLink named `globalAssetId`. The DTR marks this generated link `PUBLIC_READABLE` because it is a public discovery selector.

No separate Discovery request is required for identifiers supplied in the descriptor. `POST /lookup/shells/{aasIdentifier}` can add further AssetLinks, but the descriptor must already exist.

### `assetIds` on `GET /shell-descriptors`

In the DTR, each repeated `assetIds` query value is interpreted as an encoded AssetLink selector, not as a plain asset identifier. Construct each value as follows:

1. Create a JSON `SpecificAssetId` object containing at least `name` and `value`, for example `{"name":"customerPartId","value":"4711"}`.
2. Encode the JSON text as UTF-8 bytes and then Base64URL-encode those bytes. Correctly padded and unpadded Base64URL forms are accepted.
3. Repeat the query parameter to request more than one link: `?assetIds=<encoded-link-1>&assetIds=<encoded-link-2>`.

Only the encoded object's `name` and `value` select the AssetLink. Visibility is determined from the matching stored AssetLink, not from an `externalSubjectId` included in the query value. When several values are supplied, a descriptor must match **all** requested links. Invalid Base64URL, non-UTF-8 content, invalid JSON, or an invalid `SpecificAssetId` produces `400 Bad Request`.

The lookup is subject to the [AssetLink visibility rules](#assetlink-visibility-and-edc-bpn) below. A selector whose `name` is exactly `globalAssetId` uses the special global-asset-ID discovery behavior.

### `createdAt` and `createdAfter`

The DTR's AAS descriptor list and individual descriptor responses include a top-level `createdAt` timestamp. It is the descriptor's stored registration-creation timestamp and remains unchanged when the descriptor is updated. It is distinct from timestamps inside the descriptor's `administration` object.

The optional `createdAfter` query parameter is supported on:

- `GET /shell-descriptors`
- `POST /lookup/shellsByAssetLink`

Its value must be an RFC 3339 date-time, for example `2026-09-25T10:15:30Z`; an invalid value produces `400 Bad Request`. The comparison is inclusive: a result is eligible when its DTR descriptor `createdAt` is equal to or later than `createdAfter`. On the Discovery POST, this is the creation timestamp of the associated AAS descriptor, not the time at which an AssetLink was added.

`createdAfter` is not part of the declared contract for deprecated `GET /lookup/shells` and should not be used there.

### Submodel Descriptor Compatibility

The standard Submodel Descriptor field is `supplementalSemanticIds` (plural). For compatibility with clients that use `supplementalSemanticId` (singular), the DTR's shipped configuration sets `general.supportsSingularSupplementalSemanticId: true`. In that mode, DTR accepts and emits the singular form. Set the option to `false` to use the plural form instead; clients and the service must agree on the selected representation.

## Security and Visibility Semantics

### AssetLink Visibility and `Edc-Bpn`

When a restricted ABAC `READ` policy is applied to an AssetLink lookup, a normal AssetLink is eligible only when its stored `name` and `value` match and one of these conditions is true:

- one of the stored `externalSubjectId.keys[].value` values exactly equals the caller's `Edc-Bpn` claim; or
- one of those values is the literal `PUBLIC_READABLE`.

`PUBLIC_READABLE` therefore makes that AssetLink usable by any caller that is otherwise authorized to invoke the operation. A missing or non-matching `externalSubjectId` does not make a normal link visible under a restricted read. When multiple AssetLinks are requested, every requested link must match and be visible. An unrestricted `READ` authorization does not apply this per-link BPN filter.

`Edc-Bpn` can come from a signed claim. If `general.enableCustomMiddlewareHeaderInjection` is enabled, the service instead copies the request header `Edc-Bpn` into the claims used for filtering. Header injection is disabled by default.

```{warning}
A caller-supplied `Edc-Bpn` header is not authenticated identity. If header-to-claim injection is enabled, place the DTR behind a trusted intermediary, prevent direct client access, and have the intermediary strip or overwrite incoming `Edc-Bpn` values before setting the verified identity. Otherwise a caller can spoof another party's BPN.
```

Prefer a signed claim from a trusted identity provider when possible. Authentication, ABAC, trust-list, and header-injection settings are described in [General Configuration](../common/configuration.md#oidc-and-abac).

### `globalAssetId` Is a Public Discovery Key

The generated `globalAssetId` AssetLink is intentionally `PUBLIC_READABLE`. A caller that knows a descriptor's `globalAssetId` can use an AssetLink selector with `name` set to `globalAssetId` to discover the corresponding AAS identifier, subject to authorization for the Discovery operation itself.

This does **not** grant authorization to read the full AAS descriptor. Descriptor access and field visibility are evaluated separately. In particular, an ABAC policy that hides the `globalAssetId` field in descriptor responses does not make the value private as a discovery key. Do not use `globalAssetId` for sensitive identifiers whose knowledge must not reveal that an AAS exists.

If `abac.policyFileImport` is omitted, the DTR uses `always`: the configured access-rules file is imported on every startup and supersedes the active database policy. Choose `always`, `if_missing`, or `never` deliberately; see the [`abac` configuration](../common/configuration.md#oidc-and-abac).

## Differences from Standalone Registry and Discovery

| Operation or topic | Standalone service | DTR behavior | Client implication |
| --- | --- | --- | --- |
| `POST /lookup/shells/{aasIdentifier}` | Basic Discovery replaces the complete AssetLink set. | DTR appends the submitted links, does not remove duplicates, and requires the AAS descriptor to exist. | Create the descriptor first, send only additions, and avoid blind retries if duplicates matter. |
| Descriptor PUT path/body IDs | Standalone AAS Registry rejects an empty body ID or one that differs from the decoded path ID. | For AAS descriptors and nested Submodel Descriptors, DTR treats the decoded path identifier as authoritative and replaces the body ID. | Treat the path as the update target; a conflicting body ID does not select another resource. |
| `GET /shell-descriptors?assetIds=...` | Registry filtering follows the standalone Registry behavior. | DTR resolves encoded `name`/`value` selectors through Discovery and applies DTR AssetLink visibility. | Do not send plain asset IDs; follow the DTR encoding and visibility rules above. |
| Empty Discovery search result | Standalone Discovery returns a paged wrapper with `"result": []`. | A DTR search can omit `result` and return `{"paging_metadata": {}}`. | Treat an absent `result` as an empty page. |
| Descriptor/Discovery synchronization | The standalone services can be operated independently. | DTR synchronizes descriptor identifiers into Discovery automatically. | Do not register the descriptor's identifiers a second time. |

Path identifiers such as `aasIdentifier` and `submodelIdentifier` contain the identifier encoded as UTF-8 bytes and then Base64URL-encoded. Correctly padded and unpadded forms are accepted.

## Related Documentation

- [Setting Up the Digital Twin Registry](setup)
- [AAS Registry](../aas_registry/index)
- [Basic Discovery](../basic_discovery/index)
- [General Configuration](../common/configuration)
- [Pagination](../common/pagination)
- [Asynchronous Requests](../common/asynchronous_requests)
- [Swagger UI](../common/swagger)

```{toctree}
:hidden:
:maxdepth: 1

setup
```
