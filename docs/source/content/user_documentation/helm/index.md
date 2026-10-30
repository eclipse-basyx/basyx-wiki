# Deploy BaSyx Go with Helm

Deploy Eclipse BaSyx Go on Kubernetes with the official `basyx` Helm chart, from your first installation in an existing cluster to an operated environment with authentication, persistent storage, and controlled upgrades.

You do not need Kubernetes experience to follow the guide. Start with the concepts, request access and platform details from your cluster administrator, then follow the installation walkthrough. Each stage explains the commands and the results to check. If you already operate Kubernetes, skip directly to installation and configuration.

## Choose your starting point

| Your situation | Start here | What you will achieve |
| --- | --- | --- |
| “I have never used Kubernetes or Helm.” | [Understand the basics](fundamentals.md), [prepare access](prerequisites.md), then [install step by step](installation.md) | Understand the terms and install BaSyx with your cluster administrator's platform details. |
| “I already have a Kubernetes cluster.” | [Install in an existing cluster](installation.md) | Select a chart, render a pinned release, and configure access. |
| “I need to adapt an installation.” | [Configure your deployment](configuration.md) | Choose components, database connections, URLs, and values overlays. |
| “I need authentication or a production deployment.” | [Security and production readiness](security.md) | Separate TLS, sign-in, authorization, and operational responsibilities. |
| “I run BaSyx through a deployment pipeline.” | [Advanced deployment](advanced.md) | Handle GitOps ordering, Gateway API, observability, and scaling. |
| “I need to upgrade, back up, or remove BaSyx.” | [Operate and upgrade](operations.md) | Understand migration ordering and persistent state. |
| “Something does not work.” | [Troubleshooting](troubleshooting.md) | Diagnose problems from the cluster up to the browser. |

## The BaSyx Go chart

This section documents `basyx/basyx` from the [Eclipse BaSyx chart repository](https://eclipse-basyx.github.io/charts/). **This guide has been validated with chart version 3.17.0.** The installation walkthrough sets that reference version once as `BASYX_CHART_VERSION`; every subsequent Helm command and example download uses that selection. Other releases may require different settings; review their release notes and tagged reference before changing the version.

Here, `basyx/` before the chart name is the **local Helm repository alias**, not a Kubernetes namespace. Chart version, backend version, Web UI version, and Helm release revision describe different things. See [versions and releases](fundamentals.md#versions-and-releases).

List available releases before following {ref}`the version selection step <select-the-chart-version>`:

```bash
helm repo add basyx https://eclipse-basyx.github.io/charts
helm repo update
helm search repo basyx/basyx --versions
```

Choose a release after reviewing its [release notes](https://github.com/eclipse-basyx/charts/releases). Keep that exact version with your deployment configuration. Selecting a release does not imply that the newest one is suitable for every existing database or cluster.

## Version-specific reference

The [chart repository](https://github.com/eclipse-basyx/charts) maintains the full values reference, image defaults, component-specific examples, and upgrade notes. Select the `basyx-<chart version>` tag there to match your installation; the installation guide also shows how to download examples from that tag. The wiki describes the workflow rather than duplicating that reference.

The [Helm documentation check](https://github.com/eclipse-basyx/basyx-wiki/actions/workflows/helm-docs.yml) renders and lints the installation examples against the reference chart and the latest stable chart on a weekly schedule and when these pages change. The latter is an additional compatibility check, not a change to this guide's reference version. It checks generated resources without deploying them. Historical releases can differ; use their tagged documentation when settings or lifecycle behavior do not match this guide.

## What belongs where?

The chart deploys and configures services. The **AAS Web UI** is where users browse and work with AAS data. Application behavior, APIs, and security policies are documented under [BaSyx Go components](../basyx_components/go/index.md) and [AAS Web UI](../basyx_components/web_ui/index.md).

If you want to try BaSyx Go without learning Kubernetes yet, the [AAS Environment setup guide](../basyx_components/go/aas_environment/setup.md) provides a Docker Compose alternative.

```{toctree}
:hidden:
:maxdepth: 1

fundamentals
prerequisites
installation
configuration
security
operations
advanced
troubleshooting
```
