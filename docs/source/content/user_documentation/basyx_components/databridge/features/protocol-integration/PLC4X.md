# PLC4X
The automation protocols such as Modbus, S7 leveraging **apache PLC4X** can be integrated with DataBridge. Apache PLC4X allows you to communicate directly with your industrial Hardware without retrofitting it [[1]](https://plc4x.apache.org/users/index.html). For more information please refer to [Apache PLC4X](https://plc4x.apache.org/users/getting-started/general-concepts.html)

## Configuration
To configure the PLC4X source in DataBridge you need to provide the **unique id**, the connection details like **host, port**, and the **service path** (*), **options** (*), the **driver** and the **tags**. The **driver** could be any of the drivers supported by the [PLC4X](https://plc4x.apache.org/users/protocols/index.html). For more information on the configuration please refer [Camel PLC4X](https://camel.apache.org/components/next/plc4x-component.html)

* - Optional attributes

### Sample Configuration
```
[
	{
		"uniqueId": "property1",
		"serverUrl": "localhost",
		"serverPort": 50201,
		"driver": "modbus-tcp",
		"servicePath": "",
		"options": "",
		"tags": [
			{
				"name": "value_1",
				"value": "holding-register:1"
			}
		]
	}
]
```
### Configuring Options
There are currently two supported ways for configuring the **options** for PLC4X:

#### Option Configuration 1
```
[
	{
		******same config as defined above******

		"options": "period=100&autoReconnect=true",

		******same config as defined above******
	}
]
```
#### Option Configuration 2
```
[
	{
		******same config as defined above******

		"options": [
			{
				"name": "period",
				"value": "100"
			},
                        {
				"name": "autoReconnect",
				"value": "true"
			}
		]

		******same config as defined above******
	}
]
```
Similarly, you can configure multiple PLC4X inside the configuration file.

## Naming Convention
The name of the PLC4X configuration file should be **plc4xconsumer.json**.

## Working Example
The integration example with PLC4X as a data source, Json Jackson and JSONata as a transformer, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.plc4x-jsonata-aas). and [in this article](../../../../../databridge-PLC4X.md)