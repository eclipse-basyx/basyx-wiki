# Step 6: Creating an example application
In the last example, the AAS was set up and registered. Its contents can be explored through the HTTP-Rest API.
```
In the browser, look at the various endpoints to see what is returned:
To access the AAS: http://localhost:4000/handson/oven/aas/
To access the oven Submodel: http://localhost:4000/handson/oven/aas/submodels/oven/
```

The registry also has a HTTP-REST interface. So, it is possible to directly query it:
```
Show all AAS: http://localhost:4000/handson/registry/api/v1/registry/
Show my AAS: http://localhost:4000/handson/registry/api/v1/registry/urn:org.eclipse.basyx:OvenAAS
```

However, in a real application this exploration and data retrieval should not happen through manual calls but instead through interfaces encapsulating the access. The following example shows how to use the provided interfaces and how to alternatively access the AAS directly through the VAB.


First, to access the remote registry, a AASRegistryProxy is created. Next, a ConnectedAssetAdministrationShellManager is created using this registry proxy. This will be used to access the Asset Administration Shell. The AAS is retrieved through its unique URN from the connection manager. The connector manager gets a parameter that defines how, i.e. using which protocol, the AAS server and registry can be reached. This example uses http/REST interfaces, and therefore, the HTTPConnectorFactory will be used. The ConnectedAssetAdministrationShell will be the proxy to the remote AAS.
```java
	// Return a AASHTTPRegistryProxy for the registry on localhost at port 4000
	IAASRegistry registry = new AASRegistryProxy("http://localhost:4000/handson/registry");
 
	// Create a ConnectedAssetAdministrationShell using a ConnectedAssetAdministrationShellManager
	IConnectorFactory connectorFactory = new HTTPConnectorFactory();
	ConnectedAssetAdministrationShellManager manager = new ConnectedAssetAdministrationShellManager(registry, connectorFactory);
 
	// The ID of the oven AAS
	ModelUrn aasURN = new ModelUrn("urn:org.eclipse.basyx:OvenAAS");
	ConnectedAssetAdministrationShell connectedAAS = manager.retrieveAAS(aasURN);
```

Last, the provided interfaces and classes are used for Submodel, property and operation retrieval. The following code queries a list of Submodels.
```java
	// Connect to the AAS and read the current temperature
	// Either Create a connected property using the connected facades
	Map<String, ISubmodel> submodels = connectedAAS.getSubmodels();
```

Finally, the temperature value is retrieved and based on its unit either converted to Celsius or printed directly.
```java
	ISubmodel connectedSensorSM = submodels.get("Sensor");
	Map<String, IProperty> properties = connectedSensorSM.getProperties();
	IProperty temperatureProperty = properties.get("currentTemperature");
	double temperature = (double) temperatureProperty.getValue();
```
Now, depending on the type of the application, the information can be used for whatever is necessary. Applications may access multiple AAS and Submodels, and therefore collect and aggregate data from different sources.