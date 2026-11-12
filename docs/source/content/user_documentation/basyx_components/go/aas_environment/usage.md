# Using the AAS Environment

This walkthrough imports one AAS, its linked Submodel, one Concept Description, and one specific asset identifier. It then verifies Repository, Registry, Discovery, and serialization behavior through the single AAS Environment URL.

Start the [Compose setup](setup) and wait for `http://localhost:8090/health` to return HTTP `200`. Run the commands from one working directory. In Windows PowerShell, use `curl.exe` instead of `curl`.

## Sample Identifiers

The JSON body uses original identifiers. Identifier path parameters and the `/serialization` selection parameters use their UTF-8 Base64URL encodings without padding:

| Resource | Original identifier | Encoded value |
| --- | --- | --- |
| AAS | `urn:example:aas:environment:1` | `dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE` |
| Submodel | `urn:example:submodel:environment:1` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ` |
| Concept Description | `urn:example:concept:serial-number` | `dXJuOmV4YW1wbGU6Y29uY2VwdDpzZXJpYWwtbnVtYmVy` |

When substituting your own identifiers, use the same UTF-8 Base64URL encoding.

## Import an Environment

Save the following as `environment.json`:

```json
{
  "assetAdministrationShells": [
    {
      "id": "urn:example:aas:environment:1",
      "idShort": "EnvironmentMotorAAS",
      "assetInformation": {
        "assetKind": "Instance",
        "specificAssetIds": [
          {
            "name": "serialNumber",
            "value": "SN-ENV-001"
          }
        ]
      },
      "submodels": [
        {
          "type": "ModelReference",
          "keys": [
            {
              "type": "Submodel",
              "value": "urn:example:submodel:environment:1"
            }
          ]
        }
      ],
      "modelType": "AssetAdministrationShell"
    }
  ],
  "submodels": [
    {
      "id": "urn:example:submodel:environment:1",
      "idShort": "EnvironmentNameplate",
      "submodelElements": [
        {
          "idShort": "SerialNumber",
          "semanticId": {
            "type": "ModelReference",
            "keys": [
              {
                "type": "ConceptDescription",
                "value": "urn:example:concept:serial-number"
              }
            ]
          },
          "valueType": "xs:string",
          "value": "SN-ENV-001",
          "modelType": "Property"
        }
      ],
      "modelType": "Submodel"
    }
  ],
  "conceptDescriptions": [
    {
      "id": "urn:example:concept:serial-number",
      "idShort": "SerialNumberConcept",
      "modelType": "ConceptDescription"
    }
  ]
}
```

Upload it as the multipart form field named `file`:

```bash
curl -i -X POST http://localhost:8090/upload -F 'file=@environment.json;type=application/json'
```

The `type=application/json` value is the media type of the multipart **file part**. The request itself is `multipart/form-data`; do not replace `-F` with an ordinary JSON request body or manually set the multipart boundary.

Expect HTTP `200` and a response containing:

```json
{
  "message": "JSON file parsed successfully",
  "fileName": "environment.json",
  "contentType": "application/json",
  "format": "json",
  "assetAdministrationShellCount": 1,
  "submodelCount": 1,
  "conceptDescriptionCount": 1
}
```

The endpoint accepts plain AAS Environment documents using `application/json`, `application/xml`, or `text/xml`. AASX packages use `application/aasx+json`, `application/aasx+xml`, `application/asset-administration-shell+json`, or `application/asset-administration-shell+xml`. Supply the actual format as the `file` part's media type, for example `-F 'file=@environment.aasx;type=application/aasx+json'`. If the part has no media type or `application/octet-stream`, the format is inferred from the extension (`.aasx`, `.json`, or `.xml`) of the optional `fileName` form field or of the file part's filename, and otherwise from the content.

Uploads are size-limited. The default maximum uploaded file-content size is 128 MiB (`134217728` bytes), and AASX packages are subject to additional limits on package parts, OPC metadata, individual expanded parts, total expanded content, and thumbnails. See [General Configuration](../common/configuration.md#general) when larger uploads require different limits.

A File element in an AASX package is imported with its attachment only when the referenced package part is related to the AAS specification part as `aas-suppl` (IDTA-01005). If it references another part of the package, for example the package thumbnail, no attachment is imported for it, and the service logs the warning `AASENV-UPLDSUPPL-NOSUPPLREL` with the Submodel, idShort path, and part.

## Retrieve the Imported Content

Retrieve each stored object through its Repository API. Every path identifier below is encoded:

```bash
curl -i http://localhost:8090/shells/dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE
curl -i http://localhost:8090/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ
curl -i http://localhost:8090/concept-descriptions/dXJuOmV4YW1wbGU6Y29uY2VwdDpzZXJpYWwtbnVtYmVy
```

Expect HTTP `200` for all three. Check `idShort` values `EnvironmentMotorAAS`, `EnvironmentNameplate`, and `SerialNumberConcept`. The AAS contains a reference to the Submodel; the Submodel content is stored independently, and its `SerialNumber` Property refers to the Concept Description.

For more operations and replacement semantics, use the [AAS Repository](../aas_repository/usage) and [Submodel Repository](../submodel_repository/usage) guides. The complete composed contract, including Concept Description operations, is available in the Environment's `/swagger` UI.

## Check Registration and Discovery

The setup explicitly enabled both Repository-to-Registry synchronization flags. The upload therefore also upserts descriptors whose endpoint URLs start with `http://localhost:8090`:

