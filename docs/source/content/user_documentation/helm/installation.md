# Install BaSyx Go in Your Cluster

This walkthrough takes you from cluster access to a working AAS Web UI. **You can follow it even if this is your first Helm installation.** It assumes an existing Kubernetes cluster; the [prerequisites page](prerequisites.md) explains what to request from its administrator.

Experienced users can jump to [the values files](#prepare-the-values-files), [validation](#check-the-configuration), or [installation](#install-the-release). All commands use the **BaSyx Go chart** `basyx/basyx`, version **3.15.3**.

## What you will deploy

The walkthrough uses the chart's minimal profile:

- **AAS Environment:** one Go application providing AAS, Submodel, Concept Description, Registry, and Discovery API areas.
- **AAS Web UI:** the browser application where you work with AAS data.
- **PostgreSQL:** a persistent database managed by the existing CloudNativePG operator.
- **Configuration Service:** a one-time Job that initializes the database before the backend becomes ready.

Separate repository/registry workloads are disabled because their APIs are provided by the combined AAS Environment. This keeps the first deployment easier to understand.

```{important}
This profile has **no application authentication**. Use it only for a restricted evaluation environment whose network access is limited to the intended users. HTTPS encrypts the connection but does not decide who may read or change data. For an internet-facing or production environment, configure [authentication and authorization](security.md) before exposing the applications.
```

## 1. Check tools and platform access

On your workstation, open a terminal and check:

```bash
kubectl version --client
helm version --short
curl --version
```

If a command is missing, follow [the tool installation instructions](prerequisites.md#your-workstation). You also need the administrator-provided context, namespace, StorageClass, IngressClass, DNS hostname, and certificate issuer listed under [cluster information](prerequisites.md#information-to-request-from-your-administrator).

## 2. Select the right cluster and namespace

A kubeconfig contains the cluster address and your authentication settings. `kubectl` and Helm normally read it from your user directory. If your administrator gave you a separate file, select that file first:

```bash
export KUBECONFIG=/absolute/path/to/your/kubeconfig.yaml
```

Replace the path with the real file. Skip that command if your normal kubeconfig is already configured. Treat the file as a credential and do not commit it to the chart or wiki repository.

List the available contexts:

```bash
kubectl config get-contexts
```

Use the administrator-provided **NAME** from that output, not a guessed hostname. Set the following variables in your terminal:

```bash
BASYX_CONTEXT=YOUR_CONTEXT
BASYX_NAMESPACE=basyx-evaluation
BASYX_HOST=basyx.example.com
```

Replace `YOUR_CONTEXT` with the real context, use your assigned namespace instead of `basyx-evaluation` if different, and replace `basyx.example.com` with the assigned DNS hostname. Keep the same namespace and hostname throughout this guide and in the values file. The `BASYX_*` variables are shell shortcuts; Helm does not automatically insert them into YAML files.

All following cluster commands select the context explicitly. `--namespace` (short form `-n`) selects the namespace inside that cluster. In a new terminal, set these variables again before continuing.

Check your namespace-scoped permissions:

```bash
kubectl --context "$BASYX_CONTEXT" auth can-i create deployments \
  --namespace "$BASYX_NAMESPACE"
kubectl --context "$BASYX_CONTEXT" auth can-i create secrets \
  --namespace "$BASYX_NAMESPACE"
kubectl --context "$BASYX_CONTEXT" auth can-i create clusters.postgresql.cnpg.io \
  --namespace "$BASYX_NAMESPACE"
```

Expected answer: `yes` for each. These are useful initial checks, not an exhaustive permissions test: the release also creates Services, ConfigMaps, Jobs, service accounts, ingress, and certificate resources. If you receive `no`, ask your administrator to assign the required deployment rights.

## 3. Verify the cluster prerequisites

The platform administrator should confirm the required operators and routing setup. If your user can inspect cluster-wide resources, check:

```bash
kubectl --context "$BASYX_CONTEXT" get storageclass
kubectl --context "$BASYX_CONTEXT" get ingressclass
kubectl --context "$BASYX_CONTEXT" get crd \
  clusters.postgresql.cnpg.io certificates.cert-manager.io \
  issuers.cert-manager.io clusterissuers.cert-manager.io
kubectl --context "$BASYX_CONTEXT" get clusterissuer
```

What to look for:

| Result | Meaning |
| --- | --- |
| A usable StorageClass | PostgreSQL can request a persistent volume. Set its name in the overlay, or use a suitable class marked `(default)`. |
| The assigned IngressClass | Its controller will receive browser requests for your application. Use the exact name in the overlay. |
| All four CRDs exist | Kubernetes understands the database and certificate resource types used here. The operators must also be healthy. |
| Your ClusterIssuer reports `READY=True` | It is ready to request certificates. It must also be authorized to issue one for your hostname. |

A `Forbidden` response to these cluster-wide checks may simply mean your application account cannot list platform resources. Ask the administrator to verify them; do not install another operator to work around missing inspection rights.

## 4. Add the Helm repository

Run these commands from a working directory where you will keep your values files:

```bash
helm repo add basyx https://eclipse-basyx.github.io/charts
helm repo update
helm show chart basyx/basyx --version 3.15.3
```

`helm repo add` registers a download location on your workstation. It does not install anything in Kubernetes. In `basyx/basyx`, the first `basyx` is your repository alias; the second is the chart name.

The metadata should include `version: 3.15.3` and `appVersion: 1.1.1`. Pinning `--version` makes the examples independent of later repository updates.

(prepare-the-values-files)=
## 5. Prepare the values files

Values are the configuration inputs Helm uses to generate Kubernetes resources. We use two files so the release-matched base stays separate from your environment settings.

First, download the chart release's minimal profile:

```bash
curl --fail --location \
  https://raw.githubusercontent.com/eclipse-basyx/charts/basyx-3.15.3/values/values.minimal.yaml \
  --output values.cluster-base.yaml
```

Then download {download}`values.cluster.yaml <examples/values.cluster.yaml>` into the **same working directory** and open it in your text editor:

```{literalinclude} examples/values.cluster.yaml
:language: yaml
:caption: values.cluster.yaml — environment-specific overlay
```

Replace these settings before continuing:

| Setting | What to enter |
| --- | --- |
| `host` and `tls.hosts[0]` | Your assigned hostname, without `https://` or a path; it must match `BASYX_HOST`. |
| `ingress.className` | The installed IngressClass name supplied by the administrator. Replace `YOUR_INGRESS_CLASS`. |
| `ingress.clusterIssuer` | The existing cert-manager ClusterIssuer name. Replace `YOUR_CLUSTER_ISSUER`. |
| `database.storage.storageClass` | The assigned StorageClass, or leave `""` to use a suitable default. |
| `database.storage.size` | The evaluation database's requested storage; the example uses `10Gi`. |

The overlay selects the platform ClusterIssuer and clears the base file's namespaced ingress issuer. The base still creates the chart's internal issuer resources; those are separate from the certificate authority selected for browser access. If your platform uses a namespaced Issuer instead, follow [TLS configuration](security.md#tls-and-trust) with your administrator rather than guessing a ClusterIssuer name.

The base file already contains the Web UI's API addresses and turns off its OAuth configuration for this evaluation profile. Keep those mappings. The overlay enables Repository/Registry/Discovery integration in the combined runtime so descriptors and discovery mappings follow newly created content.

Helm reads `-f` files **from left to right**: the later file overrides matching keys in the earlier one. Both files are needed. No edits to chart templates are required.

```{note}
YAML indentation is significant: use spaces, not tabs. The overlay contains placeholders and must be edited before installation. Do not copy only a few settings into a new file and discard the base profile. If sharing the namespace with another release, agree on distinct resource names such as `fullnameOverride` and `database.clusterName` first.
```

(check-the-configuration)=
## 6. Check the configuration

Render the intended resources without changing the cluster:

```bash
helm template basyx basyx/basyx \
  --version 3.15.3 --namespace "$BASYX_NAMESPACE" \
  -f values.cluster-base.yaml -f values.cluster.yaml > rendered.yaml
```

`basyx` immediately after `helm template` is the chosen **release name**: the name of this installation. It is not the context or namespace. The command writes the resulting manifests to `rendered.yaml` for inspection.

For an additional lint check, download the exact chart package:

```bash
helm pull basyx/basyx --version 3.15.3 --untar
helm lint ./basyx -f values.cluster-base.yaml -f values.cluster.yaml
```

Here `./basyx` is a downloaded directory on your workstation, while `basyx/basyx` is a Helm repository/chart reference. Both identify the same pinned chart in this procedure.

Check that the rendered output has your hostname, IngressClass, issuer, database size, and intended application images. `helm lint` can succeed even if placeholder names still exist, so this inspection matters. Neither linting nor rendering proves that the cluster's storage, certificate issuance, or networking works.

(install-the-release)=
## 7. Install the release

After reviewing the configuration, run:

```bash
helm install basyx basyx/basyx \
  --version 3.15.3 \
  --kube-context "$BASYX_CONTEXT" \
  --namespace "$BASYX_NAMESPACE" --create-namespace \
  -f values.cluster-base.yaml -f values.cluster.yaml \
  --timeout 15m
```

| Option | Meaning |
| --- | --- |
| `basyx` | Release name used again in status, upgrade, and uninstall commands. |
| `--version 3.15.3` | The exact chart version. |
| `--kube-context` | The cluster/user context selected in step 2. |
| `--namespace` | Where the release resources are created. |
| `--create-namespace` | Create the namespace if absent. This requires permission to create namespaces; if the administrator already created it, you can omit the flag. |
| The two `-f` options | Base profile first, your environment overlay second. |
| `--timeout 15m` | Maximum wait for operations such as hook Jobs. |

On the first installation, PostgreSQL provisioning and image downloads can take several minutes. The Configuration Service waits for PostgreSQL, prepares its schema, and exits successfully.

This Helm 3 first-install command deliberately omits `--wait` and `--atomic`: the initializer runs as a **post-install hook**, while the backend needs initialization before becoming ready. Waiting for backend readiness before running that hook can deadlock the installation. Check readiness explicitly in the next step.

If Helm reports that the name is already in use, first inspect `helm list` and `helm status` in the same context/namespace. Do not repeatedly run a fresh install against an existing release. See [operations](operations.md) for an intentional update and [troubleshooting](troubleshooting.md) for a failed installation.

## 8. Verify the workloads

After Helm returns successfully:

```bash
helm --kube-context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" status basyx
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" get pods,jobs,svc,ingress,pvc
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" get clusters.postgresql.cnpg.io
```

Expected results:

| Resource | Successful state |
| --- | --- |
| PostgreSQL storage claims | `Bound`, meaning storage was allocated. |
| PostgreSQL cluster | Becomes healthy with its database instance ready. |
| `basyx-configuration` Job | `Completed`: successful exit is expected, not a permanently running pod. |
| AAS Environment and Web UI | Their pods become ready, and the rollout checks below complete. |

```bash
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" rollout status \
  deployment/basyx-aas-environment --timeout=300s
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" rollout status \
  deployment/basyx-aas-web-ui --timeout=300s
```

The names above match `fullnameOverride: basyx` in the overlay. If you change that value, use the names shown by `kubectl get deployments` instead.

If initialization fails, inspect its logs and namespace events:

```bash
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" logs \
  job/basyx-configuration --all-containers --tail=100
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" get events \
  --sort-by=.metadata.creationTimestamp
```

Finished Jobs have a cleanup TTL, so a later `NotFound` does not by itself indicate failure. Persistent `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff` states need investigation; use [startup troubleshooting](troubleshooting.md#database-and-startup).

## 9. Check HTTPS and open the Web UI

Verify routing and certificate readiness:

```bash
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" get ingress
kubectl --context "$BASYX_CONTEXT" -n "$BASYX_NAMESPACE" get certificates
```

An Ingress resource needs the functioning controller selected by its IngressClass. The hostname must resolve to that controller's reachable entry point. The issued certificate should report `READY=True` and cover the same hostname.

Check the API from your workstation:

```bash
curl --fail "https://$BASYX_HOST/aas-environment/health"
curl --fail "https://$BASYX_HOST/aas-environment/shells"
```

Both requests should succeed. A fresh database has no user-created AAS data, so an empty result from `/shells` is normal. If DNS, certificate trust, or routing fails, solve that layer with your administrator before continuing; bypassing verification would hide a configuration problem.

In your browser, open **`https://YOUR_HOST/aas-gui/`**, replacing `YOUR_HOST` with the same real hostname used above. The AAS Environment's Swagger UI is at `https://YOUR_HOST/aas-environment/swagger`.

The Web UI runs in your browser and calls the configured public API addresses. A successful page load does not prove that those API calls work. If the UI loads but cannot retrieve data, compare its API addresses with the hostname and the two API checks above.

## 10. Continue with your deployment

You have completed the installation when the backend and Web UI are ready, HTTPS works, and the UI can reach the APIs. Continue in the [AAS Web UI](../basyx_components/web_ui/index.md) to browse or import suitable AAS data; Helm does not load example product data automatically.

Keep the pinned chart version and both non-secret values files for later changes. Record operator/controller versions separately. For an upgrade, pass the same reviewed files in the same order; do not treat `helm install` as an update command.

Next steps: [configuration](configuration.md), [authentication and production readiness](security.md), and [operation, upgrades, and removal](operations.md).
