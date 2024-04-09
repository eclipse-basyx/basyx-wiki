# AAS Polling Consumer
The AAS Server as a polling consumer can be integrated with the DataBridge. The AAS Polling consumer component can be configured as a Data Source in the DataBridge.

## Configuration
To configure AAS Server as a polling consumer in the DataBridge you need to provide the **unique id, endpoint of the Submodel, idShort path** and the **api** type. Supported API types are <span style="color:red"> BaSyx</span> for DotAAS V2.1 or<span style="color:red"> DotAAS-V3</span> for Dot AAS V3. It is possible to consume a single SubmodelElement and also the whole Submodel.

If the configuration contains the idShortPath attribute as empty, then the whole Submodel is consumed; otherwise, the SubmodelElement whose idShort path is provided. Please refer to the sample configurations for better understanding.

### Sample Configuration for Consuming Submodel
```
[
	{
		"uniqueId": "exampleAAS1",
		"submodelEndpoint": "http://localhost:4001/submodels/dGVsZW1ldHJ5RGF0YVN0cnVjdHVyZVRlc3Q=",
		"idShortPath": "",
                "api": "DotAAS-V3"
	}
]
```
### Sample Configuration for Consuming SubmodelElement
```
[
	{
		"uniqueId": "exampleAAS3",
		"submodelEndpoint": "http://localhost:4001/shells/TestUpdatedDeviceAAS/aas/submodels/telemetryDataStructureTest/submodel",
		"idShortPath": "pressure",
                "api": "BaSyx"
	}
]
```
In the api type DotAAS-V3 configuration for **submodelEndpoint** attribute, the **dGVsZW1ldHJ5RGF0YVN0cnVjdHVyZVRlc3Q=** is the Base64 encoded identifier of the Submodel.

**Note:**

The default api type is Dot AAS V2.1 (**BaSyx**).
The attribute **uniqueId** is an arbitrary unique identifier.

Similarly, you can configure multiple AAS polling consumers inside the configuration file.

## Naming Convention
The name of the AAS polling consumer configuration file should be **aaspollingconsumer.json.**

## Working Example
The integration example with **AAS** as a data source, JSONata as a transformer, and MQTT as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.aas-jsonata-mqtt).