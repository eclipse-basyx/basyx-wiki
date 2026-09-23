# Submodel Registry Integration

The standalone Submodel Repository can generate and maintain descriptors in the [Submodel Registry](../submodel_registry/index) when Repository content changes. This connects content management to discovery without requiring a separate descriptor write for each supported mutation.

The [AAS Environment](../aas_environment/index) provides a combined deployment route with the same Submodel APIs. In either executable, Repository-to-Registry synchronization must be enabled explicitly; sharing a process or database is not enough by itself and does not turn this into HTTP synchronization between services.

## Shared Behavior

See [Repository-to-Registry Integration](../common/registry_integration) for database prerequisites, transaction behavior, public URL configuration, and handling existing data.

The standalone Submodel Repository also refreshes embedded Submodel Descriptors in existing AAS Descriptors that reference the Submodel. Missing AAS Descriptors are skipped.

## Configuration

For a native configuration file:

```yaml
server:
  port: 8085
general:
  submodelRegistryIntegration: true
  aasRegistryIntegration: false
  externalUrl: "http://localhost:8085"
```

For the [Compose setup](setup), append these entries to the Submodel Repository's existing environment list, retaining the server and PostgreSQL settings:

```yaml
      - GENERAL_SUBMODELREGISTRYINTEGRATION=true
      - GENERAL_EXTERNALURL=http://localhost:8085
```

The default is disabled. The standalone Submodel Repository rejects `general.aasRegistryIntegration=true` at startup. Its embedded descriptor synchronization is already enabled by `submodelRegistryIntegration`; enabling the AAS flag is not required for that behavior.

Set `externalUrl` to the client-facing Repository base URL, following [Advertise a Reachable Repository URL](../common/registry_integration.md#advertise-a-reachable-repository-url).

## Generated Descriptors and Lifecycle

| Repository change | Registry effect |
| --- | --- |
| Create a Submodel | Create its standalone Submodel Descriptor and update applicable embedded descriptors. |
| Replace a Submodel | Refresh descriptors when descriptor-relevant content changes. |
| Patch Submodel metadata | Update descriptor metadata through the supported Submodel patch routes. |
| Change an element value | No descriptor payload change is normally needed: element values are not included in descriptors. |
| Delete a Submodel | Remove the standalone descriptor and applicable embedded registrations. |

The generated descriptor includes the Submodel identifier, short name, semantic references, administrative information, and descriptive metadata. It does not contain `submodelElements` or their values.

## Check the Integration

1. Enable integration and restart the Repository. Configure a Submodel Registry for the same database and a different HTTP port, for example `8083`.
2. Create a new Submodel using the [usage example](usage.md#create-a-submodel).
3. Retrieve its descriptor:

```bash
curl -i http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `200 OK`. Check the advertised endpoint, change the Submodel short name through the Repository, and retrieve the descriptor again to verify the update. After deleting the Submodel, its standalone descriptor should return `404`. Use `curl.exe` in PowerShell and adjust the Registry URL for its configured port/context path.

For embedded descriptors, also create an AAS reference and an AAS Descriptor in the same database, then verify the corresponding entry through the [AAS Registry API](../aas_registry/usage). Keep each generated endpoint reachable from the clients that use it.

See [General Configuration](../common/configuration.md#general) and [Submodel Registry Usage](../submodel_registry/usage) for further configuration and descriptor requests.

The lifecycle behavior described here is release-scoped to 1.0.11; see the pinned [standalone service wiring](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/submodelrepositoryservice/main.go) and [shared registry-synchronization implementation](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/aasenvironment).