```bash
curl -i http://localhost:8090/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE
curl -i http://localhost:8090/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ
```

Expect HTTP `200`. The AAS Descriptor contains `specificAssetIds` with `serialNumber` = `SN-ENV-001`; the Submodel Descriptor identifies `urn:example:submodel:environment:1`. Registry endpoints being present would not have caused these writes without the two explicit flags.

Because this executable forces Discovery integration on, the synchronized AAS Descriptor also maintains its asset-link mapping. Save this as `lookup.json`:

```json
[
  {
    "name": "serialNumber",
    "value": "SN-ENV-001"
  }
]
```

Resolve that specific asset identifier:

```bash
curl -i -X POST 'http://localhost:8090/lookup/shellsByAssetLink?limit=10' -H 'Content-Type: application/json' --data-binary '@lookup.json'
```

Expect HTTP `200` and `urn:example:aas:environment:1` in the response `result` array. Discovery returns an AAS identifier, not Repository content or a descriptor. See [Basic Discovery](../basic_discovery/usage) and [Registry Integration](../common/registry_integration) for the deeper semantics.

## Export Selected Data

Request the same AAS and Submodel explicitly and include Concept Descriptions. The `Accept` header selects a plain JSON AAS Environment response:

```bash
curl -G http://localhost:8090/serialization \
  -H 'Accept: application/json' \
  --data-urlencode 'aasIds=dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE' \
  --data-urlencode 'submodelIds=dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ' \
  --data-urlencode 'includeConceptDescriptions=true' \
  -o exported-environment.json
```

Open `exported-environment.json` and verify the same three original identifiers. `aasIds` and `submodelIds` accept Base64URL-encoded identifiers and may be repeated to select several resources. **Only explicitly selected AASs and Submodels are exported.** An omitted selector selects no objects of that type. Selecting an AAS does not automatically include its referenced Submodels. Supplying neither selector returns `400 Bad Request`.

`includeConceptDescriptions` defaults to `true`. It includes only readable Concept Descriptions referenced directly or indirectly by the serialized Submodels, including semantic IDs, inherited `semanticIdListElement` values, value IDs, and references from included Concept Descriptions such as IEC 61360 value-list entries. Set it to `false` to omit all Concept Descriptions. Unreferenced Concept Descriptions are not exported.

To export an AASX package with a JSON specification part, change the media type and output filename while keeping the same query parameters:

```bash
curl -G http://localhost:8090/serialization \
  -H 'Accept: application/aasx+json' \
  --data-urlencode 'aasIds=dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE' \
  --data-urlencode 'submodelIds=dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ' \
  --data-urlencode 'includeConceptDescriptions=true' \
  -o exported-environment.aasx
```

The resulting AASX can be imported through `/upload` with `-F 'file=@exported-environment.aasx;type=application/aasx+json'`. Plain XML and XML-based AASX representations are also available; always send an explicit `Accept` header so the chosen representation is unambiguous.

