# Security and Production Readiness

The unsecured evaluation profile is a learning environment. A production deployment needs decisions about identities, permissions, certificates, persistence, and operation; enabling HTTPS alone does not supply all of them.

## Separate four different questions

| Question | Mechanism |
| --- | --- |
| Am I connected to the intended server over an encrypted channel? | TLS certificates and trust. |
| Who is the user? | Authentication through a configured identity provider, commonly Keycloak/OIDC. |
| Which operations and data may that user access? | Authorization policies such as the Go components' ABAC, and optionally ReBAC. |
| Who may change the Kubernetes deployment? | Kubernetes RBAC and the access model of your deployment pipeline. |

A Keycloak realm role is not automatically a Kubernetes role, a Web UI editing permission, or a policy grant in every BaSyx API. Keep those mappings explicit and test both permitted and denied requests.

## TLS and trust

The [installation walkthrough](installation.md) uses the platform's Ingress controller and an existing cert-manager ClusterIssuer whose certificates the browser trusts. Confirm the hostname, certificate issuance, and network access restrictions with the platform administrator before exposing the evaluation profile.

The example internal CA is useful for controlled testing, but browsers and external services do not automatically trust it. Do not make certificate warnings the normal user workflow. Use your organization's certificate distribution process or an appropriately trusted certificate authority.

With an existing cert-manager ClusterIssuer, an ingress override can look like this:

```yaml
ingress:
  clusterIssuer: platform-issuer
  issuer: ""
tls:
  enabled: true
  hosts:
    - basyx.example.com
```

`platform-issuer` must already exist and be suitable for this hostname. The chart's internal issuer/trust-store configuration is a separate setting; review it even if ingress certificates are issued elsewhere.

TLS identity must match the public hostname. An existing certificate that does not include that hostname will fail validation even if it is otherwise trusted and not expired. Backend pods also need to trust certificates on outbound calls to an external identity provider or database.

## Authentication and authorization

Start by reviewing `values/values.secured.example.yaml` from the selected release in the [chart repository](https://github.com/eclipse-basyx/charts). Use tag `basyx-<your chart version>`, as described under [version-matched examples](configuration.md#inspect-the-version-you-actually-install). It enables Keycloak and ABAC and includes demonstration users. It is an example, not a production identity policy.

Before using it in a shared environment:

1. Replace all demonstration administrator, client, and user credentials. Review default users in the chart as well as overrides in your values file.
2. Choose an embedded Keycloak or an externally operated identity provider, and configure the Web UI client and exact redirect URLs for your public host/path.
3. Verify issuer, audience, token claims, and trusted signing keys against the intended provider.
4. Write and test the required API authorization rules. A role claim such as `role=admin` must actually be issued and trusted for a rule that uses it to work.
5. Test with a minimally privileged user and an administrator. Verify denied writes and data visibility, not only a successful sign-in.

The chart provides structured `oidc.providers` configuration and per-service ABAC overrides. See [Go security documentation](../basyx_components/go/common/security.md) and the selected chart's reference rather than assuming that all BaSyx implementations use identical claims or policy files.

Review the selected release's ReBAC support and policy semantics before enabling it. In the documented Go authorization model, ReBAC is a union with ABAC: either mechanism may grant a request. It is not an additional restriction applied after ABAC. Do not enable it as a presumed way to narrow existing grants.

## Secrets and network access

- Keep passwords, client secrets, private keys, and tokens out of public values files and source repositories.
- Helm release records and rendered manifests can contain secret material. A Kubernetes `Secret` object is not a substitute for controlling who can read those records.
- Use the chart's supported existing-secret references where available. Do not invent a generic `existingSecret` setting for every component; check the actual values/schema and templates.
- Configure database and identity-provider credentials through your deployment platform's secret-management process.
- Restrict network reachability to what the application needs. NetworkPolicies only take effect with a network plugin that enforces them, and must still allow DNS, database, identity-provider, and ingress traffic as appropriate.

## Production readiness review

Before going live, assign owners and verify:

- Pinned chart/operator/image versions and a tested upgrade procedure.
- Appropriate node capacity, resource requests/limits, database connection budget, and storage performance.
- Persistent database storage and a tested backup **and restore**, including PostgreSQL Large Objects where used.
- Database availability requirements and the implications of failure-domain scheduling.
- TLS, identity lifecycle, least-privilege access, and policy tests.
- Monitoring, logs, alerts, and operational contacts.
- Recovery procedures for a failed database migration; Helm rollback alone cannot restore the previous schema/data.

Continue with [operations](operations.md) and [advanced deployment](advanced.md).
