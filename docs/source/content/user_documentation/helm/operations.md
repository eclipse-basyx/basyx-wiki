# Operate and Upgrade BaSyx

This page applies to the Go chart. Reuse the release name, namespace, values, and explicit Kubernetes context from your installation. Examples use release `basyx`, namespace `basyx-evaluation`, and a shell variable `BASYX_CONTEXT` set to your real context.

## Inspect an installation

```bash
helm --kube-context "$BASYX_CONTEXT" -n basyx-evaluation list
helm --kube-context "$BASYX_CONTEXT" -n basyx-evaluation status basyx
helm --kube-context "$BASYX_CONTEXT" -n basyx-evaluation history basyx
helm --kube-context "$BASYX_CONTEXT" -n basyx-evaluation get values basyx
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get pods,jobs,pvc
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get clusters.postgresql.cnpg.io
```

`helm get values` without `--all` shows stored overrides; `--all` includes computed defaults. Values and manifests can contain credentials, so review them before attaching output to an issue.

Inspect a runtime and the initializer separately:

```bash
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation logs \
  deployment/basyx-aas-environment --all-containers --tail=100
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation logs \
  job/basyx-configuration --all-containers --tail=100
```

Finished hook Jobs may have been cleaned up by their TTL. Store operational logs outside pods if you need them after cleanup.

## Plan a database-aware upgrade

Changing chart versions can change Go images and run schema migrations. Follow the [Go deployment contract](../basyx_components/go/common/deployment.md) and [Configuration Service operations](../basyx_components/go/configuration_service/operations.md).

1. Read the target chart/application release notes and compare old and new defaults. A small chart version change can still affect images or application behavior.
2. Test the target release and your overlays in a separate environment with representative data.
3. Stop database writers and take a tested, recoverable backup before a schema-changing upgrade. Writer coordination belongs in your maintenance procedure; the Helm migration hook does not automatically stop every old writer or external client.
4. Render and review the target manifests. Keep runtime images and Configuration Service compatible with the database.
5. Apply the upgrade, require successful migration, and verify application readiness and user-visible behavior before resuming writers.

For a reviewed values-only update, restore `BASYX_CHART_VERSION` to the **already installed** chart version from your deployment records or `helm list` before running these commands. Do not automatically select the newest release for routine configuration changes:

```bash
helm template basyx basyx/basyx \
  --version "${BASYX_CHART_VERSION:?Set the installed chart version first}" --namespace basyx-evaluation \
  -f values.cluster-base.yaml -f values.cluster.yaml > rendered-upgrade.yaml

helm upgrade basyx basyx/basyx \
  --version "${BASYX_CHART_VERSION:?Set the installed chart version first}" \
  --kube-context "$BASYX_CONTEXT" --namespace basyx-evaluation \
  -f values.cluster-base.yaml -f values.cluster.yaml --timeout 15m
```

These commands retain both files from the installation walkthrough, in the same order. For a version upgrade, save the previous version and values for recovery, then set `BASYX_CHART_VERSION` to the reviewed target version. Download its base profile into a separate file using the {ref}`version-matched download <prepare-the-values-files>`, compare it with the existing base, and review the selected release's README upgrade notes before replacing your deployment files. Render and apply using that same target version and the reviewed overlays. Avoid silently carrying obsolete settings forward with `--reuse-values`.

The Configuration Service uses a `pre-upgrade` hook. Do not disable that hook just to make an upgrade appear successful. A failed or unclean schema requires investigation before starting incompatible runtimes.

## Backups and recovery

Application state belongs to PostgreSQL. Restarting application pods does not create a backup, and copying a values file does not copy the database.

For managed PostgreSQL, use a backup/restore process supported by your CloudNativePG deployment. For external PostgreSQL, coordinate with its operator. Include database data, Large Objects where used, and the necessary keys and secret-management recovery procedures. Validate restoration to a separate environment before relying on it for production recovery.

See [CloudNativePG backup](https://cloudnative-pg.io/documentation/current/backup/) and [recovery](https://cloudnative-pg.io/documentation/current/recovery/), selecting the documentation matching your operator version.

## Helm rollback is not database rollback

`helm rollback` can restore a previous release's Kubernetes configuration. It does not reverse Configuration Service migrations or restore deleted data. Starting older images against a newer schema may fail compatibility checks.

For configuration-only regressions with an unchanged compatible schema, a reviewed Helm rollback may be appropriate. For database-changing releases, use the tested recovery procedure and restore compatible database state before running the older application set. Do not assume `--atomic` makes database changes reversible.

## Remove an installation

Confirm the context, release, namespace, and data-retention plan before removing an installation:

```bash
helm --kube-context "$BASYX_CONTEXT" -n basyx-evaluation uninstall basyx
kubectl --context "$BASYX_CONTEXT" -n basyx-evaluation get pvc,secrets
```

Uninstalling removes release-managed resources. The outcome for operator-managed storage depends on ownership and retention settings. Inventory and back up the actual data first; neither “all data is deleted” nor “all data is preserved” is a safe universal assumption.

Do not remove shared CloudNativePG/cert-manager operators, CRDs, namespaces, PVCs, or Secrets as routine cleanup for one application release. Such removals can affect unrelated installations or destroy data.
