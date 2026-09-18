# Asynchronous API Operations

BaSyx Go does not provide a generic way to make an arbitrary HTTP request asynchronous. Only specific IDTA API operations support asynchronous execution. A submission returns a handle and a status location that the client can use to track the work. `202 Accepted` means that the server accepted the work; it does not mean that the operation completed successfully.

## Where Asynchronous Operations Are Supported

| Operation | Available through |
| --- | --- |
| AAS Descriptor bulk create, update, and delete | AAS Registry, Digital Twin Registry, and AAS Environment |
| Submodel Descriptor bulk create, update, and delete | Submodel Registry and AAS Environment |
| Asynchronous Operation invocation | Submodel Repository; AAS Repository through AAS-scoped Submodel routes; and AAS Environment through both route forms |
| Asynchronous AASX upload | AASX File Server |

The Registry bulk routes implement the IDTA Registry SSP-003 profiles. Asynchronous AASX upload implements the IDTA AASX File Server SSP-002 profile. Operation invocation is exposed with the IDTA `InvokeOperationAsync`, status, and result operation semantics in the Repository APIs. PostgreSQL persistence, retention periods, caller ownership, restart handling, and execution limits described below are BaSyx Go implementation choices rather than general IDTA requirements.

## Common Lifecycle

The endpoint names and result types differ, but the client workflow is the same:

1. Submit an operation and keep the returned handle and `Location` header.
2. Poll the status location using the same caller identity used for submission.
3. While work is active, the status endpoint returns `200 OK` with `executionState` set to `Running`. Honor `Retry-After` when the response provides it.
4. When the job reaches a terminal state, the status endpoint returns `302 Found` and points to the result endpoint.
5. Retrieve and inspect the result. A terminal result can report either success or failure.

```text
submit
  |
  v
202 Accepted + handle/status location
  |
  v
poll status
  |
  +--> 200 Running
  |
  +--> 302 terminal
          |
          v
       retrieve result
```

Resolve relative `Location` values against the service's public base URL and preserve any configured context path. Do not assume that response bodies, failure codes, retention, or result-consumption behavior are interchangeable between API families.

## API-Specific Differences

| Behavior | Registry bulk operations | Operation invocation | AASX asynchronous upload |
| --- | --- | --- | --- |
| Submission | `POST`, `PUT`, or `DELETE /bulk/shell-descriptors` or `/bulk/submodel-descriptors` | `POST .../submodel-elements/{idShortPath}/invoke-async` | `POST /packages-async` with a multipart AASX file |
| Status | `GET /bulk/status/{handleId}` | `GET .../submodel-elements/{idShortPath}/operation-status/{handleId}` | `GET /packages-async/status/{handleId}` |
| Result | `GET /bulk/result/{handleId}` | `GET .../submodel-elements/{idShortPath}/operation-results/{handleId}` | `GET /packages-async/result/{handleId}` |
| Successful result | `204 No Content` | `200 OK` with the Operation result | `200 OK` with a completed `BaseOperationResult` |
| Failed result | Stored failure status and body | Delegated operation's failure status and body, or a BaSyx gateway error | `200 OK` with a failed `BaseOperationResult` |
| Result retrieval consumes the handle | Yes | No | No |
| Default terminal-result retention | 15 minutes, or until the result is retrieved | 15 minutes | 15 minutes |
| Retention configurable | No | Yes, with `SMREPO_DELEGATION_ASYNC_TTL` using a Go duration such as `30m` | No |
| Authentication | Uses the component's normal security policy; the handle belongs to the submitting caller | Uses the component's normal security policy; the handle belongs to the submitting caller | Open when component security is disabled; when ABAC/OIDC security is enabled, every `/packages-async` request requires an authenticated caller |
| Capacity exhausted | Submission returns `429 Too Many Requests` | Submission returns `429 Too Many Requests` | Submission returns `429 Too Many Requests` |

The AAS Repository route adds `/shells/{aasIdentifier}/submodels/{submodelIdentifier}` before the Operation path. The Submodel Repository route starts with `/submodels/{submodelIdentifier}`. AAS Environment exposes both forms.

