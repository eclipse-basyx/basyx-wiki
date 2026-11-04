# Advanced Deployment

Use these topics after you have a working [installation](installation.md). They extend the Go chart; each still requires suitable cluster infrastructure and an explicit operational owner.

## GitOps and Argo CD

A Helm CLI installation and an Argo CD Application do not run the same lifecycle. Argo CD renders Helm templates and applies resources through its own sync engine. It does not create a normal Helm release that you subsequently upgrade with the Helm CLI.

The Go chart provides opt-in ordering annotations:

```yaml
argocd:
  enabled: true
  runtimeSyncWave: "20"

configurationService:
  hook:
    argocd:
      enabled: true
      hook: Sync
      syncWave: "10"
      deletePolicy:
        - BeforeHookCreation
```

This orders the Configuration Service after prerequisite resources and before annotated runtime Deployments. Verify the rendered Argo CD annotations and the actual sync behavior, especially on a fresh namespace. PostgreSQL readiness and the initializer still matter.

Sync waves do not automatically stop old database writers before a migration. Combine GitOps changes with the maintenance procedure described in [operations](operations.md). Do not manage the same release simultaneously with independent Helm CLI and Argo CD workflows.

Keep chart versions and non-secret overlays in Git, and provision secrets through your platform's supported mechanism. Prefer an explicit deployment review when a chart update changes database schemas or access policy.

## Ingress or Gateway API

The chart supports Kubernetes Ingress and opt-in HTTPRoutes. Select the mechanism supported by your platform; neither resource installs a routing controller by itself.

For a pre-existing Gateway, for example:

```yaml
gatewayApi:
  parentRefs:
    - name: platform-gateway
      namespace: gateway-system

aasEnvironment:
  ingress:
    enabled: false
  httpRoute:
    enabled: true

aasWebGui:
  ingress:
    enabled: false
  httpRoute:
    enabled: true
```

The Gateway must allow routes from the application namespace and have suitable listeners and certificate configuration. Verify HTTPRoute `Accepted` and `ResolvedRefs` conditions; a rendered HTTPRoute alone is not evidence that traffic is routed.

Apply the same routing decision to every publicly exposed component in your chosen topology. For a chart-managed Gateway, see the release's `gatewayApi.gateway` settings and `values.gatewayapi-managed.example.yaml`. Do not enable one Gateway/LoadBalancer per release accidentally when the platform intends a shared Gateway.

Official background: [Gateway API guides](https://gateway-api.sigs.k8s.io/guides/).

## Observability

The chart can configure structured logging and export Go telemetry to an existing OpenTelemetry Collector:

```yaml
logging:
  format: json
  level: info

telemetry:
  tracesExporter: otlp
  endpoint: http://otel-collector.observability.svc.cluster.local:4318
  protocol: http/protobuf
```

Replace the endpoint with a real Collector and review sampling, credentials, and data handling. This configures applications; it does **not** deploy a Collector, tracing backend, or dashboards. See the [Go observability documentation](../basyx_components/go/common/observability.md) and versioned `values.observability.example.yaml`.

Database PodMonitor resources require the Prometheus Operator CRDs. Enable those resources only when your monitoring platform provides them, just as HTTPRoutes require Gateway API CRDs.

## Scaling and PostgreSQL connection budgets

More backend replicas mean more connection pools. A per-pod maximum of 50 connections can become 300 across six pods, before accounting for the initializer, identity service, and operational clients. Size the aggregate budget against PostgreSQL capacity rather than copying a per-pod limit without calculation.

Horizontal Pod Autoscaling needs a metrics source and appropriate CPU/memory resource requests. Review `<component>.autoscaling` and the versioned autoscaling example. Do not infer that adding replicas makes a workload or database highly available across failure domains.

For database topology, WAL storage, resources, and performance measurements, start with `values.postgres-production.example.yaml`, then tune to your own nodes and StorageClasses. For reader replicas or pooling, review the chart's explicit `database.reader` and pooler settings; they do not make every operation safe to send to a read replica.

## Contributing chart changes

Use a source checkout when modifying templates, adding chart-local assets, or contributing fixes. Work on the chart repository, not on a downloaded values file alone.

```bash
helm lint charts/basyx -f values/values.minimal.yaml
helm template basyx charts/basyx -n basyx-test -f values/values.minimal.yaml
```

The chart repository also contains helm-unittest suites and CI installation tests. Follow its versioned contributor/test instructions when installing plugins and running those tests. A unit test of rendered YAML does not replace an actual operator-backed installation test.
