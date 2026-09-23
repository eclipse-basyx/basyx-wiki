# Kubernetes Job Integration

The BaSyx Configuration Service can be run as a Kubernetes `Job`. This fits the service model well because the service runs once, prepares the database, and exits after successful initialization.

Use a Kubernetes Job when BaSyx services run in a Kubernetes cluster and the PostgreSQL database must be initialized or patched before application pods start.

## Barebone Job Example

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: basyx-configuration
spec:
  backoffLimit: 3
  template:
    metadata:
      labels:
        app: basyx-configuration
    spec:
      restartPolicy: OnFailure
      containers:
        - name: basyx-configuration
          image: eclipsebasyx/basyxconfigurationservice-go:latest
          env:
            - name: POSTGRES_HOST
              value: postgres
            - name: POSTGRES_PORT
              value: "5432"
            - name: POSTGRES_USER
              value: admin
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: POSTGRES_DBNAME
              value: basyx
            - name: POSTGRES_MAXOPENCONNECTIONS
              value: "50"
            - name: POSTGRES_MAXIDLECONNECTIONS
              value: "25"
            - name: POSTGRES_CONNMAXLIFETIMEMINUTES
              value: "5"
            - name: POSTGRES_CONNMAXIDLETIMEMINUTES
              value: "0"
```

## Secret Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
stringData:
  password: admin123
```

## Startup Recommendation

Regular BaSyx workloads should start only after the Configuration Service Job completed successfully.

```{warning}
Job or hook completion orders new workloads; it is not proof that old workloads have stopped accessing the database. Before migrating an existing database, explicitly establish any required quiescence, make the required backup, and follow [Upgrading an existing database](operations.md#upgrading-an-existing-database).
```

Common approaches include:

- Running the Job as part of a deployment pipeline before applying BaSyx service manifests.
- Using Helm hooks to run the Job before installing or upgrading BaSyx services.
- Using an init container or external deployment controller to wait for the Job completion before starting dependent services.

## Operational Notes

- Use `restartPolicy: OnFailure` so Kubernetes retries the pod if initialization fails.
- Use `backoffLimit` to control how many retries Kubernetes should attempt.
- Store database credentials in a Kubernetes `Secret` instead of plain environment variables.
- Use the same image tag for `basyxconfigurationservice` and the runtime services that share its database. The example uses `latest`.
- Pin a concrete release tag or image digest when an immutable deployment is required.
- Ensure PostgreSQL is reachable and ready before the Job runs.
- Include the Job's pool in the PostgreSQL connection budget while it overlaps with existing workloads during installation or upgrades. Each runtime pod has a separate pool.
- Check Job logs when initialization fails; errors include BaSyx error codes for troubleshooting.

For the shared release, image, and persistent-state contract, see [Deployment, Versions, and Persistent State](../common/deployment.md).
