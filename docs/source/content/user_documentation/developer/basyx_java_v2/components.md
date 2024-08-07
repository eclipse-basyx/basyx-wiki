
# Components
The components 
* [AAS Repository](../../basyx_components/v2/aas_repository/index.md)
* [Submodel Repository](../../basyx_components/v2/submodel_repository/index.md)
* [Concept Description Repository](../../basyx_components/v2/cd_repository/index.md)
* [AAS Environment](../../basyx_components/v2/aas_environment/index.md)
* [AAS Registry](../../basyx_components/v2/aas_registry/index.md)
* [Submodel Registry](../../basyx_components/v2/submodel_registry/index.md)
* [AAS Discovery](../../basyx_components/v2/aas_discovery/index.md)

are highly configurable by leveraging the Spring framework. Thus, they utilize existing Spring configuration properties, e.g., for MongoDB. In addition, the components offer common mechanisms for checking the current health status of the application and configuring Cross-Origin Resource Sharing (CORS) options.
The source code for all the components can be found on the `basyx-java-server-sdk` GitHub Repository:

[basyx-java-server-sdk](https://github.com/eclipse-basyx/basyx-java-server-sdk)

## Health Endpoint
The health endpoint to check whether the server is up and running is available at:

	http://{host}:{port}/actuator/health
For a detailed documentation on its configuration possibilities, please refer to [Spring Management Endpoint](management_endpoint.md) documentation.

## CORS configuration
Cross-Site Resource Sharing options can be configured under [application.properties](https://github.com/eclipse-basyx/basyx-java-server-sdk/blob/main/basyx.aasrepository/basyx.aasrepository.component/src/main/resources/application.properties#L26) with the following attributes:

* Allowed Origin Patterns:<br>
Comma-separated list of origin patterns to allow. Unlike allowed origins which only supports '\*', origin patterns are more flexible (for example 'https://\*.example.com') and can be used when credentials are allowed. When no allowed origin patterns or allowed origins are set, CORS support is disabled.
  ```
  basyx.cors.allowed-origins=http://localhost:8080, https://*.example.com
  ```

* Allowed Methods:<br>
Comma-separated list of HTTP methods to allow. When not set, defaults to GET,HEAD,POST.
  ```
  basyx.cors.allowed-methods=GET,POST,PATCH,DELETE,PUT,OPTIONS,HEAD
  ```

## Configuration via Environment Variables
The BaSyx V2 components use the Spring framework as described above. Due to this, all configuration options of Spring are also available for BaSyx. In consequence, each entry of the _application.properties_ file can be also configured via environment variables by replacing "." with "_" and capitalizing each letter.

As an example _"basyx.backend"_ can be configured via the environment variable _"BASYX_BACKEND"_.