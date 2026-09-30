# AAS Environment

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![API](https://img.shields.io/badge/API-AAS%203.2-yellow)

The BaSyx Go AAS Environment is a **single runtime** that provides the main APIs for storing, registering, discovering, importing, and exporting AAS data. Use it when these capabilities should run in one deployment and share one PostgreSQL database. Use the [standalone components](../index.md#component-overview) when they require independent lifecycles, scaling, or trust boundaries.

The AAS Environment service is distinct from the serialized AAS metamodel `Environment` object. The metamodel object is an import/export representation containing AASs, Submodels, and Concept Descriptions, while the AAS Environment service is the running HTTP application that persists this data and exposes the corresponding APIs. It runs these capabilities within a single process rather than starting separate Repository, Registry, or Discovery services.

## Included APIs and Data

One AAS Environment process provides:

- an [AAS Repository](../aas_repository/index) for AAS content;
- a [Submodel Repository](../submodel_repository/index) for Submodels and Submodel Elements;
- a [Concept Description Repository](../concept_description_repository/index) for Concept Description content;
- an [AAS Registry](../aas_registry/index) and [Submodel Registry](../submodel_registry/index) for endpoint descriptors;
- [Basic Discovery](../basic_discovery/index) for asset-identifier-to-AAS-identifier mappings;
- `/upload` and `/serialization` for whole-environment import and export;
- `/description` for the AAS Environment service description and supported profiles.

All of these API areas are routes of the same runtime and use shared PostgreSQL persistence. Registry descriptors remain different resources from Repository content, and Discovery mappings remain different from both. Use the linked standalone component pages for detailed CRUD and query semantics. The routes behave as composed API areas here rather than as network calls between internal services.

The Environment also supports experimental Eventing for AAS, asset, and Submodel changes, including dedicated notifications for newly added Product Change Notification (PCN) records. Eventing is disabled by default and must be enabled explicitly; see [Eventing](../common/eventing) for Event Feed and broker configuration.

`/upload` imports AAS Environment documents in JSON or XML format as well as AASX packages. For AASX input, the package is parsed into model content and supplementary files. `/serialization` creates an Environment representation from stored content. The AAS Environment does not expose the package-oriented `/packages` API. Use the standalone [AASX File Server](../aasx_file_server/index) when clients must store, list, download, replace, or delete complete AASX package files by package identifier.

```{mermaid}
flowchart LR
    CLIENT[API client]
    DB[(PostgreSQL<br/>persistent state)]
    CONFIG[Configuration Service]

    subgraph ENV[AAS Environment runtime]
        HTTP[Environment HTTP API]
        REPOS[AAS / Submodel / Concept Description<br/>Repositories]
        REGS[AAS / Submodel Registries]
        DISC[Discovery]
        IO[Upload / Serialization]
        HTTP --> REPOS
        HTTP --> REGS
        HTTP --> DISC
        HTTP --> IO
    end

    CLIENT -->|HTTP| HTTP
    HTTP -->|SQL / persistent state| DB
    CONFIG -->|initialize / migrate| DB
    CONFIG -.->|Compose startup dependency| HTTP
```

The PostgreSQL schema must be initialized or migrated by a release-compatible Configuration Service before the AAS Environment starts. In the provided Compose setup, the Configuration Service runs as a one-shot job and the Environment starts only after it exits successfully. It is not part of normal request traffic.

## Registry and Discovery Integration

Having Registry endpoints in the process does **not** by itself make Repository writes maintain descriptors. Set `GENERAL_AASREGISTRYINTEGRATION=true` and `GENERAL_SUBMODELREGISTRYINTEGRATION=true` to enable that synchronization. `GENERAL_EXTERNALURL` supplies the public base URL used in generated descriptor endpoints. The [first-use setup](setup) enables both flags explicitly.

The AAS Environment executable always enables Discovery integration internally. Consequently, AAS Descriptor writes maintain the shared Discovery asset-link data. No `GENERAL_DISCOVERYINTEGRATION` setting is needed for this executable. Repository upload reaches Discovery in the first-use walkthrough through two steps: the enabled AAS Repository-to-Registry synchronization creates or updates the descriptor, and the forced Registry-to-Discovery integration maintains its asset links.

See [Registry Integration](../common/registry_integration) for synchronization lifecycle details. In particular, do not interpret this composition as HTTP synchronization between separate internal Registry and Repository services.

## Dependencies, Persistence, and Security

The runtime requires PostgreSQL initialized or migrated by a release-compatible BaSyx Configuration Service. PostgreSQL holds Repository content, Registry descriptors, Discovery mappings, and other persistent service state independently of the AAS Environment application container. Read [Deployment, Versions, and Persistent State](../common/deployment.md#version-scope) before deploying and its [persistent-state guidance](../common/deployment.md#persistent-state) before changing volumes or removing the Compose project.

Runtime authorization is optional and disabled in the local walkthrough. Before exposing the service beyond a trusted development machine, follow [Runtime Security](../common/security).

## Get Started

1. [Set up the three-service deployment](setup).
2. [Import, retrieve, discover, and export one environment](usage).

The running service also provides Swagger UI at `http://localhost:8090/swagger` for the complete composed API contract.

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
