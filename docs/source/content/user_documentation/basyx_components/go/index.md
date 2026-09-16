# BaSyx Go

BaSyx Go provides Go-based BaSyx backend components and shared libraries for running registries, repositories, and related infrastructure services.

- [GitHub Repository (basyx-go-components)](https://github.com/eclipse-basyx/basyx-go-components)
- [DockerHub (Eclipse BaSyx images)](https://hub.docker.com/u/eclipsebasyx)

Repositories store the AAS model content that clients read and change. Registries store descriptors that advertise where content can be reached, while Discovery stores mappings from asset identifiers to AAS identifiers. Choose a deployment from the table below; using a Repository and Registry together does not by itself enable synchronization.

## Choose a Component

| User goal | Component | Manages or stores | Required dependencies | Optional integration | Next page |
| --- | --- | --- | --- | --- | --- |
| Use AAS, Submodel, Concept Description, Registry, Discovery, upload, and serialization APIs in one runtime | AAS Environment | AAS, Submodel, and Concept Description content; AAS and Submodel descriptors; asset-identifier mappings | PostgreSQL initialized by the matching Configuration Service | Repository-to-Registry synchronization is controlled by explicit flags; Discovery is included | [AAS Environment](aas_environment/index) |
| Store and modify AAS content | AAS Repository | AAS content and its references to Submodels | PostgreSQL initialized by the matching Configuration Service | Can maintain AAS Registry descriptors in a shared database when Registry integration is enabled | [AAS Repository](aas_repository/index) |
| Store and modify Submodel content | Submodel Repository | Submodels and Submodel Elements | PostgreSQL initialized by the matching Configuration Service | Can maintain Submodel Registry descriptors in a shared database when Registry integration is enabled | [Submodel Repository](submodel_repository/index) |
| Advertise where AAS content is available | AAS Registry | AAS Descriptors and AAS-scoped Submodel Descriptors, not Repository content | PostgreSQL initialized by the matching Configuration Service | Can expose descriptors maintained by an integrated AAS Repository; Discovery coupling is configuration-dependent | [AAS Registry](aas_registry/index) |
| Advertise independently managed Submodels | Submodel Registry | Standalone Submodel Descriptors, not Submodel content | PostgreSQL initialized by the matching Configuration Service | Can expose descriptors maintained by an integrated Submodel Repository | [Submodel Registry](submodel_registry/index) |
| Find AAS identifiers from global or specific asset identifiers | Basic Discovery | Asset-identifier-to-AAS-identifier mappings, not descriptors or Repository content | PostgreSQL initialized by the matching Configuration Service | Can share mapping data with an AAS Registry or Digital Twin Registry configured for Discovery integration | [Basic Discovery](basic_discovery/index) |
| Use the Catena-X-oriented combined AAS Registry and Discovery API | Digital Twin Registry (DTR) | AAS Descriptors and asset-identifier mappings, not AAS content | PostgreSQL initialized by the matching Configuration Service | Pair with separately deployed Repositories whose endpoints are advertised by descriptors | [Digital Twin Registry](digital_twin_registry/index) |
| Discover company-provided service endpoints | Company Lookup | Company Descriptors containing company identity and service endpoints | PostgreSQL initialized by the matching Configuration Service | Describes external services; it does not automatically connect or synchronize them | [Company Lookup](company_lookup/index) |
| Initialize or migrate the shared BaSyx database | Configuration Service | Database schema, schema version, and schema state; it is a one-shot job | PostgreSQL | Must complete successfully before database-backed BaSyx runtimes start | [Configuration Service](configuration_service/index) |

For separate Repository and Registry processes, read [Repository-to-Registry Integration](common/registry_integration) before enabling synchronization. The integration writes descriptor tables in their shared database; merely starting both HTTP services does not connect them.

## Additional Components

The following components are part of the 1.0.11 source release but do not yet have complete walkthroughs in this wiki:

- **Concept Description Repository** stores and serves Concept Description content. Inspect its release-pinned [source and configuration](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/conceptdescriptionrepositoryservice) and [OpenAPI definition](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/conceptdescriptionrepositoryservice/openapi.yaml). The [AAS Environment](aas_environment/index) provides Concept Description access together with the other AAS APIs; see its release-pinned [minimal example](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxMinimalExample).
- **AASX File Server** stores and serves AASX packages. Use the release-pinned [service source](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/aasxfileserverservice), [OpenAPI definition](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/aasxfileserverservice/openapi.yaml), and [example](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxAASXFileServerExample).
- **DPP API** creates, retrieves, searches, updates, and deletes Digital Product Passport documents and their data elements. Use the release-pinned [service source](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/dppapiservice), [OpenAPI definition](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/dppapiservice/openapi.yaml), and [example](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxDPPAPIExample).

```{note}
The pinned links above make the source and example contents reproducible. The linked Minimal, AASX File Server, and DPP API example Compose files at that revision still use mutable `SNAPSHOT` image tags. Replace the BaSyx Go component tags with `1.0.11` (or pin image digests) before treating an example as a release-pinned deployment.
```

## Shared Guidance

- [Deployment, Versions, and Persistent State](common/deployment) explains the release baseline, required startup order, native database preparation, and PostgreSQL volume lifecycle.
- [Runtime Security](common/security) explains which services enforce OIDC/ABAC and how authentication, policies, and troubleshooting fit together.
- [Common Documentation](common/index) collects configuration and shared API conventions.
- [Supply Chain Security](supply_chain_security) covers image signing, provenance, SBOMs, and release verification.

```{toctree}
:hidden:
:maxdepth: 1

common/index
aas_environment/index
basic_discovery/index
aas_registry/index
submodel_registry/index
digital_twin_registry/index
submodel_repository/index
aas_repository/index
company_lookup/index
configuration_service/index
supply_chain_security
```
