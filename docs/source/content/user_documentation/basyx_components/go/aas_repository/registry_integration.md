# AAS Registry Integration

The standalone AAS Repository can synchronize AAS Descriptors when Repository resources change. Enable this when clients should discover Repository content through the [AAS Registry](../aas_registry/index) without maintaining every descriptor manually.

## Shared Behavior

See [Repository-to-Registry Integration](../common/registry_integration) for database prerequisites, transaction behavior, public URL configuration, and handling existing data.

## Configuration

For a native configuration file:

```yaml
server:
  port: 8084
general:
  aasRegistryIntegration: true
  submodelRegistryIntegration: false
  externalUrl: "http://localhost:8084"
```

For the [Compose setup](setup), append these entries to the AAS Repository's existing environment list, retaining its server and PostgreSQL settings:

```yaml
      - GENERAL_AASREGISTRYINTEGRATION=true
      - GENERAL_EXTERNALURL=http://localhost:8084
```

The default is disabled. Standalone AAS Repository startup rejects `general.submodelRegistryIntegration=true`; that flag belongs to the standalone Submodel Repository or the composed AAS Environment configuration.

Set `externalUrl` to the client-facing Repository base URL, following [Advertise a Reachable Repository URL](../common/registry_integration.md#advertise-a-reachable-repository-url).

## Generated Descriptors and Lifecycle

| Repository change | Registry effect |
| --- | --- |
| Create an AAS | Create its AAS Descriptor from AAS and asset information. |
| Replace an AAS | Regenerate the AAS Descriptor and update it when descriptor-relevant data has changed. |
| Replace Asset Information | Update the corresponding asset-related fields of the AAS Descriptor. |
| Add a Submodel reference | Add or update the corresponding AAS-scoped Submodel Descriptor. If the referenced Submodel exists, descriptor metadata is derived from it; otherwise a minimal descriptor containing the Submodel ID and endpoint is generated. |
| Remove a Submodel reference | Remove the corresponding AAS-scoped Submodel Descriptor. |
| Create or replace a Submodel through the AAS-scoped API | Create or update its AAS-scoped Submodel Descriptor and ensure that the AAS contains the corresponding Submodel reference. |
| Patch a Submodel or its metadata through the AAS-scoped API | Regenerate and update its AAS-scoped Submodel Descriptor from the resulting Submodel. |
| Delete a Submodel through the AAS-scoped API | Delete the Submodel and its reference from the AAS and remove the corresponding AAS-scoped Submodel Descriptor. |
| Delete an AAS | Remove its AAS Descriptor and all AAS-scoped Submodel Descriptors embedded in that descriptor. Standalone Submodel Registry entries are unaffected. |

Descriptors derive identifiers, names, descriptive metadata, administrative information, and asset identifiers from the Repository resource. Submodel references can produce embedded Submodel Descriptors; they do not create standalone Submodel Registry entries under this flag.

Endpoint addresses are constructed by appending `/shells/{encodedAasId}` or `/submodels/{encodedSubmodelId}` to each external base URL. For the example AAS this gives `http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE`. Generated interface labels are `AAS-3.0` and `SUBMODEL-3.0` in the `1.0.11` Docker images, and `AAS-3.2` and `SUBMODEL-3.2` in the pinned native source revision. See [Version Scope](../common/registry_integration.md#version-scope).

The standalone AAS Repository serves Submodels only below `/shells/{aasIdentifier}/submodels/{submodelIdentifier}`. It does not expose the generated root `/submodels/{submodelIdentifier}` URL. With embedded Submodel Descriptors, the advertised base URL must therefore route `/shells` to the AAS Repository and `/submodels` to a Submodel Repository sharing the database. The [combined Compose example](../common/registry_integration.md#combined-compose-example) provides this routing. Alternatively, use the composed AAS Environment, which exposes both paths.

The direct `http://localhost:8084` configuration above is sufficient for AAS endpoints only. For the combined example, both Repositories advertise the proxy at `http://localhost:8080`.

For existing resources and manually edited descriptors, follow [Existing Resources and Manual Changes](../common/registry_integration.md#existing-resources-and-manual-changes).

## Check the Integration

1. Enable integration, restart the Repository, and configure an AAS Registry against the same database. Use separate HTTP ports, for example Repository `8084` and Registry `8082`.
2. Create a new AAS using the [usage example](usage.md#create-an-aas).
3. Read its descriptor from the Registry:

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK` with the generated descriptor. Check `endpoints[].protocolInformation.href` from the client's network location. After adding a Submodel through the [AAS-scoped usage example](usage.md#aas-scoped-submodel-access), retrieve the AAS Descriptor again and follow each `submodelDescriptors[].endpoints[].protocolInformation.href`. Expect `200 OK` with the Submodel content, not merely a successful descriptor lookup. Then delete the example content and confirm the descriptor is absent.

See [General Configuration](../common/configuration.md#general) and [AAS Registry Usage](../aas_registry/usage) for configuration keys and descriptor requests.
