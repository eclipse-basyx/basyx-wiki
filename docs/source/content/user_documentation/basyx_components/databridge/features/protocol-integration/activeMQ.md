# Active MQ
The ActiveMQ broker can be integrated with DataBridge. When the message on the configured topic is published the route would process the data.

## Configuration
To configure ActiveMQ consumer in DataBridge you need to provide the **unique id**, and the ActiveMQ server details like h**ost, port,** and the **queue** i.e. the topic.

### Sample Configuration
```
[
	{
		"uniqueId": "property1",
		"serverUrl": "127.0.0.1",
		"serverPort": 61616,
		"queue": "first-topic"
	}
]
```
Similarly, you can configure multiple ActiveMQ consumers inside the configuration file.

## Naming Convention
The name of the ActiveMQ consumer configuration file should be **activemqconsumer.json**.

## Working Example
The integration example with ActiveMQ as a consumer, JsonAta as a transformer, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.activemq-jsonata-aas).