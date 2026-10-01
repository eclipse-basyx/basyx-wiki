# Runtime Security

This page describes runtime API access security in BaSyx Go v1.1.0. OpenID
Connect (OIDC) authenticates presented bearer access tokens. Attribute-based
access control (ABAC) decides which API operations and resources a caller may
use. This is separate from [Supply Chain Security](../supply_chain_security),
which covers container images, signatures, provenance, and SBOMs.

## What Runtime Security Does

`abac.enabled` is the switch for the shared security stack. When it is `true`,
the service initializes OIDC from the configured trustlist and applies OIDC
before ABAC on its API routes. OIDC validates a presented token and normalizes
its claims. ABAC evaluates the request method, route, required right, claims,
target objects, and policy formula.

When `abac.enabled` is `false` (the default), the service does not read the
trustlist or install the shared OIDC and ABAC middleware. The API routes then
have no protection from this stack. Use a trusted network boundary or external
gateway if access control is still required.

## Supported Components and Default Posture

The v1.1.0 entry points install the shared OIDC and ABAC stack for:

- AAS Environment
- AAS Repository and Submodel Repository
- Concept Description Repository
- AAS Registry and Submodel Registry
- Basic Discovery
- AASX File Server
- Digital Twin Registry
- DPP API

The Company Lookup service does not install this stack in v1.1.0. Sharing the
common configuration structure does not by itself make a service secured.

In the standard entry points, health and Swagger/OpenAPI endpoints are
registered outside the protected API router. Do not rely on an ABAC rule to
restrict those endpoints.

## Enabling Runtime Security

A typical file-based startup configuration is:

```yaml
oidc:
  trustlistPath: /security/trustlist.json

abac:
  enabled: true
  modelPath: /security/access-rules.json
  policyFileImport: if_missing
```

