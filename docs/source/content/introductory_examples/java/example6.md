# Example 6 - Hello World

The "Hello World" example is a very basic client/server demonstration of BaSyx that utilizes the [Off-the-shelf components](../../user_documentation/basyx_components/index.md). It can be found in the BaSyx repository in *examples/basyx.hello_world*. The "Hello World" project consists of two parts: Client and Server.

## Server Class

```java
import org.eclipse.basyx.aas.manager.ConnectedAssetAdministrationShellManager;
import org.eclipse.basyx.aas.metamodel.api.parts.asset.AssetKind;
import org.eclipse.basyx.aas.metamodel.map.AssetAdministrationShell;
import org.eclipse.basyx.aas.metamodel.map.descriptor.CustomId;
import org.eclipse.basyx.aas.metamodel.map.parts.Asset;
import org.eclipse.basyx.aas.registration.proxy.AASRegistryProxy;
import org.eclipse.basyx.components.aas.AASServerComponent;
import org.eclipse.basyx.components.aas.configuration.AASServerBackend;
import org.eclipse.basyx.components.aas.configuration.BaSyxAASServerConfiguration;
import org.eclipse.basyx.components.configuration.BaSyxContextConfiguration;
import org.eclipse.basyx.components.registry.RegistryComponent;
import org.eclipse.basyx.components.registry.configuration.BaSyxRegistryConfiguration;
import org.eclipse.basyx.components.registry.configuration.RegistryBackend;
import org.eclipse.basyx.submodel.metamodel.api.identifier.IIdentifier;
import org.eclipse.basyx.submodel.metamodel.map.Submodel;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.Property;
 
public class Server {
	// Server URLs
	public static final String REGISTRYPATH = "http://localhost:4000/registry";
	public static final String AASSERVERPATH = "http://localhost:4001/aasServer";
 
	// AAS/Submodel/Property Ids
	public static final IIdentifier OVENAASID = new CustomId("eclipse.basyx.aas.oven");
	public static final IIdentifier DOCUSMID = new CustomId("eclipse.basyx.submodel.documentation");
	public static final String MAXTEMPID = "maxTemp";
 
	public static void main(String[] args) {
		// Create Infrastructure
		startRegistry();
		startAASServer();
 
		// Create Manager - This manager is used to interact with an AAS server
		ConnectedAssetAdministrationShellManager manager = 
				new ConnectedAssetAdministrationShellManager(new AASRegistryProxy(REGISTRYPATH));
 
		// Create AAS and push it to server
		Asset asset = new Asset("ovenAsset", new CustomId("eclipse.basyx.asset.oven"), AssetKind.INSTANCE);
		AssetAdministrationShell shell = new AssetAdministrationShell("oven", OVENAASID, asset);
 
		// The manager uploads the AAS and registers it in the Registry server
		manager.createAAS(shell, AASSERVERPATH);
 
		// Create submodel
		SubModel documentationSubmodel = new SubModel("documentationSm", DOCUSMID);
 
		// - Create property
		Property maxTemp = new Property(MAXTEMPID, 1000);
 
		// Add the property to the Submodel
		documentationSubmodel.addSubModelElement(maxTemp);
 
		// - Push the Submodel to the AAS server
		manager.createSubModel(shell.getIdentification(), documentationSubmodel);
	}
 
	/**
	 * Starts an empty registry at "http://localhost:4000"
	 */
	private static void startRegistry() {
		BaSyxContextConfiguration contextConfig = new BaSyxContextConfiguration(4000, "/registry");
		BaSyxRegistryConfiguration registryConfig = new BaSyxRegistryConfiguration(RegistryBackend.INMEMORY);
		RegistryComponent registry = new RegistryComponent(contextConfig, registryConfig);
 
		// Start the created server
		registry.startComponent();
	}
 
	/**
	 * Startup an empty server at "http://localhost:4001/"
	 */
	private static void startAASServer() {
		BaSyxContextConfiguration contextConfig = new BaSyxContextConfiguration(4001, "/aasServer");
		BaSyxAASServerConfiguration aasServerConfig = new BaSyxAASServerConfiguration(AASServerBackend.INMEMORY, "", REGISTRYPATH);
		AASServerComponent aasServer = new AASServerComponent(contextConfig, aasServerConfig);
 
		// Start the created server
		aasServer.startComponent();
	}
}
```

This is the server class. Its main method starts an AAS server and a Registry server. The AAS server gets populated by an AAS and a Submodel, which contains the Property “maxTemp” with the value 1000.

## Expected Output

First there will be some info about the registry which will be an InMemoryRegistry, followed by info (maybe in a red text color) about the BaSyx Context and HTTP server (a Tomcat server) which has been started. In between this output there will be information about the registry server and the AASServerComponent. If the server started correctly the last line will be **AASRegistryProxy - AAS with Id eclipse.basyx.aas.oven created.**

```
16:05:54.907 [main] INFO  o.e.b.c.r.RegistryComponent - Loading InMemoryRegistry
...
16:05:55.411 [main] INFO  o.e.b.c.r.RegistryComponent - Registry server started
16:05:55.416 [main] INFO  o.e.b.c.a.AASServerComponent - Create the server...
16:05:55.442 [main] INFO  o.e.b.c.a.AASServerComponent - Registry loaded at "http://localhost:4000/registry"
16:05:55.442 [main] INFO  o.e.b.c.a.AASServerComponent - Using InMemory backend
16:05:55.444 [main] INFO  o.e.b.c.a.AASServerComponent - Start the server
...
16:05:55.819 [main] INFO  o.e.b.a.r.p.AASRegistryProxy - AAS with Id eclipse.basyx.aas.oven created
```

## Client Class

```java
import org.eclipse.basyx.aas.manager.ConnectedAssetAdministrationShellManager;
import org.eclipse.basyx.aas.registration.proxy.AASRegistryProxy;
import org.eclipse.basyx.submodel.metamodel.api.ISubmodel;
import org.eclipse.basyx.submodel.metamodel.api.submodelelement.ISubmodelElement;
 
public class Client {
	public static void main(String[] args) {
		// Create Manager
		ConnectedAssetAdministrationShellManager manager =
				new ConnectedAssetAdministrationShellManager(new AASRegistryProxy(Server.REGISTRYPATH));
 
		// Retrieve submodel
		ISubModel submodel = manager.retrieveSubModel(Server.OVENAASID, Server.DOCUSMID);
 
		// Retrieve MaxTemp Property
		ISubmodelElement maxTemp = submodel.getSubmodelElement(Server.MAXTEMPID);
 
		// Print value
		System.out.println(maxTemp.getIdShort() + " is " + maxTemp.getValue());
	}
}
```

This is the second part of the “Hello World” example, the client. It connects to the AAS server started in the first part of this project and retrieves the Submodel. Next, it prints the *idShort* of the contained Property and its value to the console.

## Expected Output
If the client is successful in connecting to the server and retrieving the Submodel, its output will show the maxTemp value.

```
maxTemp is 1000
```