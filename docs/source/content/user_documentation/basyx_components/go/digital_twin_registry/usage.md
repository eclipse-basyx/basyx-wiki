# Using the Digital Twin Registry

This walkthrough registers a motor AAS Descriptor, verifies automatic Discovery synchronization, resolves the AAS from asset information, retrieves its descriptor, and exercises the DTR-specific AssetLink and filtering behavior.

The examples use the unsecured [Docker Compose setup](setup) at `http://localhost:5004` with an empty context path. Run them in order against an example database and save the JSON files in your working directory. The curl commands are single-line commands usable in Bash. In Windows PowerShell, invoke `curl.exe` instead of `curl`.

For generic descriptor CRUD, nested Submodel Descriptors, structured queries, pagination, and bulk operations, see [Using the AAS Registry](../aas_registry/usage). For the standalone Discovery replacement workflow, see [Using Basic Discovery](../basic_discovery/usage).

## Register an AAS Descriptor

Save this as `dtr-descriptor.json`:

```json
{
  "id": "urn:example:aas:dtr:1",
  "idShort": "MotorDTR",
  "assetKind": "Instance",
  "assetType": "Motor",
  "globalAssetId": "urn:example:asset:dtr:1",
  "specificAssetIds": [
    {
      "name": "serialNumber",
      "value": "SN-DTR-001",
      "externalSubjectId": {
        "type": "ExternalReference",
        "keys": [
          { "type": "GlobalReference", "value": "PUBLIC_READABLE" }
        ]
      }
    }
  ],
  "endpoints": [
    {
      "interface": "AAS-3.2",
      "protocolInformation": {
        "href": "https://example.com/shells/dXJuOmV4YW1wbGU6YWFzOmR0cjox",
        "endpointProtocol": "https"
      }
    }
  ]
}
```

Register the descriptor:

```bash
curl -i -X POST http://localhost:5004/shell-descriptors -H 'Content-Type: application/json' --data-binary '@dtr-descriptor.json'
```

Expect `201 Created`. Because the request omits the DTR-specific top-level `createdAt`, the database assigns it. Retrieve the descriptor afterward to obtain the stored `createdAt` value. The DTR also makes the descriptor's `specificAssetIds` available through Discovery and generates a `globalAssetId` AssetLink. No separate Discovery registration is required.

