# Example 2a - Remote VAB Access via BaSyxTCP
This is a variant of the scenario showcased in [Example 2](example2.md).

Instead of accessing the oven model through HTTP/REST, [BaSyxTCP](../../user_documentation/vab/tcp_mapping.md) is used. The registry is still accessed through HTTP/REST.

## Example Code
Only small code changes are necessary to support this scenario. First, the local variant needs to be changed to provide the oven model via TCP. Then, the remote side needs to be extended to support both HTTP/REST and TCP.

### Local
Instead of providing the oven through HTTP/REST, it is now provided via TCP. Thus, the oven servlet is replaced with a [BaSyxTCP](../../user_documentation/vab/tcp_mapping.md) server. Additionally, the registry entry is updated to point to the TCP server.
```java
import java.util.Map;
 
import javax.servlet.http.HttpServlet;
 
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.modelprovider.lambda.VABLambdaProvider;
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
public class Scenario2TCP {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(Scenario2TCP.class);
 
	public static void main(String[] args) throws Exception {
		// First, a local model is created that is wrapped by a model provider (see first HandsOn)
		Map<String, Object> model = Scenario1.createMyOvenModel(new Oven());
		IModelProvider modelProvider = new VABLambdaProvider(model);
		// Up to this point, everything is known from the previous HandsOn
 
		// Create a directory that can store endpoints for VAB models
		// => The directory will be published using an HTTP-REST interface
		IVABRegistryService directory = new VABInMemoryRegistry();
 
		// Register the VAB model at the directory (locally in this case)
		// For this example, the endpoint will be a basyx:// endpoint instead of an http:// endpoint
		directory.addMapping("oven", "basyx://127.0.0.1:7000");
		logger.info("Oven model registered!");
 
		// Similar to the IModelProvider for the local oven model, a IModelProvider for the directory is created
		IModelProvider directoryProvider = new VABRegistryModelProvider(directory);
 
                // Next, this model provider is given to a HTTP servlet that gives access to the directory
		HttpServlet directoryServlet = new VABHTTPInterface<IModelProvider>(directoryProvider);
		logger.info("Created a servlet for the directory");
 
		// Now, define a context to which multiple servlets can be added
		BaSyxContext context = new BaSyxContext("/handson", "", "localhost", 4001);
		// => Every servlet contained in this context is available at http://localhost:4001/handson/
		context.addServletMapping("/directory/*", directoryServlet);
		// The directory will be available at http://localhost:4001/handson/directory/
		BaSyxHTTPServer server = new BaSyxHTTPServer(context);
		// Finally, the HTTP-REST server with this context is started.
		server.start();
 
		// Creates a tcp server providing the oven model on port 7000
		// Note, that this is the only difference to the previous example. The modelProvider is exactly the same
		BaSyxTCPServer<IModelProvider> tcpServer = new BaSyxTCPServer<>(modelProvider, 7000);
		tcpServer.start();
		logger.info("Server started");
	}
}
```

### Remote
Due the abstracting nature of the VAB, there's little change on the remote side. Instead of directly using the HTTPConnectorProvider, the ConnectorProviderMapper is used. It allows to provide different connectors, selected depending on the address passed to it. The ConnectorProviderMapper is initialized with http prefix for HTTP/REST and basyx prefix for TCP.

The application logic, i.e. the control of the oven based on its temperature, remains unchanged. This again showcases the capability of the VAB to enable abstraction from the specific communication mechanism used.
```java
import org.eclipse.basyx.vab.gateway.ConnectorProviderMapper;
import org.eclipse.basyx.vab.manager.VABConnectionManager;
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.protocol.basyx.connector.BaSyxConnectorFactory;
import org.eclipse.basyx.vab.protocol.http.connector.HTTPConnectorFactory;
import org.eclipse.basyx.vab.registry.proxy.VABRegistryProxy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
/** 
 * This is the connected site in the HandsOn. Although everything is executed locally in this HandsOn,
 * the connection to the model can also be established from distributed locations in the network using this code
 * (using the correct network addresses).
 * 
 * The additionally used protocol has to be added to the connection manager. Apart from that, the code for 
 * the remote access is mostly identical to the code in the previous example, since the IModelProvider and 
 * directory abstract from the underlying communication protocol. 
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
		VABRegistryProxy directoryProxy = new VABRegistryProxy("http://localhost:4001/handson/directory/");
 
		// The connection manager is responsible for resolving every connection attempt
		// For this, it needs:
		// - The directory at which all models are registered
		// - A provider for different types of network protocols (in this example, both HTTP-REST and TCPBaSyx)
		ConnectorProviderMapper mapper = new ConnectorProviderMapper();
		mapper.addConnectorProvider("http", new HTTPConnectorFactory());
		mapper.addConnectorProvider("basyx", new BaSyxConnectorFactory());
		// Thus, when creating the connectionManager, this mapper is passed in the constructor
		VABConnectionManager connectionManager = new VABConnectionManager(directoryProxy, mapper);
 
		// It is now one line of code to retrieve a model provider for any registered model in the network
		IModelProvider connectedOven = connectionManager.connectToVABElement("oven");
 
		// Now, implement a simple a simple bang-bang controller as it has been done in the first HandsOn
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
The output states, that the oven model has been registered. After this there will be some info (maybe in a red text color) about the BaSyx Context and HTTP server (a Tomcat server) and the message from our logger, that the server has been started.

Only if you execute the remote code the output **Heater: activated** and **Heater: deactivated** will show up.
```
15:35:57.279 [main] INFO  i.Scenario2TCP - Oven model registered!
15:35:57.292 [main] INFO  i.Scenario2TCP - Created a servlet for the directory
...
15:35:57.753 [main] INFO  i.Scenario2 - HTTP server started
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
15:39:04.381 [main] INFO  i.Scenario2Connected - Current temperature: 20.0
15:39:04.511 [main] INFO  i.Scenario2Connected - Current temperature: 23.0
15:39:04.619 [main] INFO  i.Scenario2Connected - Current temperature: 25.7
15:39:04.729 [main] INFO  i.Scenario2Connected - Current temperature: 28.13
15:39:04.837 [main] INFO  i.Scenario2Connected - Current temperature: 30.317
15:39:04.946 [main] INFO  i.Scenario2Connected - Current temperature: 32.2853
15:39:05.055 [main] INFO  i.Scenario2Connected - Current temperature: 34.05677
15:39:05.161 [main] INFO  i.Scenario2Connected - Current temperature: 35.651093
15:39:05.271 [main] INFO  i.Scenario2Connected - Current temperature: 37.08598370000001
15:39:05.379 [main] INFO  i.Scenario2Connected - Current temperature: 38.37738533000001
15:39:05.488 [main] INFO  i.Scenario2Connected - Current temperature: 39.53964679700001
15:39:05.595 [main] INFO  i.Scenario2Connected - Current temperature: 40.58568211730001
15:39:05.703 [main] INFO  i.Scenario2Connected - Current temperature: 38.52711390557001
15:39:05.810 [main] INFO  i.Scenario2Connected - Current temperature: 36.674402515013014
15:39:05.921 [main] INFO  i.Scenario2Connected - Current temperature: 35.00696226351172
...
```