`Accept: application/aas+zip`, the AASX media type of the IDTA OpenAPI and Part 5, returns an AASX package with an XML specification part and the response `Content-Type` `application/aas+zip`. To import such a package through `/upload`, declare the file part as `application/aasx+xml`.

### Export Limits

The JSON or XML environment specification, including inside an AASX package, is limited by `general.aasxMaxPartExpandedSizeBytes` (default 128 MiB). Exceeding an export limit returns `413 Request Entity Too Large`. See [General Configuration](../common/configuration.md#general) for all export limits.

### Import and Export Permissions

With runtime security enabled, permissions are type-specific: access to an AAS does not automatically include its Submodels or Concept Descriptions.

Explicitly selecting a missing or inaccessible AAS or Submodel aborts the export with `404`, without returning a partial selection. A caller without permission to use the import or export endpoint receives `403`.

Imports through `/upload` and `/upload-async` require CREATE for new content and UPDATE for existing content, including attachments and thumbnails. See [Runtime Security](../common/security.md#environment-import-and-export) for grant syntax, filtering rules, binary-content permissions, and a policy example.

## Re-import and Failure Behavior

Uploading the same identifiers again uses replace-on-upload behavior: existing Concept Descriptions, Submodels, and AASs are updated rather than rejected as package-level duplicates. Treat the submitted objects as complete replacements and preserve every field that should remain.

An upload is all-or-nothing. Its Concept Descriptions, Submodels, and AASs, the AASX thumbnails and supplementary files, and the synchronized Registry descriptors are stored in one transaction, together with their history and Eventing outbox entries. If any of them is rejected, nothing from the upload is stored. The error message starts with `AASENV-PROCESSENV-ROLLEDBACK`, states that nothing was stored, and names the rejected resource or package part, for example:

```text
AASENV-PROCESSENV-ROLLEDBACK upload rejected, nothing from the uploaded environment was stored: AASENV-PROCESSENV-PUTSM failed to store Submodel "urn:example:submodel": 403 Denied: ...
```

The HTTP status reflects the rejection, for example `400`, `403`, or `409`. Correct the rejected resource and upload the complete file again.

## Import Asynchronously

`POST /upload-async` accepts the same multipart request as `/upload` and imports the file in the background:

```bash
curl -i -X POST http://localhost:8090/upload-async -F 'file=@environment.json;type=application/json'
```

Expect `202 Accepted`, a JSON body with `handleId`, and a `Location` header pointing to `/upload-async/status/<handleId>`. Request that returned location without following redirects:

```bash
curl -i 'http://localhost:8090/<returned upload-async/status path>'
```

While the import runs, status returns `200 OK` with `executionState` `Running`. When it has finished, status returns `302 Found` with a `Location` header pointing to `/upload-async/result/<handleId>`. The result returns `200 OK` with a `BaseOperationResult`:

| Outcome | `executionState` | `success` | `messages` |
| --- | --- | --- | --- |
| Imported | `Completed` | `true` | An `Info` message confirming that the environment was stored completely |
| Failed | `Failed` | `false` | The messages that `/upload` returns for the same failure; nothing from the upload was stored |

The import uses the same all-or-nothing transaction as `/upload` and fails if it does not finish within 15 minutes. Reading the result does not delete the handle; finished results are retained for 15 minutes.

| Status | Meaning |
| --- | --- |
| `415 Unsupported Media Type` | The format was rejected before the file was accepted; no operation was created. |
| `429 Too Many Requests` | No execution capacity is available; retry later. Each running import holds one database connection, so at most one fifth of `postgres.maxOpenConnections`, and at least one, run at the same time. |
| `404 Not Found` on status or result | The handle is unknown, has expired, or belongs to another caller. |

The handle is bound to the uploader. With runtime security enabled, the `/upload-async` routes reject unauthenticated requests with `401`, only the uploader can read the status and result, and the background import is authorized with the uploader's ABAC and ReBAC permissions exactly like `/upload`. See [Asynchronous API Operations](../common/asynchronous_requests) for the shared lifecycle.

For shared payload-validation behavior, see [Validation](../common/validation).
