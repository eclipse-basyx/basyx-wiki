# Runtime Security

This page describes runtime API access security in BaSyx Go v1.1.0. BaSyx
validates signed JWT bearer access tokens against configured OpenID Connect
(OIDC) providers, checks required scopes, and normalizes the resulting claims.
Attribute-based access control (ABAC) then decides which API operations and
resources the caller may use. Requests without credentials can continue as
anonymous; ABAC still decides whether they are allowed. This is separate from
[Supply Chain Security](../supply_chain_security), which covers container
images, signatures, provenance, and SBOMs.

## What Runtime Security Does

`abac.enabled` is the switch for the shared security stack. When it is `true`,
the service reads the configured trustlist and installs OIDC before ABAC on its
API routes. ABAC evaluates the request method, route, required right, claims,
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
```

The equivalent enable switch is `ABAC_ENABLED=true`. The trustlist must be
readable, and `modelPath` must be readable when the component loads or imports
the file. See
[General Configuration](configuration.md#oidc-and-abac) for all keys, defaults,
environment-variable names, startup import modes, and file-mount guidance.

For components with PostgreSQL-backed ABAC policy storage, authorization uses
the active database policy. `abac.policyFileImport` controls whether
`abac.modelPath` is imported and activated at startup. When the setting is
omitted, the default is `if_missing` for these components except the Digital
Twin Registry, whose default is `always`. The DPP API instead loads the file
directly and does not use this database-backed import lifecycle. See
[ABAC Policy Management](abac_policy_management) for policy scopes, versioning,
staged changes, activation, and multi-replica operation.

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
the signature, issuer, expiration, and the configured audience. A malformed or
unverifiable token sent using the header above is rejected before ABAC.

Audience validation is optional. If a trustlist entry has an empty or omitted
`audience`, BaSyx skips the audience check and logs a startup warning for that
issuer. Configure an audience when the identity provider supplies one for the
BaSyx API.

The trustlist entry's `scopes` list names the scopes that the token must grant.
Every configured scope is required. BaSyx reads granted scopes from the JSON
claim paths in `scopeClaims`, which default to `/scope` and `/scp`. At those
paths, a JWT claim may be a whitespace-separated string or a string array.
BaSyx splits and deduplicates these values before checking the required scopes.
A missing required scope produces `403 Forbidden` before ABAC authorization.

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
a `CLAIM` or `CLAIMPATH`, that claim must still be present. A malformed or
otherwise invalid token sent using the documented header is rejected with
`401` rather than treated as anonymous.

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

## Common Authorization Responses

| Situation | Response |
| --- | --- |
| A token sent as `Authorization: Bearer <token>` is malformed, has an untrusted issuer, or fails signature, issuer, expiration, or configured audience validation | `401 Unauthorized` |
| An authenticated token does not contain every scope required by its trustlist entry | `403 Forbidden` |
| ABAC denies an otherwise valid request on an ABAC-only route outside `/security/abac`, whether authenticated or anonymous | `403 Forbidden` |
| After OIDC processing, ABAC denies access below `/security/abac`; policy-management resources are deliberately hidden | `404 Not Found` |
| An authenticated request on a covered route needs a ReBAC decision, but that decision cannot be obtained | `503 Service Unavailable` |

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
authenticated caller on a covered route, BaSyx consults ReBAC for relevant
rights that ABAC has not granted unconditionally. A matching ReBAC grant can
therefore widen access beyond ABAC alone. For the resource covered by the
grant, ABAC policy fragment filters and update conditions do not restrict that
grant; caller-supplied query and fragment filters still apply.

If a required ReBAC decision cannot be obtained, the request fails closed with
`503 Service Unavailable` instead of falling back to ABAC-only behavior.
Anonymous requests and routes or services outside ReBAC coverage remain
ABAC-only. The Digital Twin Registry does not enable ReBAC in v1.1.0. See
[Relationship-Based Access Control](rebac) for supported components, roles,
sharing, inheritance, and administration.

## See Also

- [General Configuration](configuration.md#oidc-and-abac) for all OIDC, ABAC,
  and security-file settings
- [Shared Runtime Features](shared_features) for the wider shared runtime
  feature set
- [Supply Chain Security](../supply_chain_security) for image integrity,
  provenance, and SBOMs
