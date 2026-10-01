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

Common approaches include:

- Running the Job as part of a deployment pipeline before applying BaSyx service manifests.
- Using lifecycle-appropriate Helm hooks. The official BaSyx chart uses `post-install` for fresh installations, after its PostgreSQL resources have been created, and `pre-upgrade` before release resources are updated. By default, its Configuration Service Job also uses an init container to wait for PostgreSQL readiness. A `pre-install` hook can still be appropriate when PostgreSQL is managed independently and is already available.
- Using an init container or external deployment controller to wait for the Job completion before starting dependent services.

## Operational Notes

- Use `restartPolicy: OnFailure` so a failed Configuration Service container can be restarted within the same Job Pod.
- Use `backoffLimit` to limit retries before Kubernetes marks the Job as failed.
- Store database credentials in a Kubernetes `Secret` instead of plain environment variables.
- Use the same BaSyx version or build for `basyxconfigurationservice` and the runtime services.
- Avoid mutable image tags such as `latest` and `SNAPSHOT` for reproducible deployments. Pin exact image versions or image digests where possible.
- If mutable-tag images are pulled fresh on restart, run the Configuration Service Job before DB-backed runtime workloads.
- Ensure PostgreSQL is reachable and ready before the Job runs.
- Include the Job's pool in the PostgreSQL connection budget while it overlaps with existing workloads during installation or upgrades. Each runtime pod has a separate pool.
- Check Job logs when initialization fails; errors include BaSyx error codes for troubleshooting.
