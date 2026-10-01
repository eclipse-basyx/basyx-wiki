# ABAC Policy Management

BaSyx Go v1.1.0 can store ABAC policies as versioned PostgreSQL records. An
operator can prepare, inspect, and validate a staged policy before it replaces
the policy currently used for authorization. See [Runtime Security](security)
for OIDC and ABAC request-processing semantics.

## How Policy Versions Work

Each policy version stores the configured access-rule document and a
materialized form in which reusable definitions have been resolved. Its ordered
materialized rule rows are what the runtime evaluator uses. Only the `active`
version for the effective policy scope affects authorization. Editing a staged
version has no effect until activation succeeds.

| Status | Behavior |
| --- | --- |
| `staged` | Can be edited, validated, activated, rejected, or cloned. |
| `active` | Supplies the live rules for its policy scope. Normal API edits and reactivation are rejected. |
| `superseded` | A previously active, read-only version. It can be inspected or cloned. |
| `rejected` | A retained, read-only version that cannot be activated. It can be inspected or cloned into a new staged version. |

The API permits edits only while it observes `staged`. It does not provide an
ETag or policy-revision precondition, so do not edit, reject, or activate the
same draft concurrently from multiple administration clients.

## Configuration

The following enables runtime security, startup import, and the optional policy
management API:

```yaml
abac:
  enabled: true
  modelPath: /security/access-rules.json
  policyFileImport: if_missing
  policyScope: aasrepositoryservice
  managementApi:
    enabled: true
```

