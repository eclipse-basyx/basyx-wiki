# Asynchronous API Operations

BaSyx Go does not provide a generic way to make an arbitrary HTTP request asynchronous. Only specific IDTA API operations and the AAS Environment's asynchronous upload support asynchronous execution. A submission returns a handle and a status location that the client can use to track the work. `202 Accepted` means that the server accepted the work. It does not mean that the operation completed successfully.

```{note}
The [BaSyx Delegated Operations Example](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.3/examples/BaSyxDelegatedOperationsExample) provides a runnable AAS Environment and delegated service, with requests for asynchronous submission, status polling, and result retrieval in normal and ValueOnly form.
```

## Where Asynchronous Operations Are Supported

| Operation | Available through |
| --- | --- |
| AAS Descriptor bulk create, update, and delete | AAS Registry, Digital Twin Registry, and AAS Environment |
| Submodel Descriptor bulk create, update, and delete | Submodel Registry and AAS Environment |
| Asynchronous Operation invocation | Submodel Repository; AAS Repository through AAS-scoped Submodel routes; and AAS Environment through both route forms |
| Asynchronous AASX upload | AASX File Server |
| Asynchronous environment upload | AAS Environment |

The Registry bulk routes implement the IDTA Registry SSP-003 profiles. Asynchronous AASX upload implements the IDTA AASX File Server SSP-002 profile. The AAS Environment's `/upload-async` is a BaSyx extension that follows the same semantics for whole-environment import. Operation invocation is exposed with the IDTA `InvokeOperationAsync`, status, and result operation semantics in the Repository APIs. PostgreSQL persistence, retention periods, caller ownership, restart handling, and execution limits described below are BaSyx Go implementation choices rather than general IDTA requirements.

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

| Behavior | Registry bulk operations | Operation invocation | Asynchronous uploads |
| --- | --- | --- | --- |
| Submission | `POST`, `PUT`, or `DELETE /bulk/shell-descriptors` or `/bulk/submodel-descriptors` | `POST .../submodel-elements/{idShortPath}/invoke-async` or `.../invoke-async/$value` | `POST /packages-async` or `POST /upload-async` with a multipart file |
| Status | `GET /bulk/status/{handleId}` | `GET .../submodel-elements/{idShortPath}/operation-status/{handleId}` | `GET /packages-async/status/{handleId}` or `GET /upload-async/status/{handleId}` |
| Result | `GET /bulk/result/{handleId}` | `GET .../submodel-elements/{idShortPath}/operation-results/{handleId}` or `.../operation-results/{handleId}/$value` | `GET /packages-async/result/{handleId}` or `GET /upload-async/result/{handleId}` |
| Successful result | `204 No Content` | `200 OK` with the normal or ValueOnly Operation result | `200 OK` with a completed `BaseOperationResult` |
| Failed result | `400` Result with one message per submitted item; execution failures return their stored error status | `200 OK` with an `OperationResult` whose `executionState` is `Failed` or `Timeout` | `200 OK` with a failed `BaseOperationResult` |
| Result retrieval consumes the handle | Yes | No | No |
| Default terminal-result retention | 15 minutes, or until the result is retrieved | 15 minutes | 15 minutes |
| Retention configurable | No | Yes, with `SMREPO_DELEGATION_ASYNC_TTL` using a Go duration such as `30m` | No |
| Authorization and ownership | Uses the component's normal security policy; the handle is scoped to the submitting owner | Uses the component's normal security policy; the handle is scoped to the submitting owner | Uses the component's normal security policy; the handle is scoped to the submitting owner |
| Capacity exhausted | Submission returns `429 Too Many Requests` | Submission returns `429 Too Many Requests` | Submission returns `429 Too Many Requests` |

The AAS Repository route adds `/shells/{aasIdentifier}/submodels/{submodelIdentifier}` before the Operation path. The Submodel Repository route starts with `/submodels/{submodelIdentifier}`. AAS Environment exposes both forms.

### Registry Bulk Operations

Registry submissions apply the complete input batch atomically. While a job runs, its status response also supplies `Retry-After: 2`. A successful result is `204 No Content`. If a descriptor operation fails, the result is `400 Bad Request` with an AAS `Result` that contains only `messages`: one `Error` message per submitted item, with the item's status code as `code`, `bulk-item-<index>` as `correlationId`, and the item's index, identifier, and failure reason in `text`. Items rolled back because of another item's failure name that item's index. Execution failures return their stored error status and response.

