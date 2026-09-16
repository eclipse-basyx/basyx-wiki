# Operation Invocation and Delegation

This guide runs the release 1.0.11 delegated-operation fixture through both invocation modes. The same inputs, `5` and `3`, produce an output variable named `sum` with value `8`.

## Modeled Operation Versus Invocation

An AAS `Operation` Submodel Element models input, output, and in-output variables. Storing that element does not install or execute application code. For BaSyx Go 1.0.11, an invocation is executable only when the Operation has an `invocationDelegation` qualifier whose string value is the HTTP or HTTPS endpoint that implements the behavior.

The Repository loads the stored Operation, forwards the request's input and in-output variables to the delegation endpoint, validates the delegated response, and returns an `OperationResult`. Treat the modeled contract, the Repository invocation API, and the delegated implementation as three distinct concerns.

## Delegation Prerequisite and Trusted Destinations

The release fixture defines `AddNumbersSync` and `AddNumbersAsync` with qualifiers such as:

```json
{
  "type": "invocationDelegation",
  "valueType": "xs:string",
  "value": "http://delegated-operation-service:8080/delegate/add/sync"
}
```

Delegation sends requests from the Repository runtime to an endpoint named by stored model data. Restrict that server-side request boundary with `SMREPO_DELEGATION_TRUSTED_HOSTS`. For a DNS name, the allowlist must cover **both** the original service hostname and port **and** every resolved IP address and port that may be selected. The fixture therefore uses:

```text
SMREPO_DELEGATION_TRUSTED_HOSTS=delegated-operation-service:8080,172.28.0.10:8080
```

BaSyx first checks `delegated-operation-service:8080`, resolves it, then checks the resolved address such as `172.28.0.10:8080` before dialing that address. Checking both authorities limits DNS-rebinding and name-to-address substitution: trusting only the hostname, or only its current IP, is insufficient. If you change the Compose subnet, static service address, service name, or port, update the qualifier and both allowlist entries together. Do not broadly trust destinations merely to make an invocation succeed.

## Start the Release-Matched Example

Clone and select the release fixture. The `v1.0.11` tag resolves to commit `81324eb3aad9d63baea93d3385bc9ca7e6a6a05a`:

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components
cd basyx-go-components
git checkout v1.0.11
cd examples/BaSyxDelegatedOperationsExample
```

The pinned example's Compose file uses moving `SNAPSHOT` tags. Do not inherit those tags silently. Save the following as `compose.release.yml`; override only the two BaSyx services needed by this API walkthrough:

```yaml
services:
  aas_environment:
    image: eclipsebasyx/aasenvironment-go:1.0.11
  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:1.0.11
```

Start the database, Configuration Service, AAS Environment, delegated service, and data initializer. The AAS Web UI is optional and is not started:

```bash
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

See [Encode Your Own Identifier](../common/encoding.md#encode-your-own-identifier) when substituting a different Submodel identifier. The exact release assets are the pinned [example directory](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxDelegatedOperationsExample), [Submodel fixture](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxDelegatedOperationsExample/data/submodel-delegated-operations.json), and [invocation request](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/examples/BaSyxDelegatedOperationsExample/data/invoke-request-add-5-and-3.json).

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

These are operation-specific resources. Do not apply Registry bulk assumptions about `204` results, consuming a result on retrieval, or bulk retention to delegated-operation results. See [Asynchronous Requests](../common/asynchronous_requests) for the cross-component comparison.

## Failure Diagnosis

| Symptom | Check |
| --- | --- |
| Invocation is not implemented | Confirm the addressed element is an `Operation` and has a non-empty `invocationDelegation` qualifier. A modeled Operation alone is not executable. |
| Target is reported as untrusted | Ensure `SMREPO_DELEGATION_TRUSTED_HOSTS` contains both the qualifier's hostname and port and its resolved IP address and port. Check that the Compose subnet and static service address still match. |
| Delegated call fails or times out | Check the delegated service logs, container network reachability, qualifier URL, and `clientTimeoutDuration` in the request. The URL is resolved from inside the Repository container, not from the client host. |
| `404` for a status or result | Use the exact returned location and the same caller identity. Verify the handle belongs to the same Submodel identifier and Operation path and has not expired. |
| Status appears to skip the pending state | Fast work can complete before the first poll. A direct `302` to the returned result location is valid; keep redirect following off to observe it. |
| Result reports delegated failure | Inspect the stored failure body and delegated service logs. `202 Accepted` confirms submission, not successful execution. |

For general response diagnosis, see [API Errors](../common/api_errors).

## API and Shared Asynchronous References

- The running service exposes its exact contract at `/swagger` and `/api-docs/openapi.yaml`.
- [Asynchronous Requests](../common/asynchronous_requests) compares operation resources with Registry bulk jobs.
- The release-pinned [delegation implementation](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/submodelrepository/api/operation_delegation.go), [destination guard](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/submodelrepository/api/operation_delegation_security.go), and [integration test](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/submodelrepository/integration_tests/delegation_operation_integration_test.go) define the 1.0.11 behavior documented here.
