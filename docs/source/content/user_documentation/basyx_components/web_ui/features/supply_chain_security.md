# Supply Chain Security

The BaSyx AAS Web UI release pipeline for `eclipsebasyx/aas-gui` follows open supply-chain standards and publishes verifiable evidence for release artifacts.

Use this page when you need to:

- Verify that an AAS Web UI image was signed by the expected Eclipse BaSyx GitHub Actions workflow.
- Inspect provenance and SBOM attestations.
- Download SBOM release assets for audit, compliance, or downstream vulnerability management.
- Understand the difference between release evidence and runtime Web UI security.

For the general concepts behind these checks, see the [BaSyx supply chain security overview](../../supply_chain_security.md).

## What the Release Workflow Produces

For each published release, the AAS Web UI release workflow produces:

- Multi-architecture Docker images for `linux/amd64`, `linux/arm64`, and `linux/arm/v7`.
- Docker BuildKit OCI attestations attached to the image index.
- BuildKit provenance with `provenance: mode=max`.
- BuildKit SBOM output with `sbom: true`.
- Sigstore Cosign keyless signature on the immutable image digest.
- Cosign-signed provenance attestations from BuildKit provenance predicates.
- Cosign-signed SBOM attestations using the `https://spdx.dev/Document` predicate type.
- Exported SPDX JSON SBOM files named `aas-gui-<version>.spdx.json`.
- Exported CycloneDX JSON SBOM files named `aas-gui-<version>.cdx.json`.
- `release-image-metadata.json`.
- SBOM uploads as GitHub Actions artifacts for build-time evidence.
- SBOM uploads as GitHub Release assets for versioned downloadable evidence.

The workflow verifies the Syft bootstrap by checking a signed checksum file and certificate identity constraints before verifying the downloaded archive hash.

## Trust Model

AAS Web UI images are signed by GitHub Actions keyless identity for the `eclipse-basyx/basyx-aas-web-ui` repository. Verification should check both the certificate identity and the OIDC issuer.

Expected certificate identity for releases:

```text
https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-release-ui.yml@refs/tags/<tag>
```

Expected certificate identity for snapshots:

```text
https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-prerelease-ui.yml@refs/heads/main
```

Expected OIDC issuer:

```text
https://token.actions.githubusercontent.com
```

```{important}
Verify by digest, not by tag. A digest reference such as `eclipsebasyx/aas-gui@sha256:<digest>` identifies the exact artifact that was signed.
```

## Verify Image Signature

