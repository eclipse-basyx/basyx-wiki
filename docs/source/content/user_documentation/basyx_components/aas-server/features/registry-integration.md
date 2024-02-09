# Registry Integration
## User Story & Use Case
*As AAS Server user*

*I want AAS Server and AAS Registry to be linked*

*so that I don't have to directly work with the AAS registry in most use cases*

In a full deployment of BaSyx using the AAS Server component and AAS Registry component, by linking the AAS Server to the AAS Registry, the AAS Server can provide additional quality of life features.

## Feature Overview
If AAS and/or Submodels are preconfigured, linking the AAS Server to the AAS Registry will automatically register the preconfigured AAS/Submodels.

Additionally, the AAS Server will try to resolve requests for distributed Submodels for an AAS stored on the component via the registry.

If the AAS Server is externally accessible by a different URL (e.g., in a reverse-proxy scenario), its externally visible URL can be configured for AAS Registry registration. Furthermore, the AAS Server will automatically register/unregister uploaded/deleted AAS and Submodels.

## Feature Configuration
The registry path depends on the deployment location. Thus, when starting a local docker registry for testing purposes, it needs to be in the same docker network as the AAS to be reachable. So for a non-docker deployment, the registry address could be:
```
registry.path=http://localhost:4000/registry/
```
Whereas it could be different for a deployment with docker containers:
```
registry.path=http://registry:4000/registry/
```
See also the official [Docker documentation](https://docs.docker.com/network/) for more information on that topic.


If the external URL of the AAS Server differs from its internal address, this external address can be specified to be used when auto registering AASs/Submodels:
```
aas.externalurl=http://external-address:4000/aasServer
```
If this value is not specified the internal address of the AAS Server will be used.


For integrating with a secured AAS Registry, additional configuration is necessary in aas.properties:
```
tokenEndpoint=http://127.0.0.1:9006/auth/realms/basyx-demo/protocol/openid-connect/token
clientId=basyx-demo
clientSecret=OZtOv3TlXvEhhKf705Z53J8QL8YPY9UJP
clientScopes=["urn:org.eclipse.basyx:scope:aas-registry:read","urn:org.eclipse.basyx:scope:aas-registry:write"]
```