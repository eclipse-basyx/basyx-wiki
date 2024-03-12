# Existing Releases

## Java Release 1.5.1

Bugfixes:

* Fixes Submodel creation event being sent at incorrect times when using MongoDB
* Fixes FileSubmodelElement‘s value being wrong with MongoDB & preconfigured AASX

## Java Release 1.5.0

Features:

* RBAC can now be configured based on submodel SemanticId
* Reworks MongoDB backend implementation to be stateless, thus enabling better scaling
* Adds compatibility for inconsistently specified dataTypes (allows upercase)
* Adds ConnectedEntity for working with remote Entity SMEs
* Adds support for implementing further EmbeddedDataSpecification
Bugfixes:

* Fixes empty assets in AAS when deserializing from XML/AASX
* Fixes RBAC configuration file not being read from file system
* Adds missing ValueType "decimal"
* Fixes File SubmodelElement's files sometimes not being served
* Fixes order of calls to AAS Server & AAS Registry in case of AAS/Submodel deletion to ensure consistent state in registry
* Fixes collisions in case of loading multiple AASX that included files with same file name
* Fixes AASX upload ignoring files included in AASX
* Fixes submodel elements being duplicated in MongoDB when being created in an SMC
Miscellaneous:

* Renames "registry.host" entry of AAS Server configuration to "aas.externalurl" to highlight its intention and avoid confusion. "registry.host" still works to ensure backward compatibility.

## Java Release 1.4.0

Features:

* AAS/Submodels added to the AAS Server are now automatically registered with the Registry, if configured
* File SubmodelElements now support upload/download of files by a dedicated HTTP/REST API
    * Upload via HTTP/POST [1] (path-to-file-submodelelement/File/upload)
    * Download via HTTP/GET [1] (path-to-file-submodelelement/File)
    * Supported for both InMemory and MongoDB backend
* If a file is uploaded to a File SubmodelElement, the value of the File SubmodelElement is automatically adapted
* The ConnectedAASManager now tries all endpoints and takes the first working one
    * This is particulary useful in reverse-proxy scenarios where only certain endpoints may be valid depending on the context
Bugfixes:

* Fixes bug where aasx file unpacking could fail
* Fixes scenarios where an mqtt client was not shut down correctly
* Fixes signals like SIGTERM not being correctly propagated to the Docker components
    * Shutting down an AAS Server gracefully now unregisters every contained AAS/Submodel, if a registry is configured

## Java Release 1.3.1

* Fixes OperationVariable's internal representation of SMC & Entity
* Adds missing date valuetype
* Adds missing Wget installation to components' Dockerfiles for Health Checks
* Fixes MongoDBSubmodelAPI value retrieval bug
* Fixes delegated operation handling in MongoDBSubmodelAPI
* Removes _id entry from aas/sm where not already removed for MongoDB
* Enables auto reconnect for mqtt connection
* Fixes missing mapping of mqtt client environment variable
* Adds missing default config for mqtt to docker images

## Java Release 1.3
* Hierarchical MQTT Topics for [AASServer](./user_documentation/basyx_components/aas-server/features/hierarchical-mqtt.md) and [AASRegistry](./user_documentation/basyx_components/registry/features/hierarchical-mqtt.md) with flexible Identifier encoding
    * Base64URL encoding
    * URL encoding
* [Property Delegation](./user_documentation/basyx_components/aas-server/features/property-delegation.md)
* [Adds MongoDB backend for tagged directory](./user_documentation/basyx_components/registry/features/tagged-directory.md)
* Each component now provides a health endpoint
* [Integrates secured AAS Registry with AAS Server](./user_documentation/basyx_components/aas-server/features/registry-integration.md)
* Rule-based Authorization (see example project)

## Java Release 1.2

Features:

* CORS-Support
* Asset Reference Harmonization
* TaggedDirectory:
    * Adds support for authorization
    * Adds support for MQTT Eventing
