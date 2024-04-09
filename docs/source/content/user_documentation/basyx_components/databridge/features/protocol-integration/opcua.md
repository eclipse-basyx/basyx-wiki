# OPC UA
The OPC UA client can be integrated with DataBridge. The Milo Client component provides access to OPC UA servers using the Eclipse Milo™ implementation.

## Configuration
To configure OPC UA client source in DataBridge you need to provide the **unique id**, and the OPC UA server details like **host, port, service path** along with the **node information**, and **requested publishing interval (in milliseconds)** as a query parameter. For more information on query parameters [OPC UA Client Query Parameters](https://camel.apache.org/components/3.20.x/milo-client-component.html#_query_parameters).


Please note that for using OPC UA, the route trigger type should be configured as "event"!

### Sample Configuration
```
[
	{
		"uniqueId": "doublescalar",
		"serverUrl": "127.0.0.1",
		"serverPort": 12686,
		"pathToService": "milo",
		"nodeInformation": "ns=2;s=HelloWorld/ScalarTypes/Double",
		"username": "name",
		"password": "secretPassword",
                "requestedPublishingInterval": 50
	}
]
```
**Note**: By default, the requestedPublishingInterval is 1000 milliseconds.

<span style="color:red">Disclaimer: Please note that only the query parameters i.e. **nodeInformation** and **requestedPublishingInterval** in the sample configuration are supported as of now.</span>

Similarly, you can configure multiple OPC UA client consumers inside the configuration file.

## Naming Convention
The name of the OPC UA consumer configuration file should be **opcuaconsumer.json**.

## Working Example
The integration example with event triggered OPC UA as a data source, with two transformers JSONata and Jackson, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.opcua-jackson-jsonata-aas).