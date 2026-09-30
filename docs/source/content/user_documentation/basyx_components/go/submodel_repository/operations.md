# Operation Invocation and Delegation

This walkthrough invokes the delegated-operation example synchronously and asynchronously. The example adds `5` and `3` and returns an output variable named `sum` with value `8`.

The upstream example uses the [AAS Environment](../aas_environment/index), which exposes the same Submodel Repository operation endpoints and delegation behavior. The standalone Submodel Repository uses the same operation invocation implementation.

## Modeled Operation Versus Invocation

An AAS `Operation` Submodel Element models input, output, and in-output variables. Storing that element does not install or execute application code. An invocation is executable only when the Operation has an `invocationDelegation` qualifier whose string value is the HTTP or HTTPS endpoint that implements the behavior.

The Repository loads the stored Operation, forwards the request's input and in-output variables to the delegation endpoint, validates the delegated response, and returns an `OperationResult`. Treat the modeled contract, the Repository invocation API, and the delegated implementation as three distinct concerns.

Delegated invocation supports both the normal `OperationRequest` and `OperationResult` representation and the value-only representation. Use `/invoke/$value` for synchronous value-only invocation, `/invoke-async/$value` for asynchronous value-only invocation, and `/operation-results/{handleId}/$value` to retrieve the completed value-only result. In v1.1.0, both normal and value-only asynchronous invocation requests require a non-empty `clientTimeoutDuration`. A missing or empty value produces `400 Bad Request`.

## Delegation Prerequisite and Trusted Destinations

The example defines `AddNumbersSync` and `AddNumbersAsync` with qualifiers such as:

```json
{
  "type": "invocationDelegation",
  "valueType": "xs:string",
  "value": "http://delegated-operation-service:8080/delegate/add/sync"
}
```

Set `SMREPO_DELEGATION_TRUSTED_HOSTS` to the delegated endpoint's hostname and port and, for DNS names, every resolved IP address and port that BaSyx may connect to. The example uses:

```text
SMREPO_DELEGATION_TRUSTED_HOSTS=delegated-operation-service:8080,172.28.0.10:8080
```

If the service name, port, or Compose network address changes, update the qualifier and allowlist together.

## Start the Example

Clone the BaSyx Go repository and select the source tag that matches the BaSyx images you intend to run:

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
cd basyx-go-components
git checkout RELEASE_TAG
cd examples/BaSyxDelegatedOperationsExample
```

Replace `RELEASE_TAG` with the selected Git release tag. The example's Compose file uses `SNAPSHOT`. Save the following as `compose.release.yml` to select matching stable images instead:

```yaml
services:
  aas_environment:
    image: eclipsebasyx/aasenvironment-go:${BASYX_IMAGE_TAG}
  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:${BASYX_IMAGE_TAG}
```

Set `BASYX_IMAGE_TAG` to the concrete Docker release tag matching the selected source tag. Docker release tags omit the source tag's leading `v`.

Start the database, Configuration Service, AAS Environment, delegated service, and data initializer. The AAS Web UI is optional and is not started:

```bash
export BASYX_IMAGE_TAG=IMAGE_TAG
docker compose -f docker-compose.yml -f compose.release.yml up -d --build \
  db basyx_configuration aas_environment delegated-operation-service data-init
docker compose -f docker-compose.yml -f compose.release.yml logs data-init
docker compose -f docker-compose.yml -f compose.release.yml ps -a data-init
```

Wait for `Delegated operations example data initialized` and an exit code of `0`. The fixture is now available through `http://localhost:8090`. It loads:

- Submodel ID `https://example.com/ids/sm/delegated-operations`;
- encoded path value `aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vZGVsZWdhdGVkLW9wZXJhdGlvbnM`;
- Operations `AddNumbersSync` and `AddNumbersAsync`;
- request body `data/invoke-request-add-5-and-3.json`.