Install [Cosign](https://docs.sigstore.dev/cosign/installation/) and verify the immutable image digest.

```bash
IMAGE="eclipsebasyx/aas-gui@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-release-ui.yml@refs/tags/<tag>"

cosign verify \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

For snapshots, use the snapshot workflow identity:

```bash
IDENTITY="https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-prerelease-ui.yml@refs/heads/main"
```

Successful verification means the digest was signed by the expected GitHub Actions workflow identity. It does not mean the image is free of vulnerabilities or that the runtime configuration is secure.

## Verify Provenance Attestations

The workflow creates explicit Cosign provenance attestations from BuildKit provenance data.

Use the provenance predicate type detected from BuildKit output. Common values are:

- `https://slsa.dev/provenance/v1`
- `https://slsa.dev/provenance/v0.2`

```bash
IMAGE="eclipsebasyx/aas-gui@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-release-ui.yml@refs/tags/<tag>"
PROVENANCE_TYPE="https://slsa.dev/provenance/v1"

cosign verify-attestation \
  --type "$PROVENANCE_TYPE" \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

Provenance helps you confirm the build identity and retain evidence about how the artifact was produced.

## Verify SBOM Attestations

```bash
IMAGE="eclipsebasyx/aas-gui@sha256:<digest>"
IDENTITY="https://github.com/eclipse-basyx/basyx-aas-web-ui/.github/workflows/docker-release-ui.yml@refs/tags/<tag>"

cosign verify-attestation \
  --type "https://spdx.dev/Document" \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE"
```

SBOM attestations are useful for automated policy checks. Downloadable SBOM release assets are useful for audit records, inventory systems, and downstream vulnerability management.

## Verify BuildKit OCI Attestations Exist

The workflow attaches provenance and SBOM as BuildKit OCI attestations.

```bash
IMAGE="eclipsebasyx/aas-gui@sha256:<digest>"

docker buildx imagetools inspect "$IMAGE" --raw | jq \
  '.manifests[] | select(.annotations["vnd.docker.reference.type"] == "attestation-manifest")'
```

If this command returns attestation manifests, the OCI index has attached BuildKit attestations.

## Inspect BuildKit Provenance and SBOM Payloads

```bash
IMAGE="eclipsebasyx/aas-gui@sha256:<digest>"

docker buildx imagetools inspect "$IMAGE" --format '{{ json (index .Provenance "linux/amd64").SLSA }}' | jq .
docker buildx imagetools inspect "$IMAGE" --format '{{ json (index .SBOM "linux/amd64").SPDX }}' | jq .
```

If your Docker or Buildx version does not expose per-platform maps, try:

```bash
docker buildx imagetools inspect "$IMAGE" --format '{{ json .Provenance.SLSA }}' | jq .
docker buildx imagetools inspect "$IMAGE" --format '{{ json .SBOM.SPDX }}' | jq .
```

## Download SBOM Release Assets

Each release includes:

- `aas-gui-<version>.spdx.json`
- `aas-gui-<version>.cdx.json`
- `release-image-metadata.json`

Download these files from the GitHub Release page for the tag you deploy. Store them together with your deployment records if your organization needs release evidence.

## Artifact Types and What They Mean

**Signed image digest**
: Cryptographic evidence that the immutable image digest was signed by the expected workflow identity.

**BuildKit OCI attestations**
: OCI-attached provenance and SBOM data produced at image build time.

**Cosign-signed provenance attestation**
: Signed in-toto evidence about the build process and source context.

**Cosign-signed SBOM attestation**
: Signed in-toto SBOM evidence attached to the image digest.

**GitHub Actions SBOM artifact**
: CI-run artifact retained for build evidence and troubleshooting.

**GitHub Release SBOM assets**
: Versioned SBOM exports intended for downstream consumers and compliance records.

## Vulnerability Scanning

Vulnerability scanning is handled in a dedicated workflow:

- `.github/workflows/vuln-scan.yml`
- Trivy repository filesystem scan for pull requests, pushes, schedules, and manual runs.
- Trivy container image scan for pushes, schedules, and manual runs.
- Report-only behavior.
- SARIF upload to GitHub code scanning where permitted.

Downstream users should still scan the exact image digest they deploy. Vulnerability impact depends on the deployed configuration, reachable components, exposed interfaces, and compensating controls.

## Practical Deployment Implications

For production or compliance-relevant deployments:

1. Prefer release images over snapshots.
2. Resolve the image tag to an immutable digest.
3. Deploy `eclipsebasyx/aas-gui@sha256:<digest>` instead of only `eclipsebasyx/aas-gui:<tag>`.
4. Verify the signature with the expected release workflow identity.
5. Verify provenance and SBOM attestations when your policy requires build evidence.
6. Download and archive the SPDX or CycloneDX SBOM release assets.
7. Configure runtime Web UI authentication separately. Supply chain verification does not replace OAuth2, OIDC, HTTPS, or backend authorization.

## Attestation Verification Model

The release workflows verify:

- Cosign image signatures.
- BuildKit OCI attestation presence and readability.
- Cosign provenance attestations.
- Cosign SBOM attestations.

This provides tamper evidence and traceability for published artifacts. It does not replace vulnerability response, secure runtime configuration, or environment-specific risk assessment.

## Vulnerability Disclosure

For vulnerability reporting and disclosure policy, use the Eclipse BaSyx global security policy:

- [eclipse-basyx/.github SECURITY.md](https://github.com/eclipse-basyx/.github/blob/main/SECURITY.md)
