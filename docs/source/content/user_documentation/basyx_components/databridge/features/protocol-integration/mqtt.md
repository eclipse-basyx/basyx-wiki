# MQTT
The MQTT broker can be integrated with DataBridge. The paho component provides a connector for the MQTT messaging protocol using the Eclipse Paho library.

## Configuration
To configure MQTT source in DataBridge you need to provide the **unique id**, and the MQTT broker server details like **host, port,** and the **topic**.

### Sample Configuration
```
[
	{
		"uniqueId": "property1",
		"serverUrl": "localhost",
		"serverPort": 1884,
		"topic": "Properties"
	}
]
```
Similarly, you can configure multiple MQTT brokers inside the configuration file.

## Naming Convention
The name of the MQTT configuration file should be **mqttconsumer.json.** 

## Working Example
The integration example with MQTT as a data source, JSONata as a transformer, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.mqtt-jsonata-aas).