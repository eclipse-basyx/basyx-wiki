# Response Representations

Repository APIs can expose different views of the same model content. Choose a representation according to what the client needs, and check the operation in the running [Swagger UI](swagger) before adding a suffix or modifier. Support is endpoint-specific; Registry descriptors do not automatically support Repository representation routes.

## Choose a Representation

| Suffix | Purpose |
| --- | --- |
| None | Normal model JSON, including model metadata and values. |
| `$value` | Value-oriented content, useful to applications reading element values. |
| `$metadata` | Model metadata without runtime values. |
| `$reference` | A reference identifying the resource. |
| `$path` | Paths addressing contained elements, where exposed. |

The Submodel Repository provides representation routes for Submodels and Submodel Elements as specified by each operation. AAS-scoped Submodel routes delegate to Submodel behavior. Do not assume that an AAS resource itself supports every Submodel representation.

## Compare Normal and Value Reads

Create the example Submodel from [Submodel Repository Usage](../submodel_repository/usage), then read its `Nameplate.SerialNumber` Property. Set the base URL to that of your running Repository:

```bash
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber'
curl -i 'http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ/submodel-elements/Nameplate.SerialNumber/$value'
```

The first response contains the Property model, including its `modelType`, `idShort`, `valueType`, and value. The second contains its value representation. Keep dollar-sign paths in single quotes in Bash and PowerShell so the shell does not expand them. In PowerShell, use `curl.exe`. Adjust the port and context path to your deployment.

## Depth and Blob Content

Where the read operation exposes them:

| Modifier | Effect |
| --- | --- |
| `level=deep` | Include nested content. |
| `level=core` | Limit the representation to its core level. |
| `extent=withoutBlobValue` | Omit Blob payload values. |
| `extent=withBlobValue` | Include Blob payload values. |

These modifiers change the response, not the stored resource. They do not download a File element's attachment. Use the component's attachment endpoint for that.

## Writing a Representation

Use the request schema of the specific write endpoint. A `$value` response is not a complete resource body for a normal PUT. Submodel PATCH routes expect their corresponding normal, metadata, or value representation, rather than an RFC 6902 JSON Patch array. Keep resource-specific PATCH examples in [Submodel Repository Usage](../submodel_repository/usage).

For Submodel Element `$metadata` PATCH requests, this implementation accepts common metadata fields such as `description`, but rejects `valueType`. The existing Property datatype is retained. See the [metadata PATCH example](../submodel_repository/usage.md#representations-and-partial-updates).

Full Environment import/export is a separate capability; representation suffixes do not imply support for `/serialization` in a standalone service.
