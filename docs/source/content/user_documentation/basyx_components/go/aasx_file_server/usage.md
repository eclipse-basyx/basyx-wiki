# Using the AASX File Server

This walkthrough uploads, lists, downloads, replaces, and deletes an AASX package and then demonstrates the asynchronous upload workflow.

## Before You Start

Start the [Compose setup](setup), check the service, and place a valid package named `example.aasx` in your working directory:

```bash
curl -i http://localhost:8087/health
```

Continue after HTTP `200`. The examples use an empty context path and the unsecured local setup. In Windows PowerShell, use `curl.exe` instead of the `curl` alias.

## Upload a Package

```bash
curl -i -X POST http://localhost:8087/packages -F 'file=@example.aasx;type=application/asset-administration-shell-package' -F 'aasIds=urn:example:aas:1'
```

Expect `201 Created`. The JSON response is a package description containing only `packageId` and `aasIds`, both as plain identifiers. The `Location` header contains the package path with the unpadded Base64URL-encoded package identifier; use it for `/packages/{packageId}` requests, or Base64URL-encode the returned `packageId` yourself.

`file` is required and `aasIds` is optional. The stored file name is the `filename` parameter of the `file` part's `Content-Disposition` header, which curl sets from the uploaded file; only its base filename is stored. A separate `fileName` form field is ignored.

Supply plain, unencoded AAS identifiers in `aasIds`. Each `aasIds` part carries exactly one identifier, so a comma is part of the identifier; repeat the part to associate several identifiers. Surrounding whitespace and empty values are ignored, and duplicate identifiers are stored once. These identifiers are caller-supplied metadata: the File Server does not discover them by importing the AASX contents into Repository storage.

## List Packages

```bash
curl -i -G http://localhost:8087/packages --data-urlencode 'limit=10'
```

The response contains package descriptions in `result` and pagination information in `paging_metadata`. Page sizes follow `server.pagination.defaultLimit` (default `100`) and `server.pagination.maxLimit` (default `1000`). A non-positive or excessive `limit` returns `400 Bad Request`. If `paging_metadata.cursor` is present, treat it as opaque and pass it unchanged in the next request:

```bash
curl -i -G http://localhost:8087/packages --data-urlencode 'limit=10' --data-urlencode 'cursor=RETURNED_CURSOR'
```

To filter by an AAS identifier supplied during upload, pass its Base64URL representation. For `urn:example:aas:1`:

```bash
curl -i -G http://localhost:8087/packages --data-urlencode 'aasId=dXJuOmV4YW1wbGU6YWFzOjE'
```

## Download the Package

Replace `RETURNED_PACKAGE_ID` with the encoded package identifier from the upload's `Location` header:

```bash
curl -D response-headers.txt -o downloaded.aasx http://localhost:8087/packages/RETURNED_PACKAGE_ID
```

The response has the Content-Type `application/asset-administration-shell-package`, whether the package contains a JSON or XML environment, and includes its stored name in the `X-FileName` header. HTTP headers are written to `response-headers.txt`, while the package bytes are written to `downloaded.aasx`.

## Replace the Package

Place a valid replacement package named `replacement.aasx` in the working directory, then send a complete multipart replacement:

```bash
curl -i -X PUT http://localhost:8087/packages/RETURNED_PACKAGE_ID -F 'file=@replacement.aasx;type=application/asset-administration-shell-package' -F 'aasIds=urn:example:aas:1'
```

Expect `204 No Content` for an existing package. PUT creates a missing package with `201 Created`. Replacement changes the stored file, file name, and AAS associations together; include every association that should remain.

In secured deployments, authorization follows the operation that `PUT` actually performs: creating a missing package requires create permission, while replacing an existing package requires update permission.

## Delete the Package

```bash
curl -i -X DELETE http://localhost:8087/packages/RETURNED_PACKAGE_ID
curl -i http://localhost:8087/packages/RETURNED_PACKAGE_ID
```

The DELETE returns `204 No Content`; the following GET returns `404 Not Found`.

## Upload a Package Asynchronously

Asynchronous upload implements the SSP-002 profile. Confirm that the running service advertises it before submitting work:

```bash
curl -i http://localhost:8087/description
```

The `profiles` array always contains SSP-001 and contains SSP-002 when the asynchronous routes are enabled.

```{note}
The local Compose setup has access control disabled, so it accepts these asynchronous requests anonymously. When ABAC/OIDC security is enabled, add a valid bearer token to the submission, status, and result requests and use the same authenticated identity for all three. Handles are scoped to that identity; another caller receives `404 Not Found`.
```

Submit the package:

```bash
curl -i -X POST http://localhost:8087/packages-async -F 'file=@example.aasx;type=application/asset-administration-shell-package' -F 'aasIds=urn:example:aas:async'
```

Expect `202 Accepted`, an `OperationHandle` JSON body containing `handleId`, and a `Location` header pointing to `/packages-async/status/{handleId}`. Use the encoded handle path from `Location`; do not place the raw JSON `handleId` into the path without Base64URL-encoding it. As with synchronous uploads, the stored file name comes from the `file` part's `Content-Disposition` filename.

If the service has no free asynchronous execution capacity, submission returns `429 Too Many Requests`; retry later. `202 Accepted` means that the upload was accepted for processing, not that package validation and storage have completed.

Poll the status URL returned in `Location`:

```bash
curl -i http://localhost:8087/packages-async/status/ENCODED_HANDLE_ID
```

While processing continues, the endpoint returns `200 OK` with a `BaseOperationResult` whose `executionState` is `Running`. At a terminal state it returns `302 Found`; use that response's `Location` header to retrieve the result:

```bash
curl -i http://localhost:8087/packages-async/result/ENCODED_HANDLE_ID
```

The result endpoint returns `200 OK` with a completed or failed `BaseOperationResult`. It reports the operation outcome rather than a package description. After a successful result, list the packages to obtain the new `packageId` and Base64URL-encode it for `/packages/{packageId}` requests. Reading the result does not delete the handle. See [Asynchronous API Operations](../common/asynchronous_requests) for the shared lifecycle and retention behavior.

## Upload Validation and Limits

The server validates that an upload is an AASX package and rejects ambiguous JSON/XML specification parts.

With the release defaults, uploaded file content is limited to 128 MiB, the complete expanded package to 512 MiB, each expanded part to 128 MiB, OPC metadata and thumbnails to 16 MiB each, and the package to 10,000 parts. Invalid packages return a client error; uploads exceeding configured limits can return `413 Payload Too Large`. Adjust limits through the verified settings in [Setup](setup), not through web-server assumptions.

For secured deployments, add a valid bearer token and ensure its subject has permission for the package operation. Uploading or replacing a package here does not populate the AAS Repository, Submodel Repository, or AAS Environment.
