# Step 4: Providing the Submodel in the network via HTTP
In this step, the code of the previous example will be extended to provide the created Submodel through its [HTTP/REST interface](../../user_documentation/API/submodel.md). Submodels for the same AAS can be created and hosted on different locations in the network. For example, the AAS may be hosted in the central IT infrastructure to ensure its availability. Submodels may be hosted in the infrastructure as well, or on the device. Static information, e.g. a digital nameplate is often hosted in the IT infrastructure as well. Submodels with dynamic data may be hosted closer to the process to prevent a high network load.


## Example Code
The Submodel that has been created in the previous step is made available on a HTTP REST interface by the means of the VAB. This is done by wrapping the provider in a Servlet and providing it via e.g. an Apache Tomcat server. To enable clients to connect to this model, it is registered at the registry.

```java
/**
 * Expected console output in this HandsOn:
 * - the heater id
 * - oven is activated and deactivated multiple times
 * - temperature values between 30 and 40
 */
public class SubModelProvider {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(SubModelProvider.class);
 
	public static void main(String[] args) throws Exception {
		// First, a local model is created that is wrapped by a model provider (see previous step 3)
		Submodel ovenModel = createMyOvenModel(new Oven());
		// Now wrap the model in a SubmodelProvider
		IModelProvider modelProvider = new SubmodelProvider(ovenModel);
		// Up to this point, everything is known from the previous step example
 
 
		// Now, create the servlet that will provide the http/REST interface for accessing the oven Submodel
		// => Every servlet that is provided by this node is available at http://localhost:4001/handson/
		BaSyxContext context = new BaSyxContext("/handson", "", "localhost", 4001);
 
		// Now, the model provider is attached to a HTTP servlet that enables access to the model in the next steps through a HTTP rest interface
		// => The model will be published using an HTTP-REST interface
		HttpServlet modelServlet = new VABHTTPInterface<IModelProvider>(modelProvider);
		logger.info("Created a servlet for the oven model");
 
		// The provider will be available at http://localhost:4001/handson/oven/
                // And submodel can be accessed at: http://localhost:4001/handson/oven/submodel
   		context.addServletMapping("/oven/*", modelServlet);
 
		// Start the local HTTP server
		BaSyxHTTPServer server = new BaSyxHTTPServer(context);
		server.start();
		logger.info("HTTP server started");
	}
}
```