The service also needs a readable OIDC trustlist. See
[General Configuration](configuration.md#oidc-and-abac) for all properties,
defaults, environment-variable aliases, and file-mount guidance.

### Policy Scope

`abac.policyScope` selects the `service_scope` under which policy versions,
rules, events, and activation evidence are stored. If it is empty, the service
uses its built-in service name, such as `aasrepositoryservice`. PostgreSQL
enforces at most one `active` version per scope.

Use distinct scopes for deployments that share a database but require
independent policies. Sharing a scope makes those deployments share one active
database policy. Do this only when the services are intended to use the same
rules: a policy prepared for one component's routes can be incomplete or grant
unexpected access on another component.

### Startup Policy Import

`abac.policyFileImport` controls how `abac.modelPath` is used when the service
starts:

| Mode | Startup behavior |
| --- | --- |
| `always` | Reads and materializes the file on every startup. If the same policy is already active, that version is reused. Otherwise a new version is created and activated. |
| `if_missing` | Imports and activates the file only when the effective scope has no active policy. Otherwise the database policy is loaded and the file is not re-imported. |
| `never` | Does not read the policy file. Startup fails closed if the effective scope has no active database policy. |
| Empty | Uses the component default: `always` for Digital Twin Registry and `if_missing` for the other components listed under [Component Support](#component-support). |

With `if_missing`, changing the mounted JSON file does not change an existing
active policy on restart. With `always`, different files used by instances that
share a scope can successively supersede one another.

### Enabling the Management API

The `/security/abac/**` routes exist only when both `abac.enabled` and
`abac.managementApi.enabled` are `true`. Their OpenAPI definitions are added to
the service's Swagger document only under the same condition and when Swagger
itself is enabled.

## Protecting the Management API

The management routes pass through the active ABAC policy. Before enabling the
API, ensure that the active or startup policy explicitly grants the required
rights to trusted administrators for both `/security/abac` and
`/security/abac/*`. The route mappings use `READ`, `CREATE`, `UPDATE`, and
`DELETE` according to the operation.

ABAC-denied requests below `/security/abac` return `404 Not Found` rather than
`403 Forbidden`, which avoids exposing policy and rule identifiers through
probing. A disabled management API also has no routes and therefore returns
not found.

## Managing Policies

Paths below are relative to the service base URL, including any configured
`server.contextPath`. Use the runtime Swagger page for complete request and
response schemas.

| Purpose | Method and path |
| --- | --- |
| Inspect the active version or its rules | `GET /security/abac/active-policy`; `GET /security/abac/active-policy/rules` |
| List, import, or inspect versions | `GET` or `POST /security/abac/policy-versions`; `GET /security/abac/policy-versions/{versionID}` |
| Clone, validate, activate, or reject | `POST /security/abac/policy-versions/{versionID}/{clone|validate|activate|reject}` |
| Inspect or edit rules | `/security/abac/policy-versions/{versionID}/rules/**` |
| Inspect or edit definitions | `/security/abac/policy-versions/{versionID}/definitions/**` |

### Recommended Workflow

The normal change workflow is to inspect the active version, clone it, edit the
staged clone, validate it, and activate it:

```bash
export BASE_URL=http://localhost:8081
export TOKEN=replace-with-admin-token

export ACTIVE_VERSION_ID="$(
  curl --fail-with-body -sS \
    -H "Authorization: Bearer ${TOKEN}" \
    "${BASE_URL}/security/abac/active-policy" \
  | jq -r '.version_id'
)"

export DRAFT_VERSION_ID="$(
  curl --fail-with-body -sS -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    "${BASE_URL}/security/abac/policy-versions/${ACTIVE_VERSION_ID}/clone" \
  | jq -r '.version_id'
)"
```

Use the rule and definition endpoints or Swagger to edit
`${DRAFT_VERSION_ID}`. Then validate and activate it:

```bash
curl --fail-with-body -sS -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  "${BASE_URL}/security/abac/policy-versions/${DRAFT_VERSION_ID}/validate"

curl --fail-with-body -sS -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  "${BASE_URL}/security/abac/policy-versions/${DRAFT_VERSION_ID}/activate"
```

Verify the result with `GET /security/abac/active-policy`. Keep the old active
version's identifier until the new policy has been operationally verified. The
old version remains stored as `superseded` and can be cloned for a rollback
policy.

### Creating a Staged Version

`POST /security/abac/policy-versions` accepts a complete policy in the `policy`
field and creates a staged version. Optional `source_ref` metadata can identify
the change ticket or deployment source. Set `activate: true` only when import
and immediate activation are intentional. Creation and activation then use one
database transaction and a failure rolls back the imported version.

Cloning copies any stored version into a new staged version. Cloning the active
version is generally the safest starting point because it preserves currently
required routes while changes are prepared.

### Editing Staged Versions

The API provides list, create, replace (`PUT`), merge-patch (`PATCH`), and
delete operations for reusable `attributes`, `acls`, `objects`, and `formulas`.
It also supports creating, replacing, merge-patching, deleting, duplicating,
moving, and enabling or disabling staged rules. Definition changes can affect
every rule that references that definition.

Every edit rematerializes the complete staged policy within its database
transaction. A malformed change or unresolved reference is rejected without
committing the edit. Active, superseded, and rejected versions reject these
mutation operations.

`PUT` replaces the selected rule or definition. `PATCH` recursively merges JSON
objects. `null` removes a field. It is not RFC 6902 JSON Patch. The result must
still satisfy the policy grammar, including the mutually exclusive pairs
`ACL`/`USEACL`, `FORMULA`/`USEFORMULA`, and `OBJECTS`/`USEOBJECTS`.

Rule indices are 1-based. Inserting, deleting, duplicating, or moving rules
recomputes their order, and order is security-relevant. Audit
`matched_rule_id` values contain an order-derived prefix, so reordering can
change the identifier recorded for an otherwise unchanged rule.

### Validation, Activation, and Rejection

Validation reparses and materializes a staged policy, resolves reusable
definitions, refreshes its stored materialized rules and hashes, and returns
`valid`, `policy_id`, and `materialized_policy_hash`. Validation does not
activate the version. It verifies the grammar and materialization supported by
BaSyx. It does not prove that route coverage or organizational authorization
intent is complete.

Activation repeats validation. Superseding the current active version, marking
the staged version active, and recording the corresponding policy events use one
database transaction. When evidence is enabled, it must be written before that
transaction can commit. The handling service instance publishes the new
materialized rules to its evaluator only after the commit. If validation or
required evidence writing fails, the database changes roll back and the previous
active policy remains in use.

Rejecting changes a staged version to `rejected`. It remains stored and
inspectable but cannot be edited or activated. It can still be cloned into a
new staged version.

## Shared Databases and Multiple Replicas

Policy scopes partition the stored state, and a database constraint prevents
more than one active version for the same scope. The API does not provide
optimistic revision checks for concurrent draft edits or activations, so
coordinate policy writers instead of relying only on the database constraint.

For replicated services, use one startup-import owner per scope. Start or
restart followers with `never` after an active policy exists, or use
`if_missing` when simultaneous first startup is avoided. Do not use different
files with `always` on replicas sharing a scope: a later successful startup can
supersede the policy imported by another replica.

In v1.1.0 each process keeps its own in-memory evaluator cache. Activation or
startup import updates only the instance performing that operation. There is no
cross-replica cache invalidation. Coordinate a restart or rollout of the other
replicas after activation so all instances evaluate the same database policy.

## Audit and Evidence

Policy events in PostgreSQL record imports, edits, validation attempts,
activations, supersessions, and rejections. Records include available actor,
issuer, client, request/correlation, source, operation, endpoint, and before/after
hash information. The v1.1.0 management API does not expose a policy-event list.
Retain and inspect the database records through controlled operational tooling
when this audit trail is required.

Normal mutation history can record `policy_id` and `matched_rule_id`, allowing
an authorization decision to be related to the stored policy version and rule.
See [Recent Changes, History, and Signed Reads](history_and_changes) for the
separate resource-history feature.

When `history.evidence.enabled` is `true`, activation writes an
`abac_policy_version` artifact containing the configured and materialized policy,
ordered materialized rules, identifiers, hashes, scope, source, and activation
metadata. Required evidence storage must succeed before the database activation
can commit. The external object write itself is not part of the PostgreSQL
transaction, so a later database failure can leave an unreferenced evidence
object even though the active policy was not changed.

## Component Support

The following v1.1.0 services wire PostgreSQL-backed startup import and the
optional management routes:

- AAS Environment
- AAS Repository and Submodel Repository
- Concept Description Repository
- AAS Registry and Submodel Registry
- Basic Discovery
- AASX File Server
- Digital Twin Registry

Their built-in policy scopes are the corresponding service names passed by the
entry points. Management is disabled by default for all of them. For startup
policy import, Digital Twin Registry is the exception: it defaults to `always`,
while the others default to `if_missing`.

The DPP API uses a file-backed policy directly in v1.1.0 and does not expose
this PostgreSQL policy-management API. Company Lookup does not wire the shared
OIDC/ABAC stack.

## See Also

- [Runtime Security](security) for OIDC authentication and ABAC authorization
  semantics
- [General Configuration](configuration.md#oidc-and-abac) for the complete
  configuration reference
- [Recent Changes, History, and Signed Reads](history_and_changes) for resource
  history and evidence
- [Relationship-Based Access Control](rebac) for the optional ReBAC extension
