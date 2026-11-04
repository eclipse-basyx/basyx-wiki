# Configure Your Deployment

Use values files to express your deployment choices. The complete reference is the selected chart's `values.yaml` and `values.schema.json`; this page explains how the important groups fit together. Set `BASYX_CHART_VERSION` using {ref}`version selection <select-the-chart-version>` first.

## Inspect the version you actually install

```bash
helm show chart basyx/basyx --version "${BASYX_CHART_VERSION:?Select a chart version first}"
helm show values basyx/basyx --version "${BASYX_CHART_VERSION:?Select a chart version first}" > values.defaults.yaml
```

In the [chart repository](https://github.com/eclipse-basyx/charts), select tag `basyx-<your chart version>` and use its README, `charts/basyx` source, and `values` examples together. The repository's `main` branch may already document features that are not in your installed chart. For example, download an observability overlay matched to your selection:

```bash
curl --fail --location \
  "https://raw.githubusercontent.com/eclipse-basyx/charts/basyx-${BASYX_CHART_VERSION:?Select a chart version first}/values/values.observability.example.yaml" \
  --output values.observability.yaml
```

If the file is unavailable for an older release, inspect that release's available profiles instead of substituting an example from `main`.

## Choose a deployment shape

| Need | Starting profile in the chart repository | Important distinction |
| --- | --- | --- |
| One combined API runtime and the Web UI | `values/values.minimal.yaml` | Enables `aasEnvironment`; separate registries/repositories are disabled. |
| Separate core Go services | `values/values.example.yaml` | Unsecured evaluation profile. Individual services share the configured database. |
| Keycloak and ABAC | `values/values.secured.example.yaml` | Replace demo credentials and verify the actual access policy. |
| BaSyx Studio as the user interface | `values/values.studio.example.yaml`, where supplied by the selected release | Review that release's Studio storage, identity, and app-origin requirements. |
| Catena-X marker-based access example | `values/values.catena-x.example.yaml` | A specific DTR/Submodel Repository scenario, not a declaration of production compliance. |
| Existing PostgreSQL | `values/values.external-db.example.yaml` | Configure database connection and migration ownership explicitly. |
| Database sizing/scheduling | `values/values.postgres-production.example.yaml` | Tune to your storage, nodes, workload, and connection budget. |
| Gateway API | `values/values.gatewayapi.example.yaml` | Requires Gateway API CRDs and a functioning controller/Gateway. |
| Logs/traces or autoscaling | `values/values.observability.example.yaml`, `values/values.autoscaling.example.yaml` | Overlays, not complete deployment profiles. |

The sample files are stored in the Git repository; `helm show values` shows chart defaults, not all repository examples.

## How overrides work

Helm combines the chart defaults with your values. Later files override earlier ones, and command-line `--set` options override files. Maps can be overridden by key; lists are replaced rather than merged item by item.

For example:

```bash
helm template basyx basyx/basyx --version "${BASYX_CHART_VERSION:?Select a chart version first}" \
  --namespace basyx-evaluation \
  -f values.cluster-base.yaml -f values.cluster.yaml -f values.observability.yaml
```

This continues the installation walkthrough: load its downloaded base profile first, your cluster-specific overlay second, and any additional overlay last. Only add an observability file that you have created or copied from the matching chart release. Keep environment-specific files small enough to review. Save the full intended configuration for later upgrades instead of relying on remembered `--set` arguments or blindly reusing old values.

## Main configuration groups

| Values | Responsibility |
| --- | --- |
| `host`, `paths.*` | Browser-facing host and public service routes. |
| `ingress`, `<component>.ingress` | Controller class, annotations, and routing for Ingress. |
| `gatewayApi`, `<component>.httpRoute` | Alternative Gateway API routing. |
| `tls`, `internal.certificateIssuer`, `internal.CACertificates` | Ingress certificates, issuer resources, and outbound CA trust. These are separate concerns. |
| `database`, `<component>.database` | Managed or external PostgreSQL connections and storage settings. |
| `configurationService` | Schema initialization/migration Job and hook behavior. |
| `<component>.enabled` | Whether to deploy a component. Disabling a service does not migrate or erase its data. |
| `<component>.image` | Container image tag or digest. Empty tags for Go runtimes resolve to the chart's `appVersion`. |
| `<component>.resources` | CPU and memory requests/limits for that component; configured independently for each workload. |
| `general`, `server`, `history`, `eventing`, `rebac` | Structured Go runtime configuration; use the selected release's schema for the exact keys. |
| `environment.common`, `<component>.environment` | Explicit environment overrides. They may take precedence over structured runtime values. |
| `aasWebGui.infrastructureConfig` | Which APIs the Web UI uses and how it signs in. |
| `keycloak`, `abac`, `oidc` | Identity provider, authorization policies, and trusted token issuers. |

## CPU and memory requests and limits

Resource requests and limits can be configured in your cluster-specific values overlay. Set them separately for each enabled component using its `resources` block, for example `aasEnvironment.resources`, `aasWebGui.resources`, or `configurationService.resources`. For the managed PostgreSQL instances, use `database.resources`. Check the selected release's `values.yaml` for the available components and any additional resource blocks for init containers or poolers. There is no single global resource setting for all workloads.

The following example illustrates the syntax, **not recommended production sizing**. Merge the relevant blocks into `values.cluster.yaml` alongside your existing settings:

```yaml
aasEnvironment:
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: "2"
      memory: 1Gi

aasWebGui:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: "1"
      memory: 512Mi
```

`250m` means one quarter of a CPU core; `Mi` and `Gi` are binary memory units. Requests inform Kubernetes scheduling and resource allocation; they are not usage caps. CPU limits can throttle a busy container, while exceeding a memory limit can cause it to be terminated (`OOMKilled`). Keep requests less than or equal to the corresponding limits. Limits are optional: decide whether to cap CPU according to your platform policy and latency requirements rather than copying an example unchanged.

Size each workload from observed usage and load tests, allowing headroom for startup and peak traffic. Settings apply per pod/container, so account for replicas and other enabled components when planning node capacity. Empty `resources: {}` blocks do not explicitly set requests or limits in the chart; namespace `LimitRange` defaults and `ResourceQuota` restrictions may still apply. Application memory settings, such as a JVM heap, are separate from the container memory limit and must leave room for other memory usage.

Render and lint your merged values as described in {ref}`configuration checks <check-the-configuration>`, then apply them through the [values-only upgrade procedure](operations.md). Verify the resulting pod specifications and monitor resource usage after rollout. Updating Deployment resource settings normally replaces pods; plan for possible interruption in single-replica deployments.

## Web UI addresses and component selection

The browser calls the API URLs stored in the UI's infrastructure configuration. These must be reachable **from the browser**, not only from another pod. A URL such as `http://basyx-aas-registry:8080` is normally not suitable for an external user's browser.

The minimal profile maps UI operations to AAS Environment endpoints, including `/shells` and `/submodels`. A split deployment instead maps them to the respective services. For same-host HTTPS ingress, the defaults derive addresses from `host` and `paths.*`.

Check the rendered infrastructure after changing component selection. The combined AAS Environment still provides Registry and Discovery APIs even when the separate workloads are disabled. Disabling `aasRegistry` therefore does not mean that all references to its API area should be deleted from a combined AAS Environment setup. Consult the selected release's Web UI configuration guidance for how it handles disabled services and explicit external URLs.

Disabling Keycloak alone does not disable the Web UI's sign-in settings. An unsecured profile must also set the infrastructure's `security.type` to `None`, as the {ref}`minimal cluster profile <prepare-the-values-files>` does. For secured configurations, see [security](security.md).

## Managed or external PostgreSQL

The default managed database uses CloudNativePG. Choose `database.instances`, `database.storage.size`, and optionally `database.storage.storageClass` for your platform. The instance count does not replace a backup strategy.

For external PostgreSQL, the chart can reference an existing Secret:

```yaml
database:
  type: external
  existingSecret: basyx-postgres
```

The Secret must already exist in the release namespace with these keys: `host`, `port`, `dbname`, `user`, `password`, and `jdbc-uri`. Store it through your approved secret-management process. Optional TLS settings and component-specific database overrides are described in the chart reference.

The Configuration Service also needs the intended database connection. Do not point it at an unrelated database or silently disable it: Go runtimes require a compatible, clean schema. External database deployment, connectivity, permissions, and backups remain the database operator's responsibility.

Repository-to-Registry integration is not automatic HTTP synchronization between two pods. Review [the shared-database integration contract](../basyx_components/go/common/registry_integration.md) before splitting services across different databases.

## Images and custom files

Prefer the chart's compatible image set initially. When overriding it, keep the Configuration Service compatible with every runtime using its database. Set image digests when immutable image selection is required.

Chart-local logos and certificate files are read from the chart package/checkout with Helm's file access. Placing an arbitrary file beside your values file does not put it inside the chart. For certificates outside the chart package, use the supported existing Secret/ConfigMap trust-store references instead of assuming Helm can read any local path.

Next: [Security and production readiness](security.md), [advanced deployment](advanced.md), or [operations](operations.md).
