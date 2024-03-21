# BaSyx Components

## Off-the-Shelf-Components
BaSyx provides several easy to use off-the-shelf components. They can be used programmatically, as an executable jar or as a docker container.

* [AAS Server Component](./v1/aas-server/index.md)
* [Registry Component](./v1/registry/index.md)
* [DataBridge Component](./databridge/index.md)
* [AAS Web UI](./web_ui/index.md)

You can either pull them from Docker Hub or [follow the instructions](./v1/general_configuration/docker.md) to build them yourself.

## Configuring components with environment variables
Please see the following page for configuring BaSyx components using environment variables.

* Configuration with [environment variables](./v1/general_configuration/environment_variables.md)

## Security Component
Please see [Security Configuration](./v1/general_configuration/security/https.md) for an overview over different security relevant options with the BaSyx Java SDK.

## CORS Configuration
Cross-Origin Resource Sharing (CORS) can be configured to the BaSyx off-the-shelf components. Please see [CORS Configuration](./v1/general_configuration/context-config.md) for the steps to configure the CORS to the components.

To get to know more about CORS please visit [Wikipedia Page about CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)

## Developing own Components
There are multiple ways of implementing BaSys 4.0 conforming components.

### Extending Existing Interfaces
For each component, there exist interfaces that can be implemented to realize e.g. new backends. These interfaces integrate seamless in the REST-API-Provider. Additionally, the already defined test suites for the different component types can easily be reused.

In consequence, this is the easiest and fastest way of introducing new components.

### Conforming to the REST-API
If the interfaces provided by BaSyx can't be used (e.g. because the component is implemented in a programming language currently not supported by BaSyx), it has to be ensured that the component is conforming to the defined REST-API and behavior.

For this, BaSyx provides a Technology Compatibility Kit (TCK). The TCKs for the components can be found in the repository in components/tck. For each component, there exists a TCK. Each TCK allows to generate a jar file that tests component functionality of arbitrary http endpoints. Each jar can be called in the following way:

`java -jar $JAR $HTTP_ENDPOINT`

where *$JAR* is the name of the component's TCK jar and *$HTTP_ENDPOINT* is the endpoint on which the component's REST API is available

This section describes how to use the BaSyx Docker-Components.

```{toctree}
:maxdepth: 0

v1/index
v2/index
web_ui/index
databridge/index
```