### Registry Bulk Operations

Registry submissions apply the complete input batch atomically. While a job runs, its status response also supplies `Retry-After: 2`. A successful result is `204 No Content`; a failed result returns the stored error response.

```bash
curl -i "${BASE_URL}/bulk/status/${HANDLE_ID}"
curl -i "${BASE_URL}/bulk/result/${HANDLE_ID}"
```

```{warning}
Retrieving a terminal Registry bulk result deletes that job record, whether the job succeeded or failed. This consumption behavior is specific to Registry bulk jobs. If an HTTP client automatically follows the `302` returned by the status endpoint, it can retrieve and consume the result before the application deliberately saves it.
```

### Asynchronous Operation Invocation

This API invokes an AAS `Operation` through the configured delegation endpoint. `clientTimeoutDuration` is required for asynchronous invocation. The returned status and result routes remain below the invoked Submodel Element, and the handle is valid only with the same Submodel identifier and `idShortPath`.

Result retrieval does not delete the handle. Completed and failed records are retained for 15 minutes by default; set `SMREPO_DELEGATION_ASYNC_TTL` to a positive Go duration to change that period. In the stable release, delegated asynchronous invocation through the `$value` representation is not supported.

### Asynchronous AASX Upload

`POST /packages-async` durably accepts the uploaded AASX package before processing it. The multipart request requires `file` and may include `aasIds`; the source filename is taken from the file part. A successful or failed result is represented by a `BaseOperationResult`, and reading it does not delete the handle.

When AASX File Server security is enabled, submission, status, and result requests require a verified bearer token. Use the same authenticated caller for all three steps. The SSP-002 routes are enabled only when the PostgreSQL writer pool has enough capacity for asynchronous processing; the service omits that profile and logs a startup warning if no execution capacity can be reserved.

## BaSyx Implementation Notes

- **Persistence and ownership:** BaSyx stores asynchronous handles and results in PostgreSQL. Lookups are scoped to the caller that submitted the work; another caller receives the same not-found behavior as for an unknown handle.
- **Retention:** The retention clock begins when a job becomes terminal, not when it is submitted. Completed and failed records are retained for 15 minutes by default. Only Operation-invocation retention is configurable in this release. Registry results can disappear earlier because result retrieval consumes them.
- **Restart behavior:** Stored terminal results survive a service restart. In-flight work is not resumed after its worker stops; after its lease expires, BaSyx records the abandoned job as failed so that it does not remain `Running` forever.
- **Bounded execution:** Each API family limits concurrent asynchronous work. A submission that cannot acquire capacity returns `429 Too Many Requests`; retry it later rather than treating `202 Accepted` as guaranteed capacity for a second submission.
- **Uncertain retries:** If a client loses the submission response, resubmitting may repeat the mutation. Check for a received handle and inspect current resource state before retrying. A missing handle can mean expiry, caller mismatch, or—only for Registry bulk—a result that was already consumed.

## Detailed Usage Guides

- [AAS Registry bulk operations](../aas_registry/usage.md#bulk-operations)
- [Submodel Registry bulk operations](../submodel_registry/usage.md#bulk-operations)
- [Asynchronous Operation invocation and result retrieval](../submodel_repository/operations.md#asynchronous-invocation-and-result-retrieval)
- [AASX File Server usage](../aasx_file_server/usage) for package format, upload validation, and limits; the asynchronous endpoint lifecycle is documented above and in the component's Swagger/OpenAPI UI

Implementation references: [shared asynchronous job manager](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/internal/common/asyncjob/manager.go), [AAS Registry bulk service](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/internal/aasregistry/api/bulk_api_service.go), [Submodel Repository operation service](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/internal/submodelrepository/api/api_submodel_repository_api_service.go), and [AASX File Server service](https://github.com/eclipse-basyx/basyx-go-components/blob/v1.0.12/internal/aasxfileserver/api/api_aasx_file_server_api_service.go).
