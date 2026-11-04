# Troubleshooting

Diagnose one layer at a time: cluster connection, required APIs/operators, storage, database initialization, application readiness, routing, then browser/API access. Do not change credentials or disable TLS to work around an unrelated startup problem.

In the commands below, set `BASYX_CONTEXT` to your actual context. Examples use namespace `basyx-evaluation`; substitute your assigned namespace if it differs.

## Cluster and chart selection

| Symptom | Check | Next action |
| --- | --- | --- |
| Connection refused, unauthorized, or certificate error before listing pods | `kubectl config get-contexts`; selected kubeconfig, context, API endpoint, credential validity, certificate hostname/CA | Fix the cluster connection with the cluster operator. Application values cannot fix a Kubernetes API certificate mismatch. |
| Helm cannot find a chart/version | `helm repo list`, `helm repo update`, `helm search repo basyx/basyx --versions` | Confirm the Go chart reference `basyx/basyx`, repository URL, and published version. |
| Template/schema error | Selected chart version and exact values keys | Compare against `helm show values` for that Go chart version rather than a different release's defaults. |
| Ingress or certificate cannot become ready | Remaining placeholders in your overlay | Replace `YOUR_INGRESS_CLASS`, `YOUR_CLUSTER_ISSUER`, and `basyx.example.com` with the platform details supplied by your administrator. |
| Resource already exists or has different ownership | Existing releases, fixed resource names, and namespace | Check `fullnameOverride`, `database.clusterName`, and resource ownership before changing anything. |

## Missing CRDs or unavailable controllers

Errors such as `no matches for kind "Cluster" in version "postgresql.cnpg.io/v1"` indicate a missing CloudNativePG API definition. A similar error for `Certificate` or `Issuer` means cert-manager is missing or not ready.

```bash
kubectl --context "$BASYX_CONTEXT" get crd \
  clusters.postgresql.cnpg.io certificates.cert-manager.io issuers.cert-manager.io
kubectl --context "$BASYX_CONTEXT" -n cnpg-system get pods
kubectl --context "$BASYX_CONTEXT" -n cert-manager get pods
```

Namespace names can differ on an existing platform. A CRD existing does not prove that its operator/webhook is healthy. Ask the operator owner if installation encounters webhook errors.

## Database and startup

```bash
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get pods,jobs,pvc
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get clusters.postgresql.cnpg.io
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get events \
  --sort-by=.metadata.creationTimestamp
```

| Symptom | Likely layer | What to inspect |
| --- | --- | --- |
| PVC is `Pending` | Storage | StorageClass, provisioner events, available capacity, and volume binding/scheduling. |
| PostgreSQL pods cannot schedule | Cluster capacity/topology | Resource requests, node/zone labels, affinity, and PVC placement. |
| Configuration Job stays in its wait init container | Database readiness | CloudNativePG status and the configured database address/Secret. |
| Job fails after reaching PostgreSQL | Schema, permissions, or configuration | Initializer logs and the Go Configuration Service error. |
| First install times out with `--wait` | Hook ordering | The Go schema initializer is post-install. Follow the non-waiting first-install procedure and inspect the existing failed release before retrying. |
| `ImagePullBackOff` | Image access | Image repository, exact tag/digest, credentials, registry access, and architecture support. |
| Runtime rejects the schema | Version alignment/state | Compatible runtime/initializer images and schema state. Do not delete the database to make a production service start. |

Inspect the initializer while its Job still exists:

```bash
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation describe job basyx-configuration
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation logs \
  job/basyx-configuration --all-containers --tail=100
```

A completed Job may later disappear because of its TTL. If a migration failed, use [Configuration Service operational guidance](../basyx_components/go/configuration_service/operations.md) rather than repeatedly retrying without checking database state.

## Browser, routing, and TLS

| Symptom | What it means to check |
| --- | --- |
| Ingress returns 404 | Host header/DNS, IngressClass, controller status, configured path, and backend Service/port. |
| HTTPRoute does not work | Gateway/controller availability, listeners, namespace permissions, `parentRefs`, and route conditions. |
| TLS certificate is untrusted | Correct CA trust and issuance. A lab CA is not automatically trusted. |
| Certificate hostname mismatch | The certificate must cover the hostname used in the browser/API address. An unexpired wildcard certificate does not match arbitrary nested subdomains. |
| UI loads, but its API calls fail | Browser-facing infrastructure URLs, CORS, active API services, and application authorization. A page loading is not an API health test. |
| UI asks for sign-in although Keycloak was disabled | UI infrastructure still has OAuth enabled. Use `security.type: None` only for a deliberately unsecured profile. |
| A fresh UI shows no AAS | Check the API directly. An empty database is expected until you import/create data. |

Compare the browser-facing host in `host` and `tls.hosts` with DNS, the certificate, and the Web UI's infrastructure URLs. The walkthrough uses one HTTPS hostname with `/aas-gui/` for the UI and `/aas-environment/` for the API; internal Kubernetes Service names are not browser addresses.

## Authentication is not authorization

For sign-in failures, inspect exact redirect URI, issuer, client settings, and certificate trust. For rejected API requests, inspect HTTP status and server logs: `401` commonly points to token authentication, while `403` commonly points to authorization. Confirm the actual endpoint's behavior rather than diagnosing only from the browser's generic message.

Verify token audience, trusted issuer, required claims, and the specific policy being evaluated. Do not paste access tokens, client secrets, database passwords, or unredacted Helm values into public issues.

## Asking for help

Provide the chart name/version, Helm version, Kubernetes/operator versions, deployment shape, sanitized values excerpt, exact command/error, relevant pod/Job events, and whether the failure is in cluster access, startup, or browser traffic.

Use the [BaSyx chart issue tracker](https://github.com/eclipse-basyx/charts/issues) for chart problems, and the [Go component documentation](../basyx_components/go/index.md) for application-specific behavior. Include a minimal reproducible example and remove private infrastructure details and secrets first.
