# Supply Chain Security

Supply chain security describes how users can gain confidence that a released BaSyx container image really comes from the expected Eclipse BaSyx repository, was built by the expected CI workflow, and has machine-readable evidence describing how it was produced.

This is different from runtime security. Runtime security controls who can access a running component. Supply chain security helps you decide whether an artifact is trustworthy before you deploy it.

The following diagram shows the main artifacts and evidence users interact with. The image digest is the central deployment artifact; signatures, attestations, SBOMs, and metadata provide the evidence around it.

```{uml} charts/supply_chain_artifacts.puml
```

## Why This Matters

Industrial and digital-twin deployments often become part of long-lived production environments. Pulling an image by name alone, for example `eclipsebasyx/aas-gui:latest`, is convenient, but it does not provide much evidence about what exact artifact was deployed or how it was built.

Supply chain metadata helps with:

| Benefit | What it means for users |
| --- | --- |
| Integrity | Verify that the immutable image digest was signed by the expected project workflow. |
| Traceability | Connect an image back to a repository, commit, workflow, and release version. |
| Auditability | Keep SBOM and provenance files as evidence for compliance and internal reviews. |
| Vulnerability management | Identify the packages and base images inside an artifact so scanners and downstream teams can reason about exposure. |
| Reproducible operations | Deploy by digest so production systems do not silently move when a mutable tag is updated. |

## What BaSyx Release Pipelines Provide

BaSyx Go and the BaSyx AAS Web UI publish container artifacts with open supply-chain standards. Depending on the component, release pipelines provide:

| Artifact or capability | Why it is useful |
| --- | --- |
| Multi-architecture OCI container images | Support deployment on different CPU architectures. |
| Sigstore Cosign keyless signatures | Prove that an immutable image digest was signed by the expected workflow identity. |
| BuildKit OCI attestations | Attach build-time provenance and SBOM data to the OCI image index. |
| Cosign-signed provenance attestations | Provide independently verifiable evidence about how the image was built. |
| Cosign-signed SBOM attestations | Provide independently verifiable package inventory evidence for the image digest. |
| Exported SPDX and CycloneDX SBOM files | Give downstream users downloadable evidence for audits, inventories, and vulnerability tooling. |
| Metadata files | Make release artifacts easier to trace back to source and build context. |
| Vulnerability scanning workflows | Provide continuous visibility for maintainers. |

The component-specific pages explain the exact workflow identities, image names, and verification commands:

- [BaSyx Go supply chain security](./go/supply_chain_security.md)
- [BaSyx AAS Web UI supply chain security](./web_ui/features/supply_chain_security.md)

## Recommended Consumer Practice

For production or compliance-relevant deployments:

1. Select a release version instead of a snapshot whenever possible.
2. Resolve the image tag to an immutable digest.
3. Deploy using `image@sha256:<digest>` instead of a mutable tag.
4. Verify the Cosign signature against the expected GitHub Actions workflow identity.
5. Verify provenance and SBOM attestations when your organization requires build evidence.
6. Store the release SBOM files together with your deployment or release records.
7. Run vulnerability scans in your own environment because risk depends on your deployment context, network exposure, configuration, and compensating controls.

```{note}
Snapshot artifacts are useful for testing, but they are not stable release evidence. Prefer tagged releases for production deployments and compliance records.
```

## Key Terms

**Image digest**
: A cryptographic identifier such as `sha256:...` that points to one immutable image artifact. Tags can move; digests do not.

**Cosign signature**
: A Sigstore signature proving that a specific image digest was signed by a specific identity. BaSyx uses keyless signing, so trust is anchored in GitHub Actions OIDC identity rather than a long-lived private signing key.

**OIDC issuer**
: The identity provider that issued the signing certificate. For GitHub Actions this is `https://token.actions.githubusercontent.com`.

**Certificate identity**
: The workflow identity that signed the artifact. Verification should check this value so that a signature from an unrelated workflow or repository is not accepted.

**Provenance**
: Build metadata describing where and how an artifact was produced, such as repository, workflow, source revision, and build platform.

**SBOM**
: A Software Bill of Materials. It lists software packages and dependencies contained in the artifact so users can perform vulnerability, license, and inventory checks.

**BuildKit OCI attestation**
: Provenance or SBOM metadata attached to the OCI image index by Docker BuildKit.

**Cosign-signed attestation**
: An in-toto attestation signed with Cosign and attached to the image digest. It can be verified independently with identity constraints.

## Vulnerability Disclosure

For vulnerability reporting and disclosure policy, use the Eclipse BaSyx global security policy:

- [eclipse-basyx/.github SECURITY.md](https://github.com/eclipse-basyx/.github/blob/main/SECURITY.md)
