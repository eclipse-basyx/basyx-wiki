# Validation

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

## Check a Payload Before Writing It

The Go HTTP services, including both Repositories and both Registries, can expose `POST {contextPath}/verify` when `server.verificationEndpointAvailable` is enabled. This shared endpoint verifies AAS model content; it is not a Registry descriptor-validation endpoint. It accepts JSON, XML, and AASX payloads. Supported model content includes AAS Environments and individual AAS model objects accepted by the parser.

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

Use `curl.exe` in PowerShell and add the service context path if configured. Expect `200 OK`, `valid: true`, and an empty `messages` array. The response also identifies the format and counts the contained AAS, Submodels, and Concept Descriptions.

Change `idShort` to `1Invalid` and submit again. A parsed payload with semantic violations returns `200 OK` with `valid: false` and diagnostic `messages`. Inspect `valid`; HTTP success alone does not mean the model passed verification. This explicit verification reports violations independently of the write-verification mode.

On a write route using semantic verification, the same invalid `idShort` is rejected in `strict` mode, logged in `permissive` mode, and not checked by the semantic verifier in `off` mode. Other write checks may still reject the request in any mode.

## Other Failures

Malformed or unsupported input produces an error response, commonly `400`. Requests exceeding the configured upload limit return `413`. AASX verification also applies package-expansion limits. See [General Configuration](configuration#general) for limits and [API Errors](api_errors) for interpreting failures.

Source: [shared verification endpoint](https://github.com/eclipse-basyx/basyx-go-components/blob/main/internal/common/endpoints.go).
