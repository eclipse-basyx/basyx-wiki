# Identifiers and Encoding

Repository and Registry APIs use Base64URL-encoded identifiers in identifier path parameters. Encode the original identifier as UTF-8, use the URL-safe alphabet, and omit trailing `=` padding. Do not encode an already encoded identifier again.

## What to Encode

| Value | How to send it |
| --- | --- |
| AAS or Submodel identifier in an identifier path parameter | Base64URL-encoded original identifier. |
| `id` in a JSON resource, or a reference key's `value` | Original, unencoded identifier. |
| Submodel Element `idShortPath`, such as `Nameplate.SerialNumber` | The element path, without Base64URL encoding. |
| Query parameter | Follow the endpoint's contract. Some require encoded strings, others encoded JSON, and others plain values. |

An AAS identifier, its asset identifier, and its `idShort` identify different things. Use the AAS's `id` to address `/shells/{aasIdentifier}` and `/shell-descriptors/{aasIdentifier}`.

## Encode Your Own Identifier

In Bash, use `printf` to avoid adding a newline:

```bash
printf '%s' 'urn:example:aas:1' | base64 | tr '+/' '-_' | tr -d '=\r\n'
```

In PowerShell:

```powershell
$valueToEncode = 'urn:example:aas:1'
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($valueToEncode)).TrimEnd('=').Replace('+', '-').Replace('/', '_')
```

Both produce `dXJuOmV4YW1wbGU6YWFzOjE`. After creating that AAS using the [AAS Repository walkthrough](../aas_repository/usage), retrieve it with:

```bash
curl -i http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

Use `curl.exe` in PowerShell. Adjust the port and include the configured context path.

## Encoding Query Parameters

Base64URL encoding and URL escaping are separate steps. First encode the value required by the API; then let `curl --data-urlencode` escape it for transport.

For example, the AAS `assetIds` filter takes encoded JSON. Replace the input to either encoding command with the complete string `{"name":"serialNumber","value":"SN-002"}`. It produces `eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDIifQ`:

```bash
curl -i -G http://localhost:8084/shells --data-urlencode 'assetIds=eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDIifQ'
```

The Submodel Repository's `semanticId` filter instead expects an encoded semantic key-value string. Keep these parameter-specific instructions in the component's usage guide. Treat pagination cursors as opaque values and follow [Pagination](pagination), rather than decoding or constructing them.