```bash
curl -i "${BASE_URL}/bulk/status/${HANDLE_ID}"
curl -i "${BASE_URL}/bulk/result/${HANDLE_ID}"
```

```{warning}
Retrieving a terminal Registry bulk result deletes that job record, whether the job succeeded or failed. This consumption behavior is specific to Registry bulk jobs. If an HTTP client automatically follows the `302` returned by the status endpoint, it can retrieve and consume the result before the application deliberately saves it.
```

### Asynchronous Operation Invocation

This API invokes an AAS `Operation` through the configured delegation endpoint. Both the normal and `$value` asynchronous invocation requests require a non-empty `clientTimeoutDuration`. The returned status and result routes remain below the invoked Submodel Element, and the handle is valid only with the same Submodel identifier and `idShortPath`. Use the `$value` result route for a ValueOnly result.

Result retrieval does not delete the handle. Completed and failed records are retained for 15 minutes by default; set `SMREPO_DELEGATION_ASYNC_TTL` to a positive Go duration to change that period.

If the delegated operation fails, both result routes, including `$value`, return `200 OK` with an `OperationResult` whose `success` is `false`. `executionState` is `Timeout` when `clientTimeoutDuration` ran out and `Failed` for every other error. `messages` describe the error, for example the status code returned by the delegation endpoint; the endpoint's body is not forwarded. Check `executionState`, not the HTTP status, to detect a failed invocation. See [Operation failure diagnosis](../submodel_repository/operations.md#failure-diagnosis).

### Asynchronous AASX Upload

`POST /packages-async` durably accepts the uploaded AASX package before processing it. The multipart request requires `file` and may include `aasIds`. The source filename is taken from the file part. A successful or failed result is represented by a `BaseOperationResult`, and reading it does not delete the handle.

When using authenticated access, use the same caller for submission, status, and result requests. The SSP-002 routes are enabled only when the PostgreSQL writer pool has enough capacity for asynchronous processing; the service omits that profile and logs a startup warning if no execution capacity can be reserved.

### Asynchronous Environment Upload

`POST /upload-async` accepts the same multipart request as the AAS Environment's `/upload` and runs the same all-or-nothing import in the background. An unsupported format is rejected with `415 Unsupported Media Type` before an operation is created. A failed result carries the messages that `/upload` returns for the same failure, and nothing from the upload is stored. Reading the result does not delete the handle. See [Import Asynchronously](../aas_environment/usage.md#import-asynchronously).

## BaSyx Implementation Notes

- **Persistence and ownership:** BaSyx stores asynchronous handles and results in PostgreSQL. For authenticated requests, lookups are scoped to an owner derived from the caller's token claims; a different owner receives the same not-found behavior as for an unknown handle. The shared security middleware can also authorize requests without credentials when the ABAC policy permits them. All such requests use the same `anonymous` owner scope, so require authentication in the policy when asynchronous handles must be isolated between callers. The asynchronous upload routes `/packages-async` and `/upload-async` reject unauthenticated requests with `401` whenever runtime security is enabled.
- **Retention:** The retention clock begins when a job becomes terminal, not when it is submitted. Completed and failed records are retained for 15 minutes by default. Only Operation-invocation retention is configurable. Registry results can disappear earlier because result retrieval consumes them.
- **Restart behavior:** Stored terminal results survive a service restart. In-flight work is not resumed after its worker stops; after its lease expires, BaSyx records the abandoned job as failed so that it does not remain `Running` forever.
- **Bounded execution:** Each API family limits concurrent asynchronous work. A submission that cannot acquire capacity returns `429 Too Many Requests`; retry it later rather than treating `202 Accepted` as guaranteed capacity for a second submission.
- **Uncertain retries:** If a client loses the submission response, resubmitting may repeat the mutation. Check for a received handle and inspect current resource state before retrying. A missing handle can mean expiry, caller mismatch, or—only for Registry bulk—a result that was already consumed.

## Detailed Usage Guides

- [AAS Registry bulk operations](../aas_registry/usage.md#bulk-operations)
- [Submodel Registry bulk operations](../submodel_registry/usage.md#bulk-operations)
- [Asynchronous Operation invocation and result retrieval](../submodel_repository/operations.md#asynchronous-invocation-and-result-retrieval)
- [AAS Environment asynchronous upload](../aas_environment/usage.md#import-asynchronously)
- [AASX File Server usage](../aasx_file_server/usage) for package format, upload validation, and limits; the asynchronous endpoint lifecycle is documented above and in the component's Swagger/OpenAPI UI
