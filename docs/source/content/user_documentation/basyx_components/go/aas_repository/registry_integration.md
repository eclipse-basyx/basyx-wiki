# AAS Registry Integration

The standalone AAS Repository can synchronize AAS Descriptors when Repository resources change. Enable this when clients should discover Repository content through the [AAS Registry](../aas_registry/index) without maintaining every descriptor manually.

For a single runtime that exposes both Repository and Registry APIs, see the [AAS Environment](../aas_environment/index). The same integration flags remain explicit there; co-locating the APIs does not by itself enable descriptor synchronization.

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
  externalUrl: "http://localhost:8080"
```

For the [Compose setup](setup), append these entries to the AAS Repository's existing environment list, retaining its server and PostgreSQL settings:

```yaml
      - GENERAL_AASREGISTRYINTEGRATION=true
      - GENERAL_EXTERNALURL=http://localhost:8080
```

The default is disabled. Standalone AAS Repository startup rejects `general.submodelRegistryIntegration=true`; that flag belongs to the standalone Submodel Repository or the composed AAS Environment configuration.

Registry synchronization derives both AAS endpoints (`<externalUrl>/shells/{encodedAasId}`) and Submodel endpoints (`<externalUrl>/submodels/{encodedSubmodelId}`) from the same `externalUrl`. Configure an externally reachable URL whose routing serves both path families. The example value `http://localhost:8080` assumes a gateway that routes `/shells/...` to the AAS Repository and `/submodels/...` to a Submodel Repository using the same database.

The standalone AAS Repository on port `8084` serves Submodels only below `/shells/{aasIdentifier}/submodels/{submodelIdentifier}`. It does not serve the generated root `/submodels/{submodelIdentifier}` URL. Do not advertise the standalone service directly when clients must follow embedded Submodel Descriptor endpoints. The [combined proxy example](../common/registry_integration.md#combined-compose-example) provides a working local topology; see also [Advertise a Reachable Repository URL](../common/registry_integration.md#advertise-a-reachable-repository-url).

## Generated Descriptors and Lifecycle

| Repository change | Registry effect |
| --- | --- |
| Create an AAS | Create its AAS Descriptor from AAS and asset information. Embedded Submodel Descriptors are derived from references and contain the Submodel ID and generated endpoint. |
| Replace an AAS | Regenerate the AAS Descriptor when descriptor-relevant data has changed. Embedded Submodel Descriptors generated during this full-resource synchronization are reference-derived. |
| Replace Asset Information | Update the corresponding asset-related fields of the AAS Descriptor. |
| Add a Submodel reference | Add or update the corresponding embedded Submodel Descriptor. If the referenced Submodel exists, descriptor metadata is derived from it; otherwise a minimal descriptor containing the Submodel ID and endpoint is generated. |
| Remove a Submodel reference | Remove the corresponding AAS-scoped Submodel Descriptor. |
| Create or replace a Submodel through the AAS-scoped API | Create or update its AAS-scoped Submodel Descriptor and ensure that the AAS contains the corresponding Submodel reference. |
| Patch a Submodel or its metadata through the AAS-scoped API | Regenerate and update its AAS-scoped Submodel Descriptor from the resulting Submodel. |
| Delete a Submodel through the AAS-scoped API | Delete the Submodel and its reference from the AAS and remove the corresponding AAS-scoped Submodel Descriptor. |
| Delete an AAS | Remove its AAS Descriptor and all AAS-scoped Submodel Descriptors embedded in that descriptor. Standalone Submodel Registry entries are unaffected. |

Descriptors derive identifiers, names, descriptive metadata, administrative information, and asset identifiers from the Repository resource. Full AAS creation or replacement sees only the AAS's Submodel references, so its embedded Submodel Descriptors can contain only the referenced Submodel ID and generated endpoint. A direct stored-Submodel operation, such as an AAS-scoped Submodel PUT or PATCH, can populate the embedded descriptor from the actual Submodel metadata. Embedded descriptors do not create standalone Submodel Registry entries under the AAS integration flag.

```{note}
A full AAS replacement that causes descriptor regeneration can replace previously enriched embedded Submodel Descriptors with the minimal reference-derived form. Do not rely on enriched embedded metadata surviving a later complete AAS replacement.
```

Endpoint addresses are constructed by appending `/shells/{encodedAasId}` or `/submodels/{encodedSubmodelId}` to each external base URL. For the example AAS this gives `http://localhost:8080/shells/dXJuOmV4YW1wbGU6YWFzOjE`.

### Shared Submodel Synchronization Scope

Synchronization of AAS-scoped Submodel changes is performed for the AAS named in the request. If AAS A and AAS B both reference shared Submodel X, updating X through AAS A changes the shared content and updates AAS A's embedded descriptor. AAS B's descriptor is not automatically reconciled. Deleting X through AAS A removes the shared content and AAS A's reference and embedded descriptor, while AAS B and its Registry descriptor can retain stale references.

Enabling `general.aasRegistryIntegration` does not backfill AASs that already exist. Synchronization is mutation-driven; explicitly register or reconcile pre-existing resources. See [Existing Resources and Manual Changes](../common/registry_integration.md#existing-resources-and-manual-changes).

## Check the Integration

1. Use the [combined proxy example](../common/registry_integration.md#combined-compose-example), or provide equivalent routing for `/shells/...` and `/submodels/...`. Configure the AAS Registry and both Repositories against the same database. Direct service ports can remain `8084` for the AAS Repository, `8085` for the Submodel Repository, and `8082` for the AAS Registry.
2. Create a new AAS using the [usage example](usage.md#create-an-aas).
3. Read its descriptor from the Registry:

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Expect `200 OK` with the generated descriptor. Check `endpoints[].protocolInformation.href` from the client's network location. After adding a Submodel through the [AAS-scoped usage example](usage.md#aas-scoped-submodel-access), retrieve the AAS Descriptor again and follow each `submodelDescriptors[].endpoints[].protocolInformation.href`. With the required gateway or combined topology, the generated AAS and Submodel URLs return `200 OK` with their content. A direct standalone AAS Repository URL cannot satisfy the generated root `/submodels/...` endpoint.

Then delete the example content and confirm the descriptor is absent.

See [General Configuration](../common/configuration.md#general) and [AAS Registry Usage](../aas_registry/usage) for configuration keys and descriptor requests.
