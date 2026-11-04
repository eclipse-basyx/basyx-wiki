# Kubernetes and Helm Basics

This page introduces the concepts needed for the [cluster installation walkthrough](installation.md). You do not need to write Kubernetes manifests yourself to complete it.

## The tools and their responsibilities

| Term | Meaning in this guide |
| --- | --- |
| Container image | A packaged application, such as the BaSyx AAS Environment or AAS Web UI. |
| Kubernetes cluster | The infrastructure that schedules containers and manages their networking and storage. Your administrator provides access to an existing cluster. |
| Node | A physical or virtual machine on which Kubernetes runs workloads. |
| `kubectl` | The command-line tool for inspecting and interacting with a cluster. |
| Kubeconfig / context | Connection settings and credentials. A context selects a cluster, a user identity, and optionally a default namespace. |
| Namespace | A named scope for resources within a cluster. It is not a separate cluster or a complete security boundary. |
| Helm | A tool that renders parameterized Kubernetes manifests and tracks installations. It does not create a Kubernetes cluster. |
| Chart | A versioned package of templates and default configuration values. |
| Values file | YAML settings that customize a chart without editing its templates. |
| Release | One named installation of a chart, for example `basyx` in namespace `basyx-evaluation`. |
| Operator / CRD | An operator manages specialized resources. Its Custom Resource Definitions teach Kubernetes about types such as a PostgreSQL `Cluster` or a TLS `Certificate`. |

For example, the same chart can be installed into two namespaces with different values. Those are two releases with separate application configuration. Cluster-wide operators may be shared between them.

## What will appear in Kubernetes?

| Resource | Why you will encounter it |
| --- | --- |
| Deployment | Maintains application pods, such as the AAS Web UI. |
| Pod | Runs application containers. A pod being `Running` does not necessarily mean the application is ready. |
| Service | Provides a stable network address for a group of pods. |
| ConfigMap | Holds non-secret application configuration. |
| Secret | Holds credentials or certificate material. It still needs Kubernetes access control and appropriate protection at rest. |
| Job | Runs a task to completion. The BaSyx Configuration Service initializes or migrates the database this way. |
| PersistentVolumeClaim (PVC) | Requests durable storage. PostgreSQL stores application data there rather than inside an application pod. |
| Ingress / HTTPRoute | Routes browser requests into the cluster through an installed controller. Merely creating the resource does not install that controller. |

## The Go chart's startup sequence

1. Kubernetes creates the release resources. CloudNativePG provisions PostgreSQL and its storage.
2. The Configuration Service Job waits for PostgreSQL, initializes or migrates the schema, and exits successfully.
3. BaSyx runtime services become ready against the initialized database.
4. The Web UI connects to the configured APIs through addresses reachable from the user's browser.

CloudNativePG and cert-manager are **prerequisites**, not Helm subcharts automatically installed by the Go chart. Administrators install these operators first. See [prerequisites](prerequisites.md).

The Configuration Service Job uses `post-install` on first installation and `pre-upgrade` on upgrades. A job showing `Completed` is expected; it is not a permanently running application.

## Versions and releases

These are separate identifiers; their actual values depend on your selected release:

| Example | What it identifies |
| --- | --- |
| `BASYX_CHART_VERSION` | The Kubernetes templates and default values. Select it with Helm's `--version` and keep it fixed for the deployment. |
| Chart `appVersion` | The default image tag for Go services whose image tag is empty, including the Configuration Service. Inspect it with `helm show chart`. |
| Web UI or Studio image tag | A separate application image version selected by the chart. Inspect it with `helm show values`; it does not share the Go service version number. |
| Release revision `1`, `2`, … | Helm's history for one installed release, not an application version. |

Do not substitute a chart version for a container image tag. Keep Configuration Service and database-backed runtime images compatible. A Helm rollback restores Kubernetes configuration; it does not reverse a database migration. Read [operation and upgrade guidance](operations.md) before changing an existing installation.

## A first read-only inspection

Once your tools are installed:

```bash
kubectl config get-contexts
kubectl config current-context
kubectl get nodes
helm list --all-namespaces
```

These commands inspect your selected cluster. Before installing anything, choose the context confirmed by your administrator explicitly. The walkthrough stores it in `BASYX_CONTEXT` and uses namespace `basyx-evaluation`, so it does not depend on your default namespace.

Next: [Prepare the tools and cluster](prerequisites.md).

For further background, see the official [Kubernetes concepts](https://kubernetes.io/docs/concepts/overview/) and [Helm 3 introduction](https://helm.sh/docs/v3/intro/using_helm/).
