# Example 2 - Remote VAB Access
In this example, the code of the previous example will be extended. The model will locally be deployed on a server and registered at the [VABRegistry](../../../../../concepts%20and%20architecture/vab/index.md). Next, on the remote side, the model path is retrieved from the registry and the connection to the model is established. Finally, the same control loop as in Example 1 is implemented. As supporting component, the VABDirectoryServlet is used.

## Example Code
Since the model is now potentially deployed on a separate compute node, in the following it is distinguished between the local and the remote side.

### Local
The previously in Example 1 defined model is made available on a HTTP REST interface by the means of the VAB. This is done by wrapping the provider in a Servlet and providing it via e.g. an Apache Tomcat server. To enable clients to connect to this model, it is registered at the VABRegistry.
```java
import java.util.Map;
 
import javax.servlet.http.HttpServlet;
 
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.modelprovider.lambda.VABLambdaProvider;
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
public class Scenario2 {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(Scenario2.class);
 
	public static void main(String[] args) throws Exception {
		// First, a local model is created that is wrapped by a model provider (see first HandsOn)
		Map<String, Object> model = Scenario1.createMyOvenModel(new Oven());
		IModelProvider modelProvider = new VABLambdaProvider(model);
		// Up to this point, everything is known from the previous HandsOn
 
		// Now, the model provider is given to a HTTP servlet that gives access to the model in the next steps
		// => The model will be published using an HTTP-REST interface
		HttpServlet modelServlet = new VABHTTPInterface<IModelProvider>(modelProvider);
		logger.info("Created a servlet for the oven model");
 
		// Second, create a directory that can store endpoints for VAB models
		IVABRegistryService directory = new VABInMemoryRegistry();
 
                // Register the VAB model at the directory (locally in this case)
		directory.addMapping("oven", "http://localhost:4001/handson/oven");
                logger.info("Oven model registered!");
 
                // Similar to the IModelProvider for the local oven model, a IModelProvider for the directory is created
		IModelProvider directoryProvider = new VABRegistryModelProvider(directory);
                // Next, this model provider is given to a HTTP servlet that gives access to the directory
		HttpServlet directoryServlet = new VABHTTPInterface<IModelProvider>(directoryProvider);
		logger.info("Created a servlet for the directory");
 
		// Now, define a context to which multiple servlets can be added
		BaSyxContext context = new BaSyxContext("/handson", "", "localhost", 4001);
		// => Every servlet contained in this context is available at http://localhost:4001/handson/
		context.addServletMapping("/oven/*", modelServlet);
		// The model will be available at http://localhost:4001/handson/oven/
		context.addServletMapping("/directory/*", directoryServlet);
		// The directory will be available at http://localhost:4001/handson/directory/
		BaSyxHTTPServer server = new BaSyxHTTPServer(context);
		// Finally, the HTTP-REST server with this context is started.
		server.start();
		logger.info("HTTP server started");
	}
}
```

### Remote
The remote side connects to the provided model. This is done by first retrieving the path of the model and then using it to connect to the model. Next, the control loop is implemented. Since the VAB abstracts from the location of the accessed model, the code for the control loop is equivalent to the code from Example 1.
```java
import org.eclipse.basyx.vab.manager.VABConnectionManager;
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.protocol.http.connector.HTTPConnectorFactory;
import org.eclipse.basyx.vab.registry.proxy.VABRegistryProxy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
/**
 * This is the connected site in the HandsOn. Although everything is executed locally in this HandsOn,
 * the connection to the model can also be established from distributed locations in the network using this code
 * (using the correct network addresses).
 * 
 */
 
public class Scenario2Connected {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(Scenario2Connected.class);
 
	public static void main(String[] args) throws Exception {
		// At the connected site, no direct access to the model is possible
		// Every access is done through the network infrastructure
 
		// The Virtual Automation Bus hides network details to the connected site. Only the endpoint of the
		// directory has to be known:
		VABRegistryProxy registryProxy = new VABRegistryProxy("http://localhost:4001/handson/directory/");
 
		// The connection manager is responsible for resolving every connection attempt
		// For this, it needs:
		// - The directory at which all models are registered
		// - A provider for different types of network protocols (in this example, only HTTP-REST)
		VABConnectionManager connectionManager = new VABConnectionManager(registryProxy, new HTTPConnectorFactory());
 
		// It is now one line of code to retrieve a model provider for any registered
		// model in the network
		IModelProvider connectedOven = connectionManager.connectToVABElement("oven");
 
		// Now, implement a simple a simple bang-bang controller as it has been done in the first HandsOn
		// Note, that the IModelProvider completely abstracts from the underlying communication protocol
		for (int i = 0; i < 100; i++) {
			// Pause for 100ms
			Thread.sleep(100);
 
			// Retrieve the current temperature from the model provider
			double temperature = (double) connectedOven.getValue("/properties/temperature");
			logger.info("Current temperature: " + temperature);
 
			// Turn the oven on/off, depending on the defined temperature range
			if (temperature > 40) {
				connectedOven.invokeOperation("/operations/deactivateOven");
			} else if (temperature < 30) {
				connectedOven.invokeOperation("/operations/activateOven");
			}
		}
	}
}
```

## Expected Output
You will have different outputs for the local and remote code.

### Local
The output states, that a servlet has been created and the model registered. After this there will be some info (maybe in a red text color) about the BaSyx Context server (a Tomcat server) and the message from our logger, that the HTTP server has been started.

Only if you execute the remote code the output **Heater: activated** and **Heater: deactivated** will show up.
```
15:16:32.251 [main] INFO  i.Scenario2 - Created a servlet for the oven model
15:16:32.253 [main] INFO  i.Scenario2 - Oven model registered!
15:16:32.253 [main] INFO  i.Scenario2 - Created a servlet for the directory
...
15:16:32.730 [main] INFO  i.Scenario2 - HTTP server started
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
15:16:50.794 [main] INFO  i.Scenario2Connected - Current temperature: 20.0
15:16:50.945 [main] INFO  i.Scenario2Connected - Current temperature: 25.7
15:16:51.053 [main] INFO  i.Scenario2Connected - Current temperature: 28.13
15:16:51.162 [main] INFO  i.Scenario2Connected - Current temperature: 30.317
15:16:51.271 [main] INFO  i.Scenario2Connected - Current temperature: 32.2853
15:16:51.381 [main] INFO  i.Scenario2Connected - Current temperature: 34.05677
15:16:51.489 [main] INFO  i.Scenario2Connected - Current temperature: 35.651093
15:16:51.599 [main] INFO  i.Scenario2Connected - Current temperature: 37.08598370000001
15:16:51.708 [main] INFO  i.Scenario2Connected - Current temperature: 38.37738533000001
15:16:51.817 [main] INFO  i.Scenario2Connected - Current temperature: 39.53964679700001
15:16:51.925 [main] INFO  i.Scenario2Connected - Current temperature: 40.58568211730001
15:16:52.032 [main] INFO  i.Scenario2Connected - Current temperature: 38.52711390557001
15:16:52.141 [main] INFO  i.Scenario2Connected - Current temperature: 36.674402515013014
15:16:52.251 [main] INFO  i.Scenario2Connected - Current temperature: 35.00696226351172
...
```