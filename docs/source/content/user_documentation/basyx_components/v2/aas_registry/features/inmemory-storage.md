# InMemory Storage

This registry storage implementation uses in-memory hash maps as document-store and uses the [base java pojos](../basyx.aasregistry-service-basemodel) as data model. Include this dependency if you want to use this storage implementation:

```xml

	<dependency>
		<groupId>org.eclipse.digitaltwin.basyx</groupId>
		<artifactId>basyx.aasregistry</artifactId>
	</dependency>
```

Then included, you can activate it by setting the active profile:

```
 -Dspring.profiles.active=logEvents,inMemoryStorage
```