When substituting a different Submodel identifier, encode its UTF-8 bytes with Base64URL for the request path. The example uses the unpadded form. BaSyx Go accepts valid padded and unpadded Base64URL values. See [Using the Submodel Repository](usage.md#retrieve-and-replace-the-submodel) for the identifier-encoding guidance. The example directory in the selected checkout contains the Submodel fixture, invocation request, and delegated service used below.

## Synchronous Invocation

Invoke the synchronous fixture through `/invoke`:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  'http://localhost:8090/submodels/aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vZGVsZWdhdGVkLW9wZXJhdGlvbnM/submodel-elements/AddNumbersSync/invoke' \
  --header 'Content-Type: application/json' \
  --data @data/invoke-request-add-5-and-3.json
```

Expect `200 OK`. The `OperationResult` has `executionState: "Completed"`, `success: true`, and one output argument: the `sum` Property has value `"8"`. This demonstrates `5 + 3 = 8` through synchronous invocation.

## Asynchronous Invocation and Result Retrieval

Submit the same input through `/invoke-async`. Keep automatic redirect following disabled so that the intermediate status and result locations remain visible; in particular, do not add curl's `--location` (`-L`) option.

```bash
curl --include --request POST \
  'http://localhost:8090/submodels/aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vZGVsZWdhdGVkLW9wZXJhdGlvbnM/submodel-elements/AddNumbersAsync/invoke-async' \
  --header 'Content-Type: application/json' \
  --data @data/invoke-request-add-5-and-3.json
```

Expect `202 Accepted` with a `Location` header. Copy that returned location rather than constructing a handle URL, resolve it against `http://localhost:8090` if it is relative, and request it without redirect following:

```bash
curl --include 'http://localhost:8090/<returned operation-status path>'
```

While work is pending, status returns `200 OK` with `executionState` `Running`; repeat the same request. When complete, status returns `302 Found` with another `Location` header pointing to the corresponding `/operation-results/` resource. Copy and fetch that returned result location explicitly:

```bash
curl --include 'http://localhost:8090/<returned operation-results path>'
```

Expect `200 OK`. The completed `OperationResult` again has `executionState: "Completed"`, `success: true`, and output `sum` equal to `"8"`.

Asynchronous operation handles are retained for 15 minutes by default. Configure `SMREPO_DELEGATION_ASYNC_TTL` if clients need a different retention period. Retrieve the status and result before the handle expires.

If the Repository's concurrent asynchronous delegation capacity is exhausted, a new asynchronous invocation returns `429 Too Many Requests`. Retry after an active invocation completes.

These are operation-specific resources. Do not apply Registry bulk assumptions about `204` results, consuming a result on retrieval, or bulk retention to delegated-operation results. See [Asynchronous API Operations](../common/asynchronous_requests) for a comparison with other asynchronous BaSyx APIs.

## Failure Diagnosis

| Symptom | Check |
| --- | --- |
| Invocation is not implemented | Confirm the addressed element is an `Operation` and has a non-empty `invocationDelegation` qualifier. A modeled Operation alone is not executable. |
| Target is reported as untrusted | Ensure `SMREPO_DELEGATION_TRUSTED_HOSTS` contains both the qualifier's hostname and port and its resolved IP address and port. Check that the Compose subnet and static service address still match. |
| Delegated call fails or times out | Check the delegated service logs, container network reachability, and qualifier URL. For asynchronous calls, verify the required `clientTimeoutDuration`. for synchronous calls, check it when supplied. The URL is resolved from inside the Repository container, not from the client host. |
| `404` for a status or result | Use the exact returned location and the same caller identity. Verify the handle belongs to the same Submodel identifier and Operation path and has not expired. |
| Status appears to skip the pending state | Fast work can complete before the first poll. A direct `302` to the returned result location is valid; keep redirect following off to observe it. |
| Result reports delegated failure | Inspect the stored failure body and delegated service logs. `202 Accepted` confirms submission, not successful execution. |

## API and Shared Asynchronous References

- The running service exposes its exact contract at `/swagger` and `/api-docs/openapi.yaml`.
- [Asynchronous API Operations](../common/asynchronous_requests) compares operation resources with Registry bulk jobs.
