# Using Basic Discovery

This walkthrough uses the unsecured, standalone [Compose setup](setup) at `http://localhost:8086`, with an empty context path. Save the JSON files in your working directory and run the commands in order against an example database. In Windows PowerShell, use `curl.exe` instead of `curl`. Include any configured context path in each URL.

The requests below demonstrate standalone Discovery replacement and deletion. DTR changes the asset-link POST to append semantics and requires an existing descriptor; compare [Standalone and DTR Behavior](../digital_twin_registry/index.md#standalone-and-dtr-behavior). If Discovery is integrated with an AAS Registry, also read [Shared Registry Asset Identifiers](index.md#shared-registry-asset-identifiers) before changing mappings.

Only the Discovery Service, PostgreSQL, and the Configuration Service are required. A Registry or Repository is needed only when continuing from the discovered identifier to a descriptor or AAS content.

## Register Asset Links

Save this as `asset-links.json`:

```json
[
  { "name": "globalAssetId", "value": "urn:example:asset:1" },
  { "name": "serialNumber", "value": "SN-001" }
]
```

Register the links for `urn:example:aas:1`. Its Base64URL-encoded path value is `dXJuOmV4YW1wbGU6YWFzOjE`:

```bash
curl -i -X POST http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE -H 'Content-Type: application/json' --data-binary '@asset-links.json'
```

Expect `201 Created` and an array containing the submitted links. No pre-existing AAS in a Repository is required. Repeating POST replaces the links for this AAS identifier rather than reporting a duplicate-registration conflict.

Keep asset names and values in the body unencoded. Use the [encoding commands](../common/encoding.md#encode-your-own-identifier) when substituting your own AAS identifier.

## Retrieve the Registered Links

```bash
curl -i http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK` and a JSON array of asset identifiers, including `globalAssetId` and `serialNumber`. This response contains the registered links, not AAS content or an endpoint descriptor.

## Find an AAS by an Asset Identifier

Save this as `lookup.json`:

```json
[
  { "name": "serialNumber", "value": "SN-001" }
]
```

```bash
curl -i -X POST 'http://localhost:8086/lookup/shellsByAssetLink?limit=10' -H 'Content-Type: application/json' --data-binary '@lookup.json'
```

Expect `200 OK`. In a database containing only this example, the response is:

```json
{
  "paging_metadata": {},
  "result": ["urn:example:aas:1"]
}
```

The returned AAS identifier is unencoded. Encode it before using it in a Registry or Repository URL. For example, if the corresponding descriptor has also been registered in the [AAS Registry](../aas_registry/usage), retrieve it with:

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

That Registry request requires a separate Registry setup and descriptor registration. Discovery registration alone does not create the descriptor.

### Global Asset Identifier Lookup

Replace the contents of `lookup.json` with:

```json
[
  { "name": "globalAssetId", "value": "urn:example:asset:1" }
]
```

Repeat the POST lookup request. Expect the same AAS identifier. To require both the global asset identifier and serial number, send both objects in the lookup array. All supplied links must match; adding an unmatched link produces no match for this AAS.

### Pagination

The `limit` and `cursor` parameters apply to the POST lookup endpoint. For additional pages, submit the same lookup body with the returned cursor:

```bash
curl -i -X POST 'http://localhost:8086/lookup/shellsByAssetLink?limit=10&cursor=RETURNED_CURSOR' -H 'Content-Type: application/json' --data-binary '@lookup.json'
```

Replace `RETURNED_CURSOR` with the server-provided value, URL-escaped as needed. The single registration above has no next page. See [Keep the Same Search](../common/pagination.md#keep-the-same-search) for the shared continuation rules. An unmatched lookup returns `200 OK` with an empty `result`; it does not return `404`.

### Deprecated GET Lookup

For existing clients, `GET /lookup/shells` accepts `assetIds` query parameters containing Base64URL-encoded JSON asset links. The preferred POST endpoint avoids this additional encoding step. For the original serial-number lookup:

```bash
curl -i -G http://localhost:8086/lookup/shells --data-urlencode 'assetIds=eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi0wMDEifQ'
```

The encoded value represents `{"name":"serialNumber","value":"SN-001"}`. Expect the same paged AAS identifier response as the POST lookup.

## Replace the Asset Links

```{warning}
This standalone POST removes the current linked asset-identifier rows before inserting standalone Discovery mapping rows. With Registry Discovery integration, removing previously shared rows can also remove entries from the AAS descriptor's visible `specificAssetIds`. It does not delete the descriptor or Repository content. See [Shared Registry Asset Identifiers](index.md#shared-registry-asset-identifiers).
```

Change the serial number in `asset-links.json` to `SN-002`, retaining the global asset identifier:

```json
[
  { "name": "globalAssetId", "value": "urn:example:asset:1" },
  { "name": "serialNumber", "value": "SN-002" }
]
```

Submit the complete replacement:

```bash
curl -i -X POST http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE -H 'Content-Type: application/json' --data-binary '@asset-links.json'
curl -i http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `201 Created` for the replacement and `200 OK` for the read. A lookup by `SN-001` now returns an empty result; a lookup by `SN-002` finds the AAS. Global asset identifier lookup still finds it because that link was retained. Omitting a link from the replacement removes it from the registered set.

## Delete the Discovery Registration

```{warning}
In a Registry-integrated deployment, this deletion can remove linked specific-asset-ID rows that are also visible through the descriptor. It does not delete the descriptor or any Repository AAS/Submodel content. See [Shared Registry Asset Identifiers](index.md#shared-registry-asset-identifiers).
```

```bash
curl -i -X DELETE http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE
curl -i http://localhost:8086/lookup/shells/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `204 No Content` for deletion and `404 Not Found` for the subsequent read. Repeating an asset-link lookup returns an empty result for this example. The AAS content in a Repository is unaffected.

## Shared API Guidance

See [Identifiers and Encoding](../common/encoding), [Pagination](../common/pagination), [API Errors](../common/api_errors), and [Validation](../common/validation). The shared `/verify` endpoint verifies AAS model content; it is not a Discovery asset-link validation endpoint.
