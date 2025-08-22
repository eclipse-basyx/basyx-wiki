# Example 2b - Remote VAB Access with Gateway
This is a variant of [Example 2a](example2a.md). Instead of directly connecting to the the model via TCP, a HTTP/REST to TCP [Gateway](../../../../../concepts%20and%20architecture/gateway.md) is used. Thus, access to models only available via TCP are made possible for web based apps, e.g. a browser.

## Example Code
There's little change necessary to the already existing code. The local code can be reused from [Example 2](example2.md). Only the local side has to change to start the Gateway.

### Local
In this example variant, the local code is very similar to that of variant [Example 2a](example2a.md). Additionally to the existing TCP server, the Gateway is started.

Due to the usage of the Gateway, the path to the oven model has to be changed.
```java
import java.util.Map;
 
import javax.servlet.http.HttpServlet;
 
import org.eclipse.basyx.vab.gateway.DelegatingModelProvider;
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.modelprovider.lambda.VABLambdaProvider;
import org.eclipse.basyx.vab.protocol.basyx.connector.BaSyxConnectorFactory;
import org.eclipse.basyx.vab.protocol.basyx.server.BaSyxTCPServer;
import org.eclipse.basyx.vab.protocol.http.server.BaSyxContext;
import org.eclipse.basyx.vab.protocol.http.server.BaSyxHTTPServer;
import org.eclipse.basyx.vab.protocol.http.server.VABHTTPInterface;
import org.eclipse.basyx.vab.registry.api.IVABRegistryService;
import org.eclipse.basyx.vab.registry.memory.VABInMemoryRegistry;
import org.eclipse.basyx.vab.registry.restapi.VABRegistryModelProvider;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
/**
 * Expected console output in this HandsOn:
 * - the heater id
 * - oven is activated and deactivated multiple times
 * - temperature values between 30 and 40
 */
public class Scenario2Gateway {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(Scenario2Gateway.class);
 
	public static void main(String[] args) throws Exception {
		// First, create a tcp server that hold the model, exactly as is the Example 2a
		BaSyxTCPServer<IModelProvider> tcpModelServer = createOvenTCPServer();
		// And start this tcp server
		tcpModelServer.start();
 
		// Second, create a gateway servlet for storing endpoints for VAB models
		HttpServlet gatewayServlet = createGatewayServlet();
		// Third, create a VAB registry servlet for storing endpoints for VAB models
		HttpServlet registryServlet = createRegistryServlet();
		// Now combine the VAB registry and gateway servlets in one BaSyx HTTP server
		BaSyxHTTPServer httpServer = createHttpServerFromServlets(gatewayServlet, registryServlet);
		// And start this http server
		httpServer.start();
 
		logger.info("Server started");
	}
 
 
	private static BaSyxHTTPServer createHttpServerFromServlets(HttpServlet gatewayServlet,
			HttpServlet directoryServlet) {
		// Define a context to which multiple servlets can be added
		BaSyxContext context = new BaSyxContext("/handson", "", "localhost", 4001);
		// => Every servlet contained in this context is available at http://localhost:4001/handson/
		context.addServletMapping("/gateway/*", gatewayServlet);
		// The model will be available at http://localhost:4001/handson/oven/
		context.addServletMapping("/directory/*", directoryServlet);
		// The directory will be available at http://localhost:4001/handson/directory/
		return new BaSyxHTTPServer(context);
	}
 
	private static HttpServlet createRegistryServlet() {
		// Create a registry that can store endpoints for VAB models
		// => The registry will be published using an HTTP-REST interface
		IVABRegistryService registry = new VABInMemoryRegistry();
		// Similar to the IModelProvider for the local oven model, a IModelProvider for the registry is created
		IModelProvider registryProvider = new VABRegistryModelProvider(registry);
		// Next, this model provider is given to a HTTP servlet that gives access to the VAB registry
		VABHTTPInterface<IModelProvider> registryServlet = new VABHTTPInterface<>(registryProvider);
		logger.info("Created a servlet for the directory");
 
		// Register the VAB model at the directory (locally in this case)
		registry.addMapping("oven", "http://localhost:4001/handson/gateway//basyx://127.0.0.1:6999");
		logger.info("Oven model registered!");
 
		return registryServlet;
	}
 
	private static HttpServlet createGatewayServlet() {
		// Now, the model provider is given to a HTTP servlet that gives access to the
		// model in the next steps
		// => The model will be published using an HTTP-REST interface
		VABHTTPInterface<IModelProvider> gatewayServlet = new VABHTTPInterface<>(new DelegatingModelProvider(new BaSyxConnectorFactory()));
		logger.info("Created a servlet for the gateway");
		return gatewayServlet;
	}
 
	private static BaSyxTCPServer<IModelProvider> createOvenTCPServer() {
		// First, a local model is created that is wrapped by a model provider (see first HandsOn)
		Map<String, Object> model = Scenario1.createMyOvenModel(new Oven());
		IModelProvider modelProvider = new VABLambdaProvider(model);
		// Up to this point, everything is known from the previous HandsOn
 
		// Creates a tcp server providing the oven model on port 7000
		return new BaSyxTCPServer<>(modelProvider, 6999);
	}
}
```

### Remote
As previously stated, the code for remote from [Example 2](example2.md) can be reused.

## Expected Output
You will have different outputs for the local and remote code.

### Local
The output states, that a servlet has ben created for the gateway as wel as the directory before the oven model has been registered. After this there will be some info (maybe in a red text color) about the BaSyx Context and HTTP server (a Tomcat server) and the message from our logger, that the server has been started.

Only if you execute the remote code the output **Heater: activated** and **Heater: deactivated** will show up.

```
15:43:01.110 [main] INFO  i.Scenario2Gateway - Created a servlet for the gateway
15:43:01.112 [main] INFO  i.Scenario2Gateway - Created a servlet for the directory
15:43:01.112 [main] INFO  i.Scenario2Gateway - Oven model registered!
...
15:43:01.573 [main] INFO  i.Scenario2Gateway - Servers started
Heater: activated
Heater: deactivated
Heater: activated
Heater: deactivated
Heater: activated
...
```

### Remote
Once you start the remote you will only see information about the current temperature which will fluctuate between ~30 and ~40. This time the information about the activation or deactivation of the heater will be part of the output of the local code.

```
15:44:43.221 [main] INFO  i.Scenario2Connected - Current temperature: 20.0
15:44:43.370 [main] INFO  i.Scenario2Connected - Current temperature: 23.0
15:44:43.479 [main] INFO  i.Scenario2Connected - Current temperature: 25.7
15:44:43.588 [main] INFO  i.Scenario2Connected - Current temperature: 28.13
15:44:43.695 [main] INFO  i.Scenario2Connected - Current temperature: 30.317
15:44:43.805 [main] INFO  i.Scenario2Connected - Current temperature: 32.2853
15:44:43.914 [main] INFO  i.Scenario2Connected - Current temperature: 34.05677
15:44:44.022 [main] INFO  i.Scenario2Connected - Current temperature: 35.651093
15:44:44.131 [main] INFO  i.Scenario2Connected - Current temperature: 37.08598370000001
15:44:44.241 [main] INFO  i.Scenario2Connected - Current temperature: 38.37738533000001
15:44:44.349 [main] INFO  i.Scenario2Connected - Current temperature: 39.53964679700001
15:44:44.458 [main] INFO  i.Scenario2Connected - Current temperature: 40.58568211730001
15:44:44.579 [main] INFO  i.Scenario2Connected - Current temperature: 36.674402515013014
15:44:44.689 [main] INFO  i.Scenario2Connected - Current temperature: 35.00696226351172
...
```