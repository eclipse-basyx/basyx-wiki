# AAS Data Sink
The AAS Server can be integrated with DataBridge. The AAS component can be configured as a Data Sink in the DataBridge.

## Configuration
To configure AAS Server in DataBridge you need to provide the **unique id, endpoint of the Submodel, idShort path** and the **api** type. Supported API types are <span style="color:red"> BaSyx </span> for DotAAS V2.1 or <span style="color:red"> DotAAS-V3 </span> for Dot AAS V3.

### Sample Configuration Dot AAS V2.1
```
[
	{
		"uniqueId": "ConnectedSubmodel/ConnectedPropertyA",
		"submodelEndpoint": "http://localhost:4001/shells/TestUpdatedDeviceAAS/aas/submodels/ConnectedSubmodel/submodel",
		"idShortPath": "ConnectedPropertyA",
                "api": "BaSyx"
	}
]
```
### Sample Configuration Dot AAS V3
```
[
	{
		"uniqueId": "ConnectedTestSubmodel/DotAASV3ConformantApiSMC/DotAASV3ConformantApiProperty",
		"submodelEndpoint": "http://localhost:4001/submodels/c3VibW9kZWxJZA==",
		"idShortPath": "DotAASV3ConformantApiSMC.DotAASV3ConformantApiProperty",
		"api": "DotAAS-V3"
	}
]
```
In the **submodelEndpoint**, the **c3VibW9kZWxJZA==** is the Base64 encoded identifier of the Submodel. As per the DotAAS-V3 specification the **idShortPath** should be dot-separated as shown in the configuration above.

**Note:**

* The default api type is Dot AAS V1 (**BaSyx**).
* The attribute **uniqueId** is an arbitrary unique identifier.

Similarly, you can configure multiple AAS sinks inside the configuration file.

## Naming Convention
The name of the AAS configuration file should be **aasserver.json**.

## Working Example
The integration example with MQTT as a data source, JSONata as a transformer, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.mqtt-jsonata-aas).