The example marks the serial-number link `PUBLIC_READABLE`. This affects AssetLink matching when a restricted ABAC read policy is active. It does not by itself authorize access to an endpoint. See [Security and Visibility Semantics](index.md#security-and-visibility-semantics).

## Inspect the Synchronized AssetLinks

Path identifiers contain the identifier's UTF-8 bytes encoded with Base64URL. BaSyx Go accepts valid padded and unpadded forms. The unpadded path value for `urn:example:aas:dtr:1` is:

```text
dXJuOmV4YW1wbGU6YWFzOmR0cjox
```

Read the synchronized AssetLinks:

```bash
curl -i http://localhost:5004/lookup/shells/dXJuOmV4YW1wbGU6YWFzOmR0cjox
```

Expect `200 OK` and an array containing the submitted `serialNumber` link and a generated link with `name` `globalAssetId` and value `urn:example:asset:dtr:1`. The generated global-asset link is marked `PUBLIC_READABLE` for DTR discovery.

## Discover and Retrieve the Descriptor

Save this as `lookup.json`:

```json
[
  { "name": "serialNumber", "value": "SN-DTR-001" }
]
```

Resolve the asset identity to an AAS identifier:

```bash
curl -i -X POST 'http://localhost:5004/lookup/shellsByAssetLink?limit=10' -H 'Content-Type: application/json' --data-binary '@lookup.json'
```

Expect `200 OK`. In a database containing only this example, the response contains the unencoded AAS identifier:

```json
{
  "paging_metadata": {},
  "result": ["urn:example:aas:dtr:1"]
}
```

Use its encoded form to retrieve the descriptor from the AAS Registry API:

```bash
curl -i http://localhost:5004/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOmR0cjox
```

This completes the combined DTR flow: register a descriptor, discover its AAS identifier from asset information, and retrieve its endpoint metadata. An unmatched lookup returns `200 OK`. A DTR empty page can omit `result`, so treat an absent `result` as an empty array.

To discover by the global asset identifier instead, use `{"name":"globalAssetId","value":"urn:example:asset:dtr:1"}` in `lookup.json`. Knowing that value can reveal the associated AAS identifier, but it does not grant permission to read the descriptor.

## Add an AssetLink

Save this as `additional-asset-links.json`:

```json
[
  {
    "name": "customerPartId",
    "value": "CP-4711",
    "externalSubjectId": {
      "type": "ExternalReference",
      "keys": [
        { "type": "GlobalReference", "value": "PUBLIC_READABLE" }
      ]
    }
  }
]
```

Append it to the existing descriptor's Discovery registration, then read the complete link set:

```bash
curl -i -X POST http://localhost:5004/lookup/shells/dXJuOmV4YW1wbGU6YWFzOmR0cjox -H 'Content-Type: application/json' --data-binary '@additional-asset-links.json'
curl -i http://localhost:5004/lookup/shells/dXJuOmV4YW1wbGU6YWFzOmR0cjox
```

The POST returns `201 Created` with the submitted link. Unlike standalone Basic Discovery, DTR POST appends instead of replacing. The descriptor must already exist. Otherwise the request returns `404 Not Found`. The DTR does not deduplicate appended links, so retrying the same POST can create duplicates.

A later full descriptor PUT re-synchronizes Discovery from the replacement descriptor. Include every `specificAssetId` that should remain. An appended link omitted from that replacement is removed. The DTR treats the decoded path identifier as authoritative for descriptor PUT requests. See [Differences from Standalone Registry and Discovery](index.md#differences-from-standalone-registry-and-discovery).

## Filter Descriptors by AssetLinks

`GET /shell-descriptors` accepts repeated `assetIds` parameters. Each value represents a `SpecificAssetId` JSON object, not a plain asset identifier. Serialize the object as compact JSON, encode it as UTF-8 bytes, and then Base64URL-encode those bytes. Valid padded and unpadded Base64URL forms are accepted. This is the same representation used by the [AAS Registry filters](../aas_registry/usage.md#filtering-and-pagination).

For the links used above, the unpadded encodings are:

```text
{"name":"serialNumber","value":"SN-DTR-001"}
eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi1EVFItMDAxIn0

{"name":"customerPartId","value":"CP-4711"}
eyJuYW1lIjoiY3VzdG9tZXJQYXJ0SWQiLCJ2YWx1ZSI6IkNQLTQ3MTEifQ
```

Require both AssetLinks to match the same descriptor:

```bash
curl -i -G http://localhost:5004/shell-descriptors --data-urlencode 'assetIds=eyJuYW1lIjoic2VyaWFsTnVtYmVyIiwidmFsdWUiOiJTTi1EVFItMDAxIn0' --data-urlencode 'assetIds=eyJuYW1lIjoiY3VzdG9tZXJQYXJ0SWQiLCJ2YWx1ZSI6IkNQLTQ3MTEifQ'
```

Expect `200 OK` with the example descriptor in `result`. DTR resolves the decoded `name` and `value` through Discovery and applies **AND** semantics to repeated selectors. Stored AssetLink visibility applies. An `externalSubjectId` included in the query object does not change matching or visibility. Invalid Base64URL, decoded text, JSON, or `SpecificAssetId` content returns `400 Bad Request`.

For the generated global-asset link, encode `{"name":"globalAssetId","value":"urn:example:asset:dtr:1"}`. That exact name selects the DTR's public global-asset-ID discovery behavior described in [Security and Visibility Semantics](index.md#globalassetid-is-a-public-discovery-key).

## Filter by DTR Creation Time

Copy the top-level `createdAt` from the retrieved descriptor and use it as `RETURNED_CREATED_AT` below:

```bash
curl -i -G http://localhost:5004/shell-descriptors --data-urlencode 'createdAfter=RETURNED_CREATED_AT'
```

The RFC 3339 comparison is inclusive, so the example descriptor is eligible when the filter equals its stored DTR `createdAt`. `POST /lookup/shellsByAssetLink` accepts the same query parameter. This timestamp is separate from the descriptor's `administration` timestamps. A client can supply top-level `createdAt` on creation, so it is not necessarily the wall-clock registration time. See [`createdAt` and `createdAfter`](index.md#createdat-and-createdafter).

## Remove the Example Registration

Delete the descriptor:

```bash
curl -i -X DELETE http://localhost:5004/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOmR0cjox
```

Expect `204 No Content`. The descriptor and its synchronized AssetLinks are removed. Subsequent lookups by the example asset identities no longer find the AAS. This does not delete AAS or Submodel content from a Repository.

Calling `DELETE /lookup/shells/{aasIdentifier}` has a different lifecycle: it removes the AAS identifier's AssetLinks but leaves the AAS Descriptor itself. The descriptor's dedicated `globalAssetId` field remains, while its Discovery mapping and returned `specificAssetIds` are removed until a later descriptor write synchronizes them again.
