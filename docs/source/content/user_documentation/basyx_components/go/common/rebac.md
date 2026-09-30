# Relationship-Based Access Control (ReBAC)

```{note}
ReBAC is experimental. Its management API and database tables may change incompatibly in future releases.
```

ReBAC lets people share their own Asset Administration Shells, Submodels, SubmodelElements, Concept Descriptions, registry descriptors, discovery entries, AASX packages, and Digital Product Passports with other users or groups, without editing the ABAC policy. Whoever creates a resource becomes its owner, and owners decide who else may use it.

ReBAC runs next to ABAC as a strict union:

```text
access = ABAC allows  OR  ReBAC allows
```

ABAC syntax, evaluation, and policy management are unchanged. With `rebac.enabled=false` (the default), no ReBAC code is wired and every service behaves exactly as before. Relationships are stored in the BaSyx PostgreSQL database and evaluated there as part of each query. No external authorization service is needed.

## Roles

| Role | Allows |
| --- | --- |
| `viewer` | Read. |
| `editor` | Read, update, and create children. |
| `executor` | Invoke operations and read their status and results (shells, Submodels, and SubmodelElements only). |
| `owner` | Everything above, plus delete and manage access. |

Two more roles apply to a whole repository family, such as all shells or all Submodels:

| Repository role | Allows |
| --- | --- |
| `creator` | Create top-level resources of the family. The creator becomes their owner. |
| `admin` | Every right on every resource of the family, and managing its repository grants. |

Roles are granted to users or groups of an OIDC issuer. There are no public or wildcard grants.

## ReBAC and ABAC interplay

A ReBAC grant on a resource is not limited by ABAC fragment filters, masks, or update conditions for that resource. When an owner shares a Submodel, the recipient sees the complete Submodel, including elements an ABAC filter would hide. Keep sensitive content in separate resources with their own owners instead of relying on ABAC filters inside a resource that will be shared.

## Covered services

| Service | Covered resources |
| --- | --- |
| AAS Repository | Shells, asset information, thumbnails, Submodel references, Submodel superpaths, `/serialization`. |
| Submodel Repository | Submodels and all representations, SubmodelElements, attachments, operations. |
| Concept Description Repository | Concept Descriptions. |
| AAS Registry, Submodel Registry | Shell descriptors, Submodel descriptors, bulk API. |
| Discovery | Discovery entries and lookups. |
| AASX File Server | AASX packages and asynchronous uploads. |
| AAS Environment | All of the above except AASX packages, plus `/upload` and `/serialization`. |
| DPP API | Current state of Digital Product Passports. |

History endpoints, event feeds, `$signed` representations, `/verify`, historical passports, the ABAC policy management API, the Company Lookup service, and the Digital Twin Registry stay ABAC-only. A ReBAC grant never gives access to them.

## Setup

1. **Prerequisites.** Every service needs `abac.enabled=true` and a readable `oidc.trustlistPath`. The identity provider must issue signed JWT access tokens with a stable user identifier. Run the Configuration Service to migrate the database before starting the updated services.
2. **Configure every service** that shares the database with the same `rebac` settings:

   ```yaml
   abac:
     enabled: true
     modelPath: /security_env/access-rules.json
   oidc:
     trustlistPath: /security_env/trustlist.json
   rebac:
     enabled: true
     subjectClaim: sub
     groupClaim: groups
     administrators:
       - "https://idp.example.com/realms/basyx|group:operators"
   ```

   With environment variables, use `REBAC_ENABLED`, `REBAC_SUBJECT_CLAIM`, `REBAC_GROUP_CLAIM`, and the comma-separated `REBAC_ADMINISTRATORS`. See [General Configuration](configuration) for all keys.
3. **Map the claims.** `rebac.subjectClaim` and `rebac.groupClaim` name top-level token claims. If the provider puts the values elsewhere, map them with `claimMappings` in the trustlist entry and use the mapped name, for example `basyx.groups`.
4. **Allow the service description.** Clients detect ReBAC through the service description, so the ABAC policy must allow `/description` for everyone. List routes and the ReBAC management API need no additional ABAC rules.
5. **Let people create resources.** Right after setup, only administrators and callers with an ABAC `CREATE` right can create resources. Grant `creator` on the repository families people should create in, preferably to groups. Use the BaSyx Web UI (**Access Management**) or the ReBAC management API.

A service that shares the database but runs without ReBAC ignores all grants and assigns no owner to resources created through it. Enable ReBAC consistently on all services.

## Identity providers

- **Keycloak:** keep `subjectClaim=sub`. Add a *Group Membership* mapper named `groups` with **Full group path** switched off, and an *Audience* mapper when the trustlist entry requires an audience.
- **Microsoft Entra ID:** set `subjectClaim` to `oid`, because `sub` differs per application. Use v2 tokens and trust only the v2 issuer. Prefer app roles over group object IDs and map `/roles` into the group claim.
- **Ory Hydra:** switch the access token strategy to JWT. Map custom claims from `ext`, for example `/ext/groups`.

## BaSyx Web UI

The BaSyx Web UI detects ReBAC automatically and offers sharing and access management. The services must accept the UI origin and the headers used for sharing:

```bash
CORS_ALLOWEDORIGINS=https://ui.example.com
CORS_ALLOWEDHEADERS=Authorization,Content-Type,If-Match
CORS_ALLOWCREDENTIALS=true
CORS_ALLOWEDMETHODS=GET,POST,PUT,PATCH,DELETE,OPTIONS
```

## Kubernetes

The [BaSyx Helm chart](https://github.com/eclipse-basyx/charts) exposes the settings as `rebac.*` values, with per-service overrides under `<service>.rebac`. The chart refuses to render when ReBAC is enabled on a service without ABAC.

## Further reading

The BaSyx Go repository contains the complete guides:

- [ReBAC overview](https://github.com/eclipse-basyx/basyx-go-components/blob/main/docu/security/rebac/README.md)
- [Administration guide](https://github.com/eclipse-basyx/basyx-go-components/blob/main/docu/security/rebac/administration.md) for operations, audit trail, monitoring, and troubleshooting
- [Sharing API](https://github.com/eclipse-basyx/basyx-go-components/blob/main/docu/security/rebac/sharing-api.md)
- [ReBAC example](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.0/examples/BaSyxReBACExample)
