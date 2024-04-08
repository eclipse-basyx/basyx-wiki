# Example 4

After the last example, we can control the oven through a unified service interface. However, the provided descriptions, data and semantics are still custom made. Thus, an application working with the oven, retrieving temperature and controlling it is not necessary interoperable with another oven, using the same abstract data but not the same model.

To fill this gap, the [Asset Administration Shell](../../../../../concepts%20and%20architecture/aas_overview.md) will be used in this example. Additionally, we will explore the AAS meta model through its [HTTP-REST](../../../../../API/aas.md) interface by using any browser.

## Example Code
First, two submodels are created with properties and operations. These properties/operations hold meta data giving a description of their semantics. The defined submodels are:

1. SensorSubModel: Contains sensor data, in this case the temperature value. Additionally, a temperature unit is made available.
2. ControlSubModel: Exposes the services available, in this case it references the Control Component.

Please note that the Control Component is a concept not within the standard of the AAS. Thus, the Control Component has to be either referenced like in this example or expose itself through the submodel interface. Additionally, the standard referenced by the temperature property already defines the unit. For the sake of this tutorial, it is assumed that the oven is not 100% conforming to this standard and can switch between Fahrenheit and Celsius.

Next, these submodels are added to an AAS and hosted via HTTP. Additionally, the AAS and its submodel are registered with the [AAS Registry](../../../../../API/registry.md). After starting the HTTP server and registering, the Registry, AAS and its submodel can be explored via the HTTP-REST interface as described in the example or above.

