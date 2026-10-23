# Prepare Your Tools and Cluster

You install BaSyx Go **into an existing Kubernetes cluster**. The cluster can be provided by your organization or hosting platform. You do not have to build or administer Kubernetes yourself to follow [the installation guide](installation.md).

If Kubernetes or Helm is new to you, first read [the basics](fundamentals.md). Then arrange the cluster access and platform prerequisites below.

## Your workstation

Install these tools on the computer from which you will deploy BaSyx:

| Tool | What you use it for | Installation |
| --- | --- | --- |
| `kubectl` | Connect to Kubernetes, inspect workloads, and read logs | [Kubernetes installation guide](https://kubernetes.io/docs/tasks/tools/) |
| Helm 3 | Download and install the BaSyx chart | [Helm 3 installation guide](https://helm.sh/docs/v3/intro/install/) |
| `curl` | Download the example values and check the deployed API | Use your operating system's installation/package instructions. |

Check that the commands are available:

```bash
kubectl version --client
helm version --short
curl --version
```

The chart repository tests with Helm 3. Use tool and operator releases compatible with your cluster's Kubernetes version; Helm 4 waiting and plugin behavior is not necessarily identical to the Helm 3 procedure documented here.

Examples use Bash-compatible syntax. On Windows, use a suitable shell such as WSL, or adapt variables and line continuations to PowerShell. You will run `kubectl` and Helm on your workstation; Kubernetes runs the applications on the cluster's nodes.

## Information to request from your administrator

| Ask for | Why it is needed | Used in the installation guide |
| --- | --- | --- |
| Kubeconfig and any login instructions | Connect to the intended cluster as your user. Some platforms require a login helper or VPN. | `KUBECONFIG`, if a non-default file is used. |
| Kubernetes context name | Select the correct cluster/user configuration. | `BASYX_CONTEXT`. |
| Namespace and deployment permissions | Create BaSyx resources in the assigned namespace. | `BASYX_NAMESPACE`. |
| StorageClass and available capacity | Provision PostgreSQL's persistent volumes. | `database.storage.storageClass` and `size`. |
| IngressClass and working ingress controller | Route browser requests to the application Services. | `ingress.className`. |
| DNS hostname and network access | Reach the ingress endpoint from your browser and API clients. | `host`, `tls.hosts`, and `BASYX_HOST`. |
| cert-manager ClusterIssuer and CA trust instructions | Obtain a certificate valid for that hostname and trusted by clients. | `ingress.clusterIssuer`. |
| Confirmation that CloudNativePG and cert-manager are installed | Reconcile the database and certificate resources emitted by the chart. | Checks before installation. |

The installation guide uses an existing **ClusterIssuer** and **Ingress** as one concrete path. A namespaced Issuer or Gateway API deployment is also possible, but should be configured deliberately with the platform administrator; see [security](security.md#tls-and-trust) and [advanced deployment](advanced.md).

DNS must point the assigned hostname at the intended ingress entry point. Adding `host` to a values file does not create a DNS record or install a routing controller.

## Cluster-administrator tasks

CloudNativePG and cert-manager are shared platform components. Installing them creates cluster-wide Custom Resource Definitions (CRDs) and normally requires administrator permissions. An application user should first confirm that they already exist rather than installing duplicate operators.

If they are missing, the cluster administrator can use the following pinned example baseline, **after checking compatibility with the cluster**. Set `BASYX_CONTEXT` to the real target context first:

```bash
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm upgrade --install cnpg cnpg/cloudnative-pg \
  --version 0.29.1 \
  --kube-context "$BASYX_CONTEXT" \
  --namespace cnpg-system --create-namespace \
  --wait --timeout 10m

helm upgrade --install cert-manager jetstack/cert-manager \
  --version v1.19.3 \
  --kube-context "$BASYX_CONTEXT" \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --wait --timeout 10m
```

These versions are explicit documentation examples, not automatically selected latest releases. Use the [CloudNativePG installation documentation](https://cloudnative-pg.io/documentation/current/installation_upgrade/) and [cert-manager Helm guide](https://cert-manager.io/docs/installation/helm/) for support policies, permissions, and operator upgrades.

The administrator should verify that the resource definitions and operator pods are ready:

```bash
kubectl --context "$BASYX_CONTEXT" wait \
  --for=condition=Established crd/clusters.postgresql.cnpg.io --timeout=120s
kubectl --context "$BASYX_CONTEXT" wait \
  --for=condition=Established crd/certificates.cert-manager.io --timeout=120s
kubectl --context "$BASYX_CONTEXT" wait \
  --for=condition=Established crd/issuers.cert-manager.io --timeout=120s
kubectl --context "$BASYX_CONTEXT" wait \
  --for=condition=Established crd/clusterissuers.cert-manager.io --timeout=120s
kubectl --context "$BASYX_CONTEXT" -n cnpg-system get pods
kubectl --context "$BASYX_CONTEXT" -n cert-manager get pods
```

Operator namespace names can differ on an existing platform. The Go chart still emits cert-manager Issuer resources when public TLS is disabled; disabling `tls.enabled` alone does not remove that prerequisite.

The platform must also provide working persistent storage, the ingress controller, the selected ClusterIssuer, and DNS. The operator commands above do not set up those platform-specific pieces.

Next: [Install BaSyx Go in your cluster](installation.md).