The equivalent enable switch is `ABAC_ENABLED=true`. The trustlist must be
readable. Database-backed policy services must read `modelPath` when startup
import is required. The DPP API reads it directly. See
[General Configuration](configuration.md#oidc-and-abac) for all keys, defaults,
environment-variable names, startup import modes, and file-mount guidance.

For the database-backed policy services, authorization uses the active ABAC
policy stored in PostgreSQL. `abac.policyFileImport` controls whether
`abac.modelPath` is imported and activated at startup. Policy administration
is intentionally outside the scope of this page.

## OIDC Authentication

Send an access token as:

```text
Authorization: Bearer <token>
```

BaSyx accepts compact signed JWT bearer tokens. It does not support opaque
tokens or token introspection. Provider-specific token-type indicators are
ordinary claims. Map and require them in the ABAC policy if they must be
enforced. The token's `iss` value must identify a configured trustlist entry.
For that issuer, BaSyx obtains OpenID Provider metadata and keys, then verifies
the signature, issuer, expiration, and the configured audience. An invalid
bearer token is rejected before ABAC.

Audience validation is optional. If a trustlist entry has an empty or omitted
`audience`, BaSyx skips the audience check and logs a startup warning for that
issuer. Configure an audience when the identity provider supplies one for the
BaSyx API.

Each configured value in `scopes` is required. By default, scopes are collected
from `/scope` and `/scp`. A value may be a whitespace-separated string or a
string array. Missing required scopes produce `403 Forbidden` before ABAC.

### Trustlist Format

The trustlist is a JSON array with one entry per accepted issuer. This example
is based on the released Ory Hydra example and maps a provider-specific role
into a canonical BaSyx claim:

```json
[
  {
    "issuer": "https://idp.example.com",
    "audience": "basyx-api",
    "scopes": ["openid"],
    "claimMappings": [
      {
        "target": "role",
        "mode": "scalar",
        "sources": ["/ext/role"]
      }
    ]
  }
]
```

| Field | Behavior |
| --- | --- |
| `issuer` | Required. Duplicate or empty issuers make startup fail. |
| `audience` | Optional. An empty value disables audience validation for this issuer. |
| `scopes` | Optional list of scopes that must all be present. |
| `discoveryUrl` | Optional non-standard discovery-document URL. If omitted, standard discovery is used. A custom document must report the configured issuer and a JWKS URL. |
| `scopeClaims` | Optional JSON pointers to scope claims. The default is `/scope` and `/scp`. |
| `claimMappings` | Optional mappings from provider claims to canonical `basyx.<target>` claims. |

Mapping `target: role` creates `basyx.role`. The access policy can use that
claim while the provider's original claims remain available. `list` mode
collects and deduplicates strings from all present sources. `scalar` mode uses
the first present source and accepts a primitive value or a single-item
primitive array. Invalid mapped value shapes reject the token.

Each mapping needs a target, a `list` or `scalar` mode, and at least one source.
The `sources` values are JSON pointers. Targets must be unique, must not use the
reserved `basyx.` prefix, and must not be `scopes`. BaSyx also adds the
normalized `basyx.scopes` claim. A token that already contains any `basyx.*`
claim is rejected so that the identity provider cannot bypass canonical
mapping.

### Anonymous Requests

The OIDC layer allows a request with no bearer token to continue with an empty,
unauthenticated claim set. A missing token therefore does **not** automatically
produce `401 Unauthorized`. ABAC still evaluates the request and denies it
unless the active policy contains a rule that allows the operation without
token claims.

To make an operation public, an ACL can declare the subject attribute:

```json
{ "GLOBAL": "ANONYMOUS" }
```

Its rights, objects, and formula must also match. `ANONYMOUS` marks a public
rule and also matches authenticated callers. If the ACL additionally declares
a `CLAIM` or `CLAIMPATH`, that claim must still be present. A malformed, empty,
untrusted, or otherwise invalid `Bearer` token is rejected with `401` rather
than treated as anonymous.

## ABAC Authorization

BaSyx access-rules files use one top-level `AllAccessPermissionRules` object.
It contains reusable definitions and the rules that combine them:

| Element | Purpose |
| --- | --- |
| `DEFATTRIBUTES` | Names reusable subject attributes such as required token claims or the `ANONYMOUS` global. |
| `DEFOBJECTS` | Names reusable route, identifiable-resource, descriptor, or referable targets. |
| `DEFACLS` | Names reusable ACLs that combine subject attributes, rights, and `ALLOW` or `DISABLED`. |
| `DEFFORMULAS` | Names reusable logical conditions over claims, time globals, constants, and resource fields. |
| `rules` | Combines an ACL, objects, a formula, and optional fragment filters, either inline or through the definitions above. |

Rules grant access. A disabled rule is skipped, and no matching allow rule
means denial. When several rules match, their grants are alternatives.

### Rights and Request Matching

BaSyx maps each registered HTTP method and route to a required right:

| Right | Typical use |
| --- | --- |
| `CREATE` | Create a resource or child resource. |
| `READ` | Retrieve, list, query, or read service information. |
| `UPDATE` | Replace or modify an existing resource. |
| `DELETE` | Delete a resource. |
| `EXECUTE` | Invoke Operations and use their status/results, or call `/verify`. |
| `ALL` | ACL wildcard that satisfies any mapped right. |

The policy grammar also accepts `VIEW`, but no shared v1.1.0 runtime route is
mapped to that right. Do not use it as a substitute for `READ`.

When a route is mapped to more than one right, those rights are alternatives,
not cumulative requirements. Effect-specific checks for create-or-replace
operations are endpoint-specific. See the relevant component page.

A rule is eligible only when its right, declared subject attributes, target
objects, and formula match. Route objects match the API path. Resource objects
and formulas can further restrict identifiable resources, descriptors,
referables, or their fields.

### Attribute Evaluation

Every declared `CLAIM` or `CLAIMPATH` attribute must exist. A missing claim or
claim path makes that rule ineligible. Formula values with an unsupported type
or a condition that cannot be evaluated fail closed for that rule.

Formulas can use server-provided `UTCNOW` and `LOCALNOW` globals. `CLIENTNOW`
is taken from the validated token claim of that name when present. Time globals
can participate in formulas, but they do not by themselves identify an
eligible subject. The ACL also needs a claim attribute or `ANONYMOUS`.

### Authorization Outcomes and Resource Filtering

ABAC evaluation has three user-visible outcomes:

- no allow rule matches, so the request is denied;
- an allow rule matches without residual resource conditions, so access is
  unrestricted for that operation;
- an allow rule matches but leaves resource or fragment conditions that the
  participating API and persistence layer enforce as a query filter.

The third outcome lets a collection request return only authorized resources
and can hide restricted fragments of otherwise visible resources. Caller
filters are combined with the authorization conditions using logical `AND`.
A client-supplied query cannot broaden the ABAC result.

### Minimal Access Policy

On a component that exposes `/description`, this policy uses the `basyx.role`
produced by the trustlist example and permits callers with role `viewer` to
read the service description:

```json
{
  "AllAccessPermissionRules": {
    "DEFATTRIBUTES": [
      {
        "name": "role_attr",
        "attributes": [{ "CLAIM": "basyx.role" }]
      }
    ],
    "DEFOBJECTS": [
      {
        "name": "description_api",
        "objects": [{ "ROUTE": "/description" }]
      }
    ],
    "DEFACLS": [
      {
        "name": "viewer_read",
        "acl": {
          "USEATTRIBUTES": "role_attr",
          "RIGHTS": ["READ"],
          "ACCESS": "ALLOW"
        }
      }
    ],
    "DEFFORMULAS": [
      {
        "name": "is_viewer",
        "formula": {
          "$eq": [
            { "$attribute": { "CLAIM": "basyx.role" } },
            { "$strVal": "viewer" }
          ]
        }
      }
    ],
    "rules": [
      {
        "USEACL": "viewer_read",
        "USEOBJECTS": ["description_api"],
        "USEFORMULA": "is_viewer"
      }
    ]
  }
}
```

This policy does not grant access to any other route or right.

## Component-Specific Behavior

The Digital Twin Registry and standalone Submodel Repository can optionally
copy the caller-supplied `Edc-Bpn` header into the claims evaluated by ABAC when
`general.enableCustomMiddlewareHeaderInjection` is enabled. The header is not
authenticated by BaSyx and, when present, replaces a token claim with the same
name. Keep this option behind a trusted intermediary that strips or overwrites
client input. See the Digital Twin Registry's
[Security and Visibility Semantics](../digital_twin_registry/index.md#security-and-visibility-semantics)
for the DTR-specific behavior.

Registry, Repository, Discovery, and aggregate-service APIs also have
resource-specific authorization and filtering semantics. Their component pages
remain the source for those differences.

## Relationship to ReBAC

Experimental ReBAC is an optional authorization extension. It does not replace
OIDC or ABAC and requires `abac.enabled=true` plus a readable trustlist. For an
authenticated caller on a ReBAC-covered route, ABAC and ReBAC grants form a
strict union: either can grant access. Anonymous requests and routes outside
ReBAC coverage remain ABAC-only. See
[Relationship-Based Access Control](rebac) for supported components, roles,
sharing, inheritance, and administration.

## See Also

- [General Configuration](configuration.md#oidc-and-abac) for all OIDC, ABAC,
  and security-file settings
- [Shared Runtime Features](shared_features) for the wider shared runtime
  feature set
- [Supply Chain Security](../supply_chain_security) for image integrity,
  provenance, and SBOMs
