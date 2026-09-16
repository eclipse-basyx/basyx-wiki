# Runtime Security

BaSyx Go runtime security combines OIDC token validation with attribute-based
access control (ABAC). The configuration keys are shared, but runtime
enforcement exists only where an executable installs the shared middleware.
This page describes the behavior of the [1.0.11 release baseline](deployment.md#version-scope).

## Supported Components and Default Posture

| Component or executable | Shared runtime enforcement | Enablement | Component caveat |
| --- | --- | --- | --- |
| AAS, Submodel, and Concept Description Repositories; AAS and Submodel Registries; Discovery Service; AAS Environment; AASX File Server | OIDC and ABAC middleware | Set `abac.enabled: true` (or `ABAC_ENABLED=true`) and provide the trust list and policy configuration. | The active policy must cover that executable's routes and data. |
| Digital Twin Registry (DTR) | OIDC and ABAC middleware, plus optional Edc-Bpn claim injection | Set `abac.enabled: true`; configure Edc-Bpn only for the intended trusted deployment boundary. | An omitted policy import mode defaults to `always`, unlike the other participating services. See the [Edc-Bpn trust boundary](../digital_twin_registry/index.md#edc-bpn-trust-boundary). |
| Company Lookup Service | Not installed by the 1.0.11 service entry point | Not available through the shared OIDC/ABAC fields in this release. | Do not infer enforcement from fields accepted by the common configuration loader. See [Security limitations in 1.0.11](../company_lookup/index.md#security-limitations-in-1011). |
| Configuration Service | Not applicable | None; it is a one-shot database initializer, not a protected runtime HTTP API. | Protect access to the job, its configuration, and PostgreSQL at the deployment boundary. |

The participating services default to `abac.enabled: false`; in that state the
shared OIDC and ABAC middleware is not installed. Setting only
`oidc.trustlistPath` does not protect an API. Use network controls as well as
application security, and verify enforcement with real requests before
exposing a service.

## Request Evaluation

The request path has three distinct stages:

1. **Middleware activation.** A participating executable installs the OIDC and
   ABAC middleware only when ABAC is enabled. An executable that does not call
   the shared setup path, such as Company Lookup in 1.0.11, is not secured by
   merely supplying the common fields.
2. **Token validation.** A supplied Bearer token must be a valid signed JWT from
   an exactly configured issuer. The verifier checks its signature and time
   claims, the optional audience, and required scopes. An invalid token or
   unknown issuer is rejected with `401`; a verified token missing a required
   scope is rejected with `403`. Provider claim mappings then expose canonical
   `basyx.*` claims to policy evaluation.
3. **ABAC decision.** The active policy maps the HTTP method and route to a
   right, evaluates claims and object conditions, and either denies the
   request or passes an optional query filter to the handler. A route-level
   policy denial normally returns `403`. Single-resource reads can return
   `404` when the resource is missing or hidden, while successful list results
   can omit resources the caller may not read. See [API Errors](api_errors) for
   the conditional status meanings.

The shared setup deliberately accepts a request with no Bearer header as an
anonymous identity and still runs ABAC. Anonymous therefore means *policy
evaluated without authenticated claims*, not unrestricted access. A policy can
allow a public subset, return a filtered list, or deny the anonymous operation.
By contrast, sending a malformed, expired, or otherwise invalid Bearer token
does not fall back to anonymous access.

## Configure an Identity Provider and Policy

Mount a trust list at `oidc.trustlistPath` and an access-rule file at
`abac.modelPath`. This abbreviated trust-list entry matches the pinned secured
example:

```json
[
  {
    "issuer": "http://keycloak.localhost:8080/realms/basyx",
    "audience": "discovery-service",
    "scopes": ["email", "profile"]
  }
]
```

The token's `iss` value must exactly match `issuer`; using `localhost` in one
place and `keycloak.localhost` in another is a mismatch. The service process
must also be able to resolve and reach the issuer's discovery/JWKS endpoint.
In containers this can require internal DNS, an `extra_hosts` entry, or an
explicit `discoveryUrl`. A separate discovery URL changes how metadata is
reached, but does not change the issuer value accepted in tokens.

If `audience` is non-empty, arrange for the identity provider to put that value
in the access token's `aud` claim. Every configured `scopes` value must be
present in the token. Use `scopeClaims` when scopes live outside the usual
claim and `claimMappings` when provider-specific claims must be exposed in the
reserved `basyx.*` namespace. For example, the secured fixture maps the user's
`role` attribute into the token and its ABAC formulas distinguish `admin` from
`viewer`.

The trust list answers which tokens are accepted. The access-rule file answers
which rights those accepted claims, or an anonymous identity, have over routes
and objects. Keep the full key, alias, and provider-field reference in
[General Configuration](configuration.md#oidc-and-abac).

## Policy Persistence and Restart Behavior

ABAC policies are versioned and stored in PostgreSQL under an effective
`abac.policyScope`. The evaluator uses the one active policy for that scope;
the mounted file is an import source, not necessarily the live policy.

| Mode | Startup behavior | Effect of editing the mounted file | When no active policy exists |
| --- | --- | --- | --- |
| `always` | Validate, import, persist, and activate `abac.modelPath` on every start. | The edit takes effect after a successful restart/import and supersedes the preceding active version. | The imported version becomes active; an unreadable or invalid file fails startup. |
| `if_missing` | Import only when the effective scope has no active policy; otherwise load the active policy from PostgreSQL. | An edit followed by restart has no effect once an active policy exists. | The configured file is imported and activated. |
| `never` | Do not import the file; load the active policy from PostgreSQL. | No effect. Manage and activate a stored version separately. | Startup fails closed because there is no active policy. |

When the mode is omitted, DTR uses `always`; every other participating service
uses `if_missing`. This is not one universal default. In a multi-instance
deployment, coordinate import ownership for a shared policy scope so that
concurrent `always` imports cannot unexpectedly supersede one another.

The optional policy-management API is mounted below `/security/abac` only when
both `abac.enabled` and `abac.managementApi.enabled` are true. Its routes must
themselves be covered by an admin-only policy. An import can create a staged
version or, only when activation is explicitly requested, import and activate
it; cloning creates a staged version. Edits to a staged version do not affect
requests until validation and activation succeed. Active, superseded, and
rejected versions are immutable. See the pinned
[PostgreSQL-backed ABAC policy guide](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/security/ABAC_POLICY_REPOSITORY.md)
for lifecycle and management endpoints.

## Local Verification

This bounded walkthrough uses only the AAS Registry from the pinned
[BaSyxSecuredExample](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxSecuredExample).
Run it from that directory. It intentionally uses the fixture's local
password-grant users (`admin` / `pwd` and `usera` / `pwd`); those credentials
and the password grant are demo material, not a production authentication
design. The commands below are for Bash and require `curl` and `jq`.

The upstream example currently names BaSyx `SNAPSHOT` images. Save this as
`compose.release.yml` to override the two BaSyx images used by this walkthrough
and to make the tutorial policy file authoritative on every Registry start:

```yaml
services:
  aas-registry:
    image: eclipsebasyx/aasregistry-go:1.0.11
    environment:
      ABAC_POLICY_FILE_IMPORT: always
  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:1.0.11
```

`ABAC_POLICY_FILE_IMPORT=always` is deliberate for this isolated tutorial; it
is not a blanket production recommendation. Ensure
`keycloak.localhost` resolves consistently for the host and, through the
example's `extra_hosts`, for the Registry container. The issuer must remain
`http://keycloak.localhost:8080/realms/basyx`, and the Registry endpoint used
below is `http://localhost:8082`.

Start the Registry and its declared dependencies, then inspect startup logs:

```bash
docker compose -f docker-compose.yml -f compose.release.yml up -d aas-registry
docker compose -f docker-compose.yml -f compose.release.yml logs basyx_configuration aas-registry
```

Save a descriptor with an ID that is fresh in this example database as
`secured-descriptor.json`:

```json
{
  "id": "urn:example:aas:secured:1",
  "idShort": "SecuredExample",
  "assetKind": "Instance",
  "assetType": "SecurityDemo",
  "globalAssetId": "urn:example:asset:secured:1",
  "endpoints": [
    {
      "interface": "AAS-3.2",
      "protocolInformation": {
        "href": "https://example.com/shells/dXJuOmV4YW1wbGU6YWFzOnNlY3VyZWQ6MQ",
        "endpointProtocol": "https"
      }
    }
  ]
}
```

Acquire access tokens from the fixture. The trust list requires the
`discovery-service` audience and `email` and `profile` scopes; the fixture's
`basyx-ui` client is configured to issue them and to map each user's `role`
claim:

```bash
TOKEN_URL='http://keycloak.localhost:8080/realms/basyx/protocol/openid-connect/token'
ADMIN_TOKEN=$(curl -sS -X POST "$TOKEN_URL" -d client_id=basyx-ui -d grant_type=password -d username=admin -d password=pwd -d 'scope=openid email profile' | jq -r .access_token)
VIEWER_TOKEN=$(curl -sS -X POST "$TOKEN_URL" -d client_id=basyx-ui -d grant_type=password -d username=usera -d password=pwd -d 'scope=openid email profile' | jq -r .access_token)
```

Prove an authorized write and read. Expect `201 Created`, then `200 OK`:

```bash
curl -i -X POST http://localhost:8082/shell-descriptors -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' --data-binary '@secured-descriptor.json'
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOnNlY3VyZWQ6MQ -H "Authorization: Bearer $ADMIN_TOKEN"
```

The fixture gives the viewer read-only access. Repeating the create as the
viewer is denied with `403 Forbidden`; the request never becomes an anonymous
request merely because it lacks an admin role:

```bash
curl -i -X POST http://localhost:8082/shell-descriptors -H "Authorization: Bearer $VIEWER_TOKEN" -H 'Content-Type: application/json' --data-binary '@secured-descriptor.json'
```

A deliberately invalid supplied token is rejected with `401 Unauthorized`:

```bash
curl -i http://localhost:8082/shell-descriptors -H 'Authorization: Bearer deliberately.invalid.token'
```

Finally, omit the header. This fixture's anonymous rule permits only selected
public descriptor/data objects. A list can therefore return `200 OK` with a
policy-filtered result, but it must not expose the freshly created descriptor:

```bash
curl -i http://localhost:8082/shell-descriptors
```

Use the authorized admin token for cleanup; expect `204 No Content`:

```bash
curl -i -X DELETE http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOnNlY3VyZWQ6MQ -H "Authorization: Bearer $ADMIN_TOKEN"
```

If the example ID already exists, choose another ID and Base64URL-encode it for
the read/delete path as described in [Identifiers and Encoding](encoding).

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Service starts without enforcing OIDC/ABAC | Confirm the executable is in the capability matrix and its effective `abac.enabled` is `true`. OIDC fields alone do not activate the middleware. |
| Startup cannot initialize the OIDC provider | Resolve the issuer host from inside the service container and test its discovery endpoint. Check that the configured issuer exactly matches the provider metadata and token `iss`. |
| Valid-looking token returns `401` | Check signature/key rotation, expiry/not-before, exact issuer, and configured audience. A bad supplied token does not fall back to anonymous. |
| Token returns `403` before the handler | Check required scopes, the role/claim source, claim mappings, and whether the active policy grants the method/route/right. |
| Policy-file edit has no effect after restart | Inspect the effective policy scope, import mode, and active PostgreSQL policy. `if_missing` deliberately keeps an existing active policy. |
| Anonymous request is denied or sees only some rows | Inspect the active policy's anonymous rules and query filters. Anonymous access is policy-specific. |
| A list is successful but omits expected resources | The ABAC formula can filter list/query results. Compare with an authorized identity and inspect the active policy before treating the rows as absent. |
| Management routes are missing or return `404` | Both ABAC and the management API must be enabled; the active policy must explicitly authorize those routes. Unauthorized callers can receive `404` to avoid exposing policy identifiers. |

## Component-Specific Boundaries

- [Company Lookup security limitations in 1.0.11](../company_lookup/index.md#security-limitations-in-1011): shared configuration availability does not mean its entry point installs the middleware.
- [DTR Edc-Bpn trust boundary](../digital_twin_registry/index.md#edc-bpn-trust-boundary): header-derived identity requires a deployment boundary that strips untrusted input and injects only verified claims.

The upstream pinned [security architecture](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/security/README.md)
and [Registry security semantics](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/docu/security/REGISTRY_SECURITY.md)
provide implementation-level detail for the 1.0.11 baseline.
