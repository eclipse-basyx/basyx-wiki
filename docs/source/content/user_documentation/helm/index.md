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

This section documents only `basyx/basyx` from the [Eclipse BaSyx chart repository](https://eclipse-basyx.github.io/charts/). The installation walkthrough uses chart **3.15.3**, with BaSyx Go **1.1.1**. All component names, values, database requirements, and lifecycle guidance below refer to that Go chart.

Here, `basyx/` before the chart name is the **local Helm repository alias**, not a Kubernetes namespace. Chart version, backend version, Web UI version, and Helm release revision describe different things. See [versions and releases](fundamentals.md#versions-and-releases).

The examples are tied to the published Go chart 3.15.3 rather than to the moving `main` branch. They are a reproducible documentation baseline, not a promise that this is always the newest release. Check available versions and their release notes before selecting another version:

```bash
helm repo add basyx https://eclipse-basyx.github.io/charts
helm repo update
helm search repo basyx/basyx --versions
```

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