```java
import java.util.function.Function;
 
import javax.servlet.http.HttpServlet;
 
import org.eclipse.basyx.aas.metamodel.api.parts.asset.AssetKind;
import org.eclipse.basyx.aas.metamodel.map.AssetAdministrationShell;
import org.eclipse.basyx.aas.metamodel.map.descriptor.AASDescriptor;
import org.eclipse.basyx.aas.metamodel.map.descriptor.ModelUrn;
import org.eclipse.basyx.aas.metamodel.map.descriptor.SubmodelDescriptor;
import org.eclipse.basyx.aas.metamodel.map.parts.Asset;
import org.eclipse.basyx.aas.registration.api.IAASRegistry;
import org.eclipse.basyx.aas.registration.memory.InMemoryRegistry;
import org.eclipse.basyx.aas.registration.restapi.AASRegistryModelProvider;
import org.eclipse.basyx.aas.restapi.AASModelProvider;
import org.eclipse.basyx.aas.restapi.MultiSubmodelProvider;
import org.eclipse.basyx.models.controlcomponent.ExecutionState;
import org.eclipse.basyx.submodel.metamodel.api.reference.enums.KeyElements;
import org.eclipse.basyx.submodel.metamodel.api.reference.enums.KeyType;
import org.eclipse.basyx.submodel.metamodel.map.Submodel;
import org.eclipse.basyx.submodel.metamodel.map.reference.Key;
import org.eclipse.basyx.submodel.metamodel.map.reference.Reference;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.AASLambdaPropertyHelper;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.Property;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.valuetype.ValueType;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.operation.Operation;
import org.eclipse.basyx.submodel.restapi.SubmodelProvider;
import org.eclipse.basyx.vab.coder.json.connector.JSONConnector;
import org.eclipse.basyx.vab.modelprovider.VABElementProxy;
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.protocol.basyx.connector.BaSyxConnector;
import org.eclipse.basyx.vab.protocol.http.server.BaSyxContext;
import org.eclipse.basyx.vab.protocol.http.server.BaSyxHTTPServer;
import org.eclipse.basyx.vab.protocol.http.server.VABHTTPInterface;
 
/** 
 * Now we actually create an oven AssetAdministrationShell (AAS) using the standardized metamodel
 * 
 * The AAS will have two simple submodels:
 * Sensor
 * - submodel that represents the temperature sensor of the oven
 * Control
 * - submodel for accessing the connected control component via the AAS API
 * 
 * 
 * Expected output:
 * - the Asset Administration Shell for the oven device is accessible using the internet browser (because of the
 * HTTP-REST interface that is used in this HandsOn)
 * - the Registry is accessible using the internet browser (because of the
 * HTTP-REST interface that is used in this HandsOn)
 */
public class Scenario4 {
	public static void main(String[] args) throws Exception {
		// Create and provide the control component from the previous HandsOn
		Oven myOven = new Oven();
		Scenario3.startMyControlComponent(myOven);
		startMyAssetAdministrationShell(myOven);
	}
 
	public static void startMyAssetAdministrationShell(Oven myOven) {
		/**
		 * Sensor Submodel
		 */
		Submodel sensorSubModel = new Submodel("Sensor", new ModelUrn("urn:org.eclipse.basyx:SensorSubmodel"));
		// Create a lambda property containing the current sensor temperature
		Property temperatureProperty = new Property("currentTemperature", ValueType.Double);
		AASLambdaPropertyHelper.setLambdaValue(temperatureProperty, () -> {
			return myOven.getSensor().readTemperature();
		}, null);
 
		// Adds a reference to a semantic ID to specify the property semantics (see eCl@ss)
		temperatureProperty.setSemanticId(
				new Reference(new Key(KeyElements.PROPERTY, false, "0173-1#02-AAV232#002", KeyType.IRDI)));
		sensorSubModel.addSubmodelElement(temperatureProperty);
 
		Property temperatureUnit = new Property("temperatureUnit", ValueType.String);
		temperatureUnit.setValue("Celsius");
		sensorSubModel.addSubmodelElement(temperatureUnit);
 
		/**
		 * Control Submodel
		 */
		Submodel heaterSubModel = new Submodel("Control", new ModelUrn("urn:org.eclipse.basyx:SensorSubmodel"));
		// Create an operation that uses the control component to set a temperature value
		Function<Object[], Object> heatInvokable = (params) -> {
			// From: HandsOn 04
			// Connect to the control component
			VABElementProxy proxy = new VABElementProxy("", new JSONConnector(new BaSyxConnector("localhost", 4002)));
 
			// Select the operation from the control component
			proxy.setValue("status/opMode", OvenControlComponent.OPMODE_HEAT);
 
			// Start the control component operation asynchronous
			proxy.invokeOperation("/operations/service/start");
 
			// Wait until the operation is completed
			while (!proxy.getValue("status/exState").equals(ExecutionState.COMPLETE.getValue())) {
				try {
					Thread.sleep(500);
				} catch (InterruptedException e) {
				}
			}
 
			proxy.invokeOperation("operations/service/reset");
			// Then return -> synchronous
			return null;
		};
 
		// Create the Operation
		Operation operation = new Operation("setTemperature");
		operation.setInvokable(heatInvokable);
		heaterSubModel.addSubmodelElement(operation);
 
		/**
		 * Minimal AAS Information
		 */
 
		Asset asset = new Asset("ovenAsset", new ModelUrn("urn:org.eclipse.basyx:OvenAsset"), AssetKind.INSTANCE);
 
		ModelUrn aasURN = new ModelUrn("urn:org.eclipse.basyx:OvenAAS");
		AssetAdministrationShell aas = new AssetAdministrationShell("oven", aasURN, asset);
		// Note: The submodels are not directly integrated into the AAS model. This makes it possible to distribute
		// submodels to different nodes
		// The header contains references to the previously created submodels.
		// Here, the submodel endpoints are not yet known. They can be specified as soon as the real endpoints are known
 
		/**
		 * Again: Wrap the model in an IModelProvider (now specific to the AAS and submodel)
		 */
		// AASModelProvider and SubModelProvider implement the IModelProvider interface
		AASModelProvider aasProvider = new AASModelProvider(aas);
		SubmodelProvider sensorSMProvider = new SubmodelProvider(sensorSubModel);
		SubmodelProvider heaterSMProvider = new SubmodelProvider(heaterSubModel);
 
		// Add the independent providers to the MultiSubmodelProvider that can be deployed on a single node
		MultiSubmodelProvider fullProvider = new MultiSubmodelProvider();
		fullProvider.setAssetAdministrationShell(aasProvider);
		fullProvider.addSubmodel(sensorSMProvider);
		fullProvider.addSubmodel(heaterSMProvider);
 
		// Although the providers for aas/submodels implement the AAS API, they are still IModelProviders!
		// IModelProvider aasIModelProvider = fullProvider;
 
		/**
		 * Deployment
		 */
		// Now, the IModelProvider is given to a HTTP servlet that gives access to the model in the next steps
		// => The model will be published using an HTTP-REST interface
		HttpServlet aasServlet = new VABHTTPInterface<IModelProvider>(fullProvider);
 
		// For this HandsOn, create an InMemoryRegistry for registering the AAS
		IAASRegistry registry = new InMemoryRegistry();
		IModelProvider registryProvider = new AASRegistryModelProvider(registry);
		HttpServlet registryServlet = new VABHTTPInterface<IModelProvider>(registryProvider);
 
		// now add the references of the submodels to the AAS header
		aas.addSubmodel(sensorSubModel);
		aas.addSubmodel(heaterSubModel);
 
		// Register the VAB model at the directory (locally in this case)
		AASDescriptor aasDescriptor = new AASDescriptor(aas, "http://localhost:4000/handson/oven/aas");
		// Explicitly create and add submodel descriptors
		SubmodelDescriptor sensorSMDescriptor = new SubmodelDescriptor(sensorSubModel, "http://localhost:4000/handson/oven/aas/submodels/Sensor");
		SubmodelDescriptor heaterSMDescriptor = new SubmodelDescriptor(heaterSubModel, "http://localhost:4000/handson/oven/aas/submodels/Control");
		aasDescriptor.addSubmodelDescriptor(sensorSMDescriptor);
		aasDescriptor.addSubmodelDescriptor(heaterSMDescriptor);
		registry.register(aasDescriptor);
 
		// Deploy the AAS on a HTTP server
		BaSyxContext context = new BaSyxContext("/handson", "", "localhost", 4000);
		context.addServletMapping("/oven/*", aasServlet);
		context.addServletMapping("/registry/*", registryServlet);
		BaSyxHTTPServer httpServer = new BaSyxHTTPServer(context);
 
 
		httpServer.start();
 
		// Now in the browser, look at the various endpoints to see what is returned:
		// - AAS: http://localhost:4000/handson/oven/aas/
		// - Sensor Submodel: http://localhost:4000/handson/oven/aas/submodels/Sensor/
		// - Control Submodel: http://localhost:4000/handson/oven/aas/submodels/Control/
 
		// Similar, the registry also has a HTTP-REST interface. So, it is possible to directly query it:
		// - Show all AAS: http://localhost:4000/handson/registry/api/v1/registry/
		// - Show my AAS: http://localhost:4000/handson/registry/api/v1/registry/urn:org.eclipse.basyx:OvenAAS
		// Note: the "#" character in the URN s encoded as "%23"
 
		// The server can also be shut down:
		/* 
		try {
			// Wait for 5s and then shutdown the server
			Thread.sleep(5000);
			httpServer.shutdown();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		*/
	}
}
```

## Expected Output
The output will consist of the info (maybe in a red text color) about the BaSyx Context and HTTP server (a Tomcat server) which has been started. No other output will be generated in the console. You have to visit [ http://localhost:4000/handson/oven/aas ] to check if everything works as expected and explore the AAS meta model through its [HTTP-REST]((../../../../../API/aas.md)) interface.