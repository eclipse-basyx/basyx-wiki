# Understanding API Errors

When a request fails, keep its HTTP status, response headers, and response body together. The status identifies the broad failure category; the body usually explains the specific rejected input or failed operation.

## Inspect a Failure

For example, an invalid encoded AAS identifier can be inspected with:

```bash
curl -sS -D response-headers.txt -o response-body.json -w '%{http_code}\n' http://localhost:8084/shells/!
```

Use `curl.exe` in PowerShell. Read both saved files. Without `--fail` or `--fail-with-body`, curl can exit successfully even when the server returns an HTTP error; scripts must check the HTTP status as well as transport failures.

Shared error handling returns message entries with fields such as `messageType`, `text`, `code`, `correlationId`, and `timestamp`. The shared builder uses a JSON array of messages, while endpoint-specific failures may have a different documented shape. Follow the actual response and [Swagger schema](swagger), rather than assuming every error has a `messages` wrapper.

## Decide What to Do Next

| Status | Typical interpretation and next step |
| --- | --- |
| `400 Bad Request` | Check identifier encoding, required fields, parameter values, and the detailed validation message. Correct the input before retrying. |
| `404 Not Found` | Check the base URL, context path, resource identifier, and whether the resource or temporary handle is still available. |
| `409 Conflict` | A create operation may target an existing identifier. Retrieve the resource and choose the documented update operation if replacement is intended. |
| `413 Content Too Large` | Compare the request with configured upload and package limits. |
| `500` / `503` | Inspect server logs and dependency health. Determine whether a mutation was applied before retrying it. |
| `501 Not Implemented` | The route does not provide that operation in this component/version. Use a supported endpoint or component. |

These are common interpretations, not a universal status-code contract. A validation endpoint can return `200` with `valid: false`; an asynchronous submission can return `202` before execution fails. See [Validation](validation) and [Asynchronous Requests](asynchronous_requests).

## Find the Matching Log Entry

Retain the response's request and correlation headers and consult [Observability](observability) for matching logs. The error body's `correlationId` can be a diagnostic identifier constructed from the component and failure location; it is not necessarily the request's tracing identifier. Include the method, URL, time, HTTP status, and diagnostic message when reporting a failure.

Source: [shared error response builder](https://github.com/eclipse-basyx/basyx-go-components/blob/main/internal/common/model/error.go).