* Updates Tomcat to Version 9.0.64
* Graceful shutdown of AAS Server unregisters contained AAS/Submodels if a registry is configured

## Java Release 1.1

* MQTT eventing for all APIs
* Authorization support for all APIs
* Upload of AASX via HTTP-POST using multipart/form-data
* Operation Delegation Mechanism enabling delegating operation calls made on the AAS OTS Server to outside HTTP/REST APIs
* Integration of TaggedDirectory with off-the-shelf Registry component

## Java Release 1.0

* Support of [DotAAS (Part 1) v2.0.1](https://www.plattform-i40.de/IP/Redaktion/EN/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part1_V2.html)
    * Implementation of the meta model
    * Implementation of JSON/XML/AASX serialization & deserialization
* Server/Client implementation according to the [API specification](https://app.swaggerhub.com/organizations/BaSyx)
    * [AAS Registry](./user_documentation/basyx_components/registry/index.md) with MongoDB/SQL/InMemory backend
    * [AAS Repository](./user_documentation/basyx_components/aas-server/index.md) with MongoDB/InMemory backend
    * Submodel Repository with MongoDB/InMemory backend
* Provision of components as easy-to-configure off-the-shelf components (e.g. [Docker Images](https://hub.docker.com/u/eclipsebasyx))
    * [AAS Registry](./user_documentation/basyx_components/registry/index.md)
    * [AAS Repository](./user_documentation/basyx_components/aas-server/index.md)
    * [Streamsheets Integration](./user_documentation/monitoring_scenarios.md)
    * [Grafana Integration](./user_documentation/monitoring_scenarios.md)
* Implementation of specified submodel types
    * [Digital Nameplate](https://www.plattform-i40.de/IP/Redaktion/DE/Downloads/Publikation/Submodel_Templates-Asset_Administration_Shell-digital_nameplate.pdf?__blob=publicationFile&v=2)
    * [Technical Data](https://www.plattform-i40.de/IP/Redaktion/DE/Downloads/Publikation/Submodel_Templates-Asset_Administration_Shell-Technical_Data.pdf?__blob=publicationFile&v=6)
* Implementation of [MQTT](./developer/extensions/eventing.md) for AAS/SM
* Implementation of TaggedDirectory
* [VAB](./user_documentation/vab/index.md)
* [Control Components](./user_documentation/controlcomponent.md)

# Upcoming Releases

Upcoming releases are prepared in their respective branches

## C# Release 1.0

The current status can be found in the big-interface-changes branch. It will be merged to the master branch after official release. The following elements are part of the release:

* Implementation of [Details of the Asset Administration Shell (Part 1) v2.0.1](https://www.plattform-i40.de/IP/Redaktion/EN/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part1_V2.html)
    * Implementation of the meta model
    * Implementation of JSON/XML/AASX serialization & deserialization
* Full compatibility with AASX Package Explorer
* Building Blocks: Interface Definitions & Reference Implementations according to the [API specification](https://app.swaggerhub.com/organizations/BaSyx)
    * Asset Administration Shell Registry
    * Asset Administration Shell Server
    * Asset Administration Shell Repository Server
    * Submodel Server
    * Submodel Repository Server
    * Client libraries for all definitions above
* User-Interfaces (UI) for all building blocks
* Applications (ready to be deployed from Edge to Cloud):
    * Asset Administration Shell Registry
    * Asset Adminsitration Shell Repository Server
    * AASX Package Server
* Examples

## C++ Release 1.0

* Implementation of the AAS meta model as specified in [DotAAS (Part 1) v2.0.1](https://www.plattform-i40.de/IP/Redaktion/EN/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part1_V2.html)
* [VAB](./user_documentation/vab/index.md)
* [Control Components](./user_documentation/controlcomponent.md)
* VAB OPC UA support
* OPC UA AAS API support
* OPC UA Gateway

## Java Release 2.0

See [GitHub](https://github.com/eclipse-basyx/basyx-java-server-sdk) for details