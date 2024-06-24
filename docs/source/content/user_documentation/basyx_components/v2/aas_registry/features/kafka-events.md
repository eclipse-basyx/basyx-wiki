# Kafka Events

This registry storage implementation uses [Apache Kafka](https://kafka.apache.org/) as event sink. Include this dependency if you want to use this storage implementation:

```xml

	<dependency>
		<groupId>org.eclipse.digitaltwin.basyx</groupId>
		<artifactId>basyx.aasregistry-kafka-events</artifactId>
	</dependency>
```

Once included, you can activate it by setting the active profile:
```
 -Dspring.profiles.active=kafkaEvents,inMemory
```

You also have to set the kafka bootstrap servers.

You can set the bootstrap property either like this:
```
-Dspring.kafka.bootstrap-servers=PLAINTEXT://kafka:29092
```

Or by using the Docker environment variable:
```
KAFKA_BOOTSTRAP_SERVERS=PLAINTEXT://kafka:29092
```