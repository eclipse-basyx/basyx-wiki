# Validation and Verification

Validation helps distinguish malformed requests from AAS model content that can be parsed but violates model constraints. Successfully validating a payload does not store it or guarantee that a later write will succeed: resource conflicts and endpoint-specific requirements are checked by the write operation.

## Verification During Writes

The shared `server.strictVerification` setting controls semantic verification on request-body paths that use the shared model verifier:

| Mode | Behavior |
| --- | --- |
| `off` | Skip semantic verification. Parsing and endpoint-specific checks still apply. |
| `permissive` (configuration default) | Log semantic violations as warnings and continue processing. |
| `strict` | Reject semantic violations. |

For a deployment that should reject invalid model content, merge this into its configuration and restart the service:

```yaml
server:
  strictVerification: strict
  verificationEndpointAvailable: true
```

The equivalent variables are `SERVER_STRICTVERIFICATION=strict` and `SERVER_VERIFICATIONENDPOINTAVAILABLE=true`. See [General Configuration](configuration) for loading and precedence. Neither `off` nor `permissive` makes malformed JSON acceptable.

The mode also applies to the creation and replacement of Concept Descriptions in the Concept Description Repository and the AAS Environment, including imports. In `strict` mode, a rejected write returns `400 Bad Request` and stores nothing.

### Submodel Element Lists and PATCH

Writes of `SubmodelElementList` members are verified against the enclosing list: `PUT` and `PATCH` of a member, `POST` of a new member into a list, and `PATCH` of a list. In `strict` mode, a member that violates the list's `typeValueListElement`, `valueTypeListElement`, or `semanticIdListElement` (AASd-107, AASd-108, AASd-109) is rejected. Verification covers the complete stored list, also when access rules hide some members from the caller.

A `PATCH` of a Submodel Element, including a `$metadata` PATCH, is verified on the merged result with the element's stored value, not only on the request payload.

## idShort Rules

Every verification mode, including `off`, rejects an `idShort` that does not match the idShort type of the AAS metamodel:

- 2 to 128 characters;
- only letters, digits, `-`, and `_`;
- starts with a letter and does not end with `-`.

This applies to AASs, Submodels, Concept Descriptions, and Submodel Elements written with `POST`, `PUT`, or `PATCH`, including `$metadata` PATCH and AAS Environment uploads. An optional `idShort` may be omitted, but an explicit empty string is invalid. Single-letter idShorts such as `X`, which some IDTA Submodel Templates use, are rejected as well. A rejected write returns `400 Bad Request` with an error code ending in `-INVALIDIDSHORT` in the message text.

A Submodel Element must have an `idShort` unless it is a direct member of a `SubmodelElementList` (AASd-117). This applies in every mode to top-level elements, collection values, Entity statements, annotations, and Operation variable values. A missing `idShort` returns `400 Bad Request` with an error code ending in `-MISSINGIDSHORT`, unless `strict` verification already rejects the request with its own error.

```{note}
Resources stored by earlier versions with invalid idShorts are not migrated or repaired. Delete them and create them again with valid idShorts.

Elements stored by earlier versions without `idShort` remain stored, and a `PATCH` that does not include them is not affected. Writing them back unchanged, for example by `PUT`ting a Submodel as it was read, is rejected. Add the missing idShorts in that `PUT` to repair them.
```

## Check a Payload Before Writing It

Except for the standalone DPP API, the BaSyx Go HTTP services can expose `POST {contextPath}/verify` when `server.verificationEndpointAvailable` is enabled. The DPP API does not register this endpoint. This shared endpoint verifies AAS model content. It is not a Registry descriptor-validation endpoint. It accepts JSON, XML, and AASX payloads. Supported model content includes AAS Environments and individual AAS model objects accepted by the parser.

Verification payloads use `general.uploadMaxSizeBytes`, which defaults to 128 MiB. A request that exceeds the applicable payload limit is rejected with `413 Request Entity Too Large`.

Save this as `verify-submodel.json`:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:verification",
  "idShort": "VerificationExample"
}
```

Using the AAS Repository at port `8084`:

```bash
curl -i -X POST http://localhost:8084/verify -H 'Content-Type: application/json' --data-binary '@verify-submodel.json'
```

Add the service context path if configured. Expect `200 OK`, `valid: true`, and an empty `messages` array. The response also identifies the format and counts the contained AAS, Submodels, and Concept Descriptions.

Change `idShort` to `1Invalid` and submit again. A parsed payload with semantic violations returns `200 OK` with `valid: false` and diagnostic `messages`. Inspect `valid`; HTTP success alone does not mean the model passed verification. This explicit verification reports violations independently of the write-verification mode.

On a write route, the same invalid `idShort` is rejected in every mode; see [idShort Rules](#idshort-rules). Other semantic violations are rejected in `strict` mode, logged in `permissive` mode, and not checked in `off` mode.
