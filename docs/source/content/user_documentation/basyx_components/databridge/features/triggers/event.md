# Event
The Event trigger is used to generate message exchanges whenever an event occurs. This trigger is used when the data source produces data asynchronously for e.g. when an MQTT message is published on a topic then the route would start processing.

## Configuration
You can specify **"trigger": "event"** in **routes.json**.

### Sample Route Configuration with Event
```
[
	{
		"routeId": "namedRoute",
		"datasource": "property1",
		"transformers": ["jsonataA"],
		"datasinks": ["ConnectedSubmodel/ConnectedPropertyA"],
		"trigger": "event"
	}
]
```
## Working Example
The integration example with **event triggered** MQTT as a data source, JSONata as a transformer, and AAS as a data sink is available on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.opcua-jackson-jsonata-aas).