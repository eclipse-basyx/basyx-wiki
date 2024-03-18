# Context Configuration
By default, each Java Off-the-Shelf component starts an HTTP server providing its functionality. The configuration for the servlet can be modified within its **context.properties** file. Here is an example showing the default configuration for the AASServer component:
```
contextPath=/aasServer
contextHostname=localhost
contextPort=4001
```
Here is an example showing the default configuration for the registry component:
```
contextPath=/registry
contextHostname=localhost
contextPort=4000
```
Below is an example showing the default configuration for the Authorized registry component:
```
contextPath=/registry
contextHostname=localhost
contextPort=4000
```
```
jwtBearerTokenAuthenticationIssuerUri=http://127.0.0.1:9006/auth/realms/basyx-demo
jwtBearerTokenAuthenticationJwkSetUri=http://127.0.0.1:9006/auth/realms/basyx-demo/protocol/openid-connect/certs
jwtBearerTokenAuthenticationRequiredAud=basyx-demo
```
With the second configuration, the registry component can be accessed at:
```
http://localhost:4000/registry/
```
Note, that the port 4000 relates to the contextPort in the .properties file and the root path '/registry' is equal to the given contextPath. For docker components, the *context.properties* file can be mounted inside of the container using a volume during container startup. E.g., to run the registry component with custom context configuration, use
```
docker run --name=registry -p 8082:4000 -v C:/tmp:/usr/share/config eclipsebasyx/aas-registry:latest
```
The **context.properties** file has to be located in C:/tmp in this example.

In order to change the context configuration when directly starting the component from a component's Java executable, you can specifiy the configuration file path via the **BASYX_CONTEXT** parameter. See the following example with the registry:
```
java -jar -DBASYX_CONTEXT="C:/tmp/context.properties" registry.jar
```
Note that for docker components, the context port is the container's internal port. A set container port can be mapped to any host port. In the example above, the internal port 4000, given by the context configuration with contextPort, is mapped to the host port 8082. Therefore on the host machine, the registry will be accessible at:
```
http://localhost:8082/registry/
```

## CORS Configuration
Cross-Origin Resource Sharing (CORS) can be configured via the context.properties file by setting the *accessControlAllowOrigin* entry to a specific URL or to a wildcard, e.g., *.

Below is an example showing the Cross-Origin Resource Sharing (CORS) configuration for the registry component:
```
contextPath=/registry
contextHostname=localhost
contextPort=4000
accessControlAllowOrigin=[http://www.basyx-example.com](http://www.basyx-example.com)
```