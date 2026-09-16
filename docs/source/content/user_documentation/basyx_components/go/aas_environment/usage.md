# Using the AAS Environment

This walkthrough imports one AAS, its linked Submodel, one Concept Description, and one specific asset identifier. It then verifies Repository, Registry, Discovery, and serialization behavior through the single AAS Environment URL.

Start the release-pinned [Compose setup](setup) and wait for `http://localhost:8090/health` to return HTTP `200`. Run the commands from one working directory. In Windows PowerShell, use `curl.exe` instead of `curl`.

## Sample Identifiers

The JSON body uses original identifiers. Identifier path parameters and the `/serialization` selection parameters use their UTF-8 Base64URL encodings without padding:

| Resource | Original identifier | Encoded value |
| --- | --- | --- |
| AAS | `urn:example:aas:environment:1` | `dXJuOmV4YW1wbGU6YWFzOmVudmlyb25tZW50OjE` |
| Submodel | `urn:example:submodel:environment:1` | `dXJuOmV4YW1wbGU6c3VibW9kZWw6ZW52aXJvbm1lbnQ6MQ` |
| Concept Description | `urn:example:concept:serial-number` | `dXJuOmV4YW1wbGU6Y29uY2VwdDpzZXJpYWwtbnVtYmVy` |

See [Identifiers and Encoding](../common/encoding.md#encode-your-own-identifier) when substituting your own identifiers.

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

The endpoint also accepts AAS Environment XML (`application/xml` or `text/xml`) and AASX packages, including `application/aasx+xml` and `application/aasx+json`. Supply the actual format as the `file` part's media type, for example `-F 'file=@environment.aasx;type=application/aasx+json'`.

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

Open `exported-environment.json` and verify the same three original identifiers. `aasIds` and `submodelIds` accept Base64URL-encoded identifiers and may be repeated to select several resources. `includeConceptDescriptions` defaults to `true`; set it to `false` to omit all Concept Descriptions. When `aasIds` is omitted, all stored AASs are selected, and when `submodelIds` is omitted, all stored Submodels are selected. An omitted selector does not mean "only objects referenced by the other selector."

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

## Re-import and Failure Behavior

Uploading the same identifiers again uses replace-on-upload behavior: existing Concept Descriptions, Submodels, and AASs are updated rather than rejected as package-level duplicates. Treat the submitted objects as complete replacements and preserve every field that should remain.

```{warning}
An upload is not one atomic package transaction. The service processes Concept Descriptions, then Submodels, then AASs; a later failure can leave earlier objects stored. AASX attachments are processed afterward and can also fail after model content was written. The success counts describe the parsed input, not an all-or-nothing commit guarantee. After any error, inspect the affected resources before retrying.
```

For shared error handling and validation behavior, see [API Errors](../common/api_errors) and [Validation](../common/validation).
