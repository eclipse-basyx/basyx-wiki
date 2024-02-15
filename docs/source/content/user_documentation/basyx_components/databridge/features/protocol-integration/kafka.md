# Kafka
The Kafka source can be integrated with DataBridge. The Kafka component is used for communicating with the Apache Kafka message broker.

## Configuration
To configure Kafka source in DataBridge you need to provide the **unique id**, and the Kafka broker server details like **host, port**, along with other Kafka consumer query parameters like the **topic**, **maxPollRecords, groupId, consumersCount** and **seekTo**. For more information on query parameters [Kafka Query Parameters](https://camel.apache.org/components/3.20.x/kafka-component.html#_query_parameters)

### Sample Configuration
```
[
	{
		"uniqueId": "property1",
		"serverUrl": "localhost",
		"serverPort": 9092,
		"topic": "first-topic",
		"maxPollRecords": 5000,
		"groupId": "basyx-updater",
		"consumersCount": 1,
		"seekTo": "BEGINNING"
	}
]
```
<span style="color:red">Disclaimer: Please note that only the query parameters listed in the sample configuration are supported as of now.</span>

Similarly, you can configure multiple Kafka consumers inside the configuration file.

## Naming Convention
The name of the Kafka consumer configuration file should be **kafkaconsumer.json**.

## Working Example
The integration example with Kafka as a data source, JsonAta as a transformer, and AAS as a data sink is on [GitHub DataBridge Example]https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.kafka-jsonata-aas).