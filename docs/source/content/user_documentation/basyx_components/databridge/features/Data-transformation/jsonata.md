# JSONata
The JSONata transformer can be integrated with DataBridge. The Jsonata component allows you to process JSON messages using the [JSONata](https://jsonata.org) specification. This can be ideal when doing JSON to JSON transformation and other transformations from JSON.

## Configuration
To configure JSONata transformer in DataBridge you need to provide the **unique id**, the **relative path** to the file containing JSONata expressions, **input type** and the **output type**.

### Sample Configuration
```
[
	{
		"uniqueId": "jsonataA",
		"queryPath": "jsonataA.jsonata",
		"inputType": "JsonString",
		"outputType": "JsonString"
	}
]
```
<span style="color:red">Disclaimer: Please use only the relative path (queryPath) of the file containing JSONata expressions.</span>

Below is an example expression that can be put in the **jsonataA.jsonata** file.

### Sample JSONata expression
```
$sum(Account.Order.Product.(Price * Quantity))
```
To learn more about JSONata expressions please refer [JSONata Org](https://jsonata.org)

Similarly, you can configure multiple JSONata transformers inside the configuration file.

## Naming Convention
The name of the JSONata configuration file should be **jsonatatransformer.json**.

## Working Example
The integration example with MQTT as a data source, **JSONata** as a transformer, and AAS as a data sink is available on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.mqtt-jsonata-aas).