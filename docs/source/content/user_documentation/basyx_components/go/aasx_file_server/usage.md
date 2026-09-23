# Using the AASX File Server

This walkthrough uploads, lists, downloads, replaces, and deletes an AASX package through the synchronous Package File Server API.

## Before You Start

Start the [Compose setup](setup), check the service, and place a valid package named `example.aasx` in your working directory:

```bash
curl -i http://localhost:8087/health
```

Continue after HTTP `200`. The examples use an empty context path and the unsecured local setup. In Windows PowerShell, use `curl.exe` instead of the `curl` alias.

## Upload a Package

```bash
curl -i -X POST http://localhost:8087/packages -F 'file=@example.aasx;type=application/asset-administration-shell-package' -F 'fileName=example.aasx' -F 'aasIds=urn:example:aas:1'
```

Expect `201 Created`. Copy the `packageId` from the JSON response or the package identifier from the `Location` header. The returned value is already Base64URL-encoded for use in `/packages/{packageId}`; do not encode it again.

`file` is required. `fileName` and `aasIds` are optional. Repeat `aasIds` or provide comma-separated values to associate several AAS identifiers. These identifiers are caller-supplied metadata: the File Server does not discover them by importing the AASX contents into Repository storage.

## List Packages

```bash
curl -i -G http://localhost:8087/packages --data-urlencode 'limit=10'
```

The response contains package descriptors in `result` and pagination information in `paging_metadata`. Follow a returned `cursor` to obtain the next page.

To filter by the AAS identifier supplied during upload, pass its Base64URL representation. For `urn:example:aas:1`:

```bash
curl -i -G http://localhost:8087/packages --data-urlencode 'aasId=dXJuOmV4YW1wbGU6YWFzOjE'
```

## Download the Package

Replace `RETURNED_PACKAGE_ID` with the encoded identifier returned by the upload:

```bash
curl -D response-headers.txt -o downloaded.aasx http://localhost:8087/packages/RETURNED_PACKAGE_ID
```

The file response includes its stored name in the `X-FileName` header. HTTP headers are written to `response-headers.txt`, while the package bytes are written to `downloaded.aasx`.

## Replace the Package

Place a valid replacement package named `replacement.aasx` in the working directory, then send a complete multipart replacement:

```bash
curl -i -X PUT http://localhost:8087/packages/RETURNED_PACKAGE_ID -F 'file=@replacement.aasx;type=application/asset-administration-shell-package' -F 'fileName=replacement.aasx' -F 'aasIds=urn:example:aas:1'
```

Expect `204 No Content` for an existing package. PUT creates a missing package with `201 Created`. Replacement changes the stored file, file name, and AAS associations together; include every association that should remain.

## Delete the Package

```bash
curl -i -X DELETE http://localhost:8087/packages/RETURNED_PACKAGE_ID
curl -i http://localhost:8087/packages/RETURNED_PACKAGE_ID
```

The DELETE returns `204 No Content`; the following GET returns `404 Not Found`.

## Upload Validation and Limits

The server validates that an upload is an AASX package and rejects ambiguous JSON/XML specification parts. With the release defaults, the compressed request is limited to 128 MiB, the complete expanded package to 512 MiB, each expanded part to 128 MiB, OPC metadata and thumbnails to 16 MiB each, and the package to 10,000 parts. Invalid packages return a client error; uploads exceeding configured limits can return `413 Payload Too Large`. Adjust limits through the verified settings in [Setup](setup), not through web-server assumptions.

For secured deployments, add a valid bearer token and ensure its subject has permission for the package operation. Uploading or replacing a package here does not populate the AAS Repository, Submodel Repository, or AAS Environment.
