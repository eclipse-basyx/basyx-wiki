# Supply Chain Security

BaSyx Go container images are published with supply-chain metadata that helps users verify where an image came from, how it was built, and which software components it contains.

Use this page when you need to:

- Deploy BaSyx Go images by immutable digest.
- Verify that a release or snapshot image was signed by the expected Eclipse BaSyx GitHub Actions workflow.
- Inspect or archive provenance and SBOM evidence.
- Understand the release artifacts attached to GitHub Releases.

For the general concepts behind these checks, see the [BaSyx supply chain security overview](../supply_chain_security.md).

## What Is Produced

For each BaSyx Go service image, the release pipeline produces:

- Multi-architecture OCI images published to Docker Hub.
- Sigstore Cosign keyless signatures on immutable image digests.
- BuildKit OCI attestations for provenance and SBOM data.
- Cosign-signed provenance attestations.
- Cosign-signed SBOM attestations using the SPDX predicate type.
- Exported release SBOM assets in SPDX JSON and CycloneDX JSON formats.
- Per-service metadata JSON.
- A release supply-chain manifest JSON.
- OCI image labels for traceability, including source repository, commit SHA, and version.

The pipeline also verifies the Syft installer by using Cosign-signed checksum manifests before generating exported SBOM files.

## Supported Images

The same verification model applies to BaSyx Go service images such as:

- `eclipsebasyx/aasregistry-go`
- `eclipsebasyx/submodelregistry-go`
- `eclipsebasyx/digitaltwinregistry-go`
- `eclipsebasyx/submodelrepository-go`
- Additional BaSyx Go service images published by the `basyx-go-components` repository.

Replace the image name in the examples below with the service image you deploy.

## Trust Model

BaSyx Go images are signed by GitHub Actions keyless identity for the `eclipse-basyx/basyx-go-components` repository. Verification should check both the certificate identity and the OIDC issuer.

Expected certificate identity for releases:

```text
https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-release.yml@refs/tags/<tag>
```

Expected certificate identity for snapshots:

```text
https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-snapshot.yml@refs/heads/main
```

Expected OIDC issuer:

```text
https://token.actions.githubusercontent.com
```

```{important}
Verify by digest, not by tag. A tag such as `latest` or `v1.2.3` can be moved by a registry operation. A digest reference such as `image@sha256:<digest>` identifies the exact image that was signed.
```

## Verify Image Signatures

Install [Cosign](https://docs.sigstore.dev/cosign/installation/) and verify the immutable image digest.

```bash
IMAGE="eclipsebasyx/aasregistry-go@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-release.yml@refs/tags/<tag>"

cosign verify \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

For snapshots, use the snapshot workflow identity:

```bash
IDENTITY="https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-snapshot.yml@refs/heads/main"
```

Successful verification means the digest was signed by the expected GitHub Actions workflow identity. It does not mean the image is free of vulnerabilities or suitable for every deployment context.

## Verify Provenance Attestations

The release workflow creates explicit Cosign provenance attestations from BuildKit provenance data and verifies them with identity constraints.

Use the provenance predicate type that appears in the BuildKit output. Common values are:

- `https://slsa.dev/provenance/v1`
- `https://slsa.dev/provenance/v0.2`

```bash
IMAGE="eclipsebasyx/aasregistry-go@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-release.yml@refs/tags/<tag>"
PROVENANCE_TYPE="https://slsa.dev/provenance/v1"

cosign verify-attestation \
  --type "$PROVENANCE_TYPE" \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

Provenance is useful when you need evidence about the repository, workflow, and source revision used to build the image.

## Verify SBOM Attestations

The workflow also creates explicit Cosign SBOM attestations from BuildKit SBOM data.

```bash
IMAGE="eclipsebasyx/aasregistry-go@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-go-components/.github/workflows/docker-release.yml@refs/tags/<tag>"

cosign verify-attestation \
  --type "https://spdx.dev/Document" \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

SBOM attestations are useful for automated checks. Downloadable SBOM files from GitHub Releases are useful for audit records and downstream vulnerability management.

## Verify BuildKit OCI Attestations Exist

The workflow attaches provenance and SBOM as BuildKit OCI attestations to the OCI image index.

```bash
IMAGE="eclipsebasyx/aasregistry-go@sha256:<digest>"

docker buildx imagetools inspect "$IMAGE" --raw | jq \
  '.manifests[] | select(.annotations["vnd.docker.reference.type"] == "attestation-manifest")'
```

If this command returns attestation manifests, the OCI index has attached BuildKit attestations.

You can inspect BuildKit provenance and SBOM content with:

```bash
IMAGE="eclipsebasyx/aasregistry-go@sha256:<digest>"

docker buildx imagetools inspect "$IMAGE" --format '{{ json (index .Provenance "linux/amd64").SLSA }}' | jq .
docker buildx imagetools inspect "$IMAGE" --format '{{ json (index .SBOM "linux/amd64").SPDX }}' | jq .
```

If your Docker or Buildx version does not expose per-platform maps, try:

```bash
docker buildx imagetools inspect "$IMAGE" --format '{{ json .Provenance.SLSA }}' | jq .
docker buildx imagetools inspect "$IMAGE" --format '{{ json .SBOM.SPDX }}' | jq .
```

## Retrieve Release SBOM Assets

GitHub Releases include per-service exported SBOM files:

- `service-version.spdx.json`
- `service-version.cdx.json`

The release may also include per-service metadata JSON and a release supply-chain manifest JSON. Store these files with your deployment records if your organization needs audit evidence.

## Versioning and Tagging Implications

Release workflows parse the semantic version from the Git tag.

- Stable releases receive `major.minor.patch`, `major.minor`, `major`, and `latest` tags.
- Pre-releases keep explicit pre-release tags only.
- Metadata labels include the source repository, commit SHA, and version.
- Signatures and attestations are anchored to the immutable digest, not to the tag.

For production, prefer release tags and digest-pinned deployments. Snapshot artifacts remain non-stable by definition and are better suited for testing.

## Vulnerability Scanning

The repository provides a report-only Trivy workflow for continuous visibility.

- Repository filesystem scans cover source and dependency manifests.
- Container image scans build and scan service images on scheduled runs.
- Findings are uploaded as SARIF when permitted.
- The current mode does not fail builds.

Downstream users should still scan the exact image digest they deploy. Vulnerability impact depends on the deployment configuration, exposed interfaces, reachable code paths, and available mitigations.

## Migration Guidance

If you currently deploy by mutable tag:

1. Resolve the tag to a digest.
2. Update deployment manifests to use `image@sha256:<digest>`.
3. Verify the image signature with the expected workflow identity.
4. Download or archive release SBOM assets when compliance evidence is required.
5. Adjust automation that consumes release assets to match the current per-service SBOM file names.

## Current SLSA Posture

The BaSyx Go release model aligns with common SLSA build-integrity practices:

- GitHub Actions OIDC-based signing identity.
- Immutable digest-first signing.
- Provenance attestation and verification in CI.
- SBOM generation and signed SBOM attestations.
- Least-privilege workflow permissions.
- Immutable action pinning in workflows.

This posture improves traceability and tamper evidence. It does not replace dependency review, runtime hardening, vulnerability response, or environment-specific risk assessment.

## Vulnerability Disclosure

For vulnerability reporting and disclosure policy, use the Eclipse BaSyx global security policy:

- [eclipse-basyx/.github SECURITY.md](https://github.com/eclipse-basyx/.github/blob/main/SECURITY.md)
