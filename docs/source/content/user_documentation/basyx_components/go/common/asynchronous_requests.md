# Asynchronous Requests

An asynchronous request separates submission from execution. `202 Accepted` means the server accepted the work; it does not mean the requested changes succeeded. Keep the returned handle and status location until you have retrieved the final result.

## Follow the Job

1. Submit the request and save its response headers and body.
2. Follow the status URL returned in `Location`. Resolve relative locations against the service URL, preserving its public context path.
3. Inspect the execution state. If the response supplies `Retry-After`, wait that long before polling again.
4. Once processing ends, retrieve the result using that API's result endpoint. Completion can represent success or failure.
5. Check the result status and body before reporting success to your application.

For a Registry bulk job, start with the [AAS Registry](../aas_registry/usage) or [Submodel Registry](../submodel_registry/usage) bulk example to obtain a real handle. Then, replacing `HANDLE_ID` with that handle:

```bash
curl -i http://localhost:8082/bulk/status/HANDLE_ID
```

While running, this returns `200 OK`, `executionState: Running`, and `Retry-After: 2`. After completion it returns `302 Found` with the result location. Retrieve that location explicitly:

```bash
curl -i http://localhost:8082/bulk/result/HANDLE_ID
```

For successful Registry bulk work, expect `204 No Content`. A failed job returns its stored error. Use port `8083` for the Submodel Registry setup and `curl.exe` in PowerShell. Add the configured context path.

Submodel Operation invocation uses a different status/result lifecycle. Follow the locations returned by that API and use the [asynchronous invocation walkthrough](../submodel_repository/operations.md#asynchronous-invocation-and-result-retrieval). Do not carry the bulk example's result-consumption or retention assumptions over to operation results.

## Endpoint Differences

| Behavior | Registry bulk jobs | Submodel Operation invocation |
| --- | --- | --- |
| Status/result routes | `/bulk/status/{handleId}` and `/bulk/result/{handleId}` | Follow the returned locations for `/operation-status/{handleId}` and `/operation-results/{handleId}` below the invoked Submodel Element; see the [operation walkthrough](../submodel_repository/operations.md#asynchronous-invocation-and-result-retrieval). |
| Final result | Successful bulk result is `204`; failure returns the stored error. | Completed result returns the operation payload; a premature result request is rejected. |
| Result retention | Retrieving a completed result consumes the stored job, including a failed result. | Result retrieval does not consume the record in the current implementation. |

Avoid automatic redirect following when inspecting Registry status: it can fetch and consume the result before your application has deliberately saved it. Bulk atomicity and invocation input/output formats remain part of the individual endpoint contract.

## Expiration and Retries

The shared job manager has a default record lifetime of 15 minutes. Handles are temporary and associated with their submitting caller; use the same caller context for polling and retrieval. Do not treat them as permanent operation records.

If a submission times out after reaching the server, submitting again may execute the mutation twice. Retain any received handle, inspect current resource state, and use the operation's documented replacement or conflict behavior before retrying. An unavailable handle alone does not prove the work failed: it may have expired. For Registry bulk jobs, the result might instead have been consumed; retrieving a Submodel Operation result does not consume its record in this release.

Sources: [job manager](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/common/asyncjob/manager.go), [Registry bulk service](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/aasregistry/api/bulk_api_service.go), and [Submodel operation service](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/submodelrepository/api/api_submodel_repository_api_service.go).
