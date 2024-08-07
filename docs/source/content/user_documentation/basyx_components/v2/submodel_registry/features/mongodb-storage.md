# MongoDB Storage

This registry storage implementation uses [MongoDB](https://www.mongodb.com/) as document-store and generates a specific data model with MongoDB annotations. Include this dependency if you want to use this storage implementation:

```xml
	<dependency>
		<groupId>org.eclipse.digitaltwin.basyx</groupId>
		<artifactId>basyx.submodelregistry-service-mongodb-storage</artifactId>
	</dependency>
```

Then included, you can activate it by either setting the active profile or the *registry.type* attribute:

```
 -Dspring.profiles.active=logEvents,mongoDbStorage
```

Dont't forget to also set the mongodb url as property

```
-Dspring.data.mongodb.uri=mongodb://admin:admin@localhost:27017/
```

or use the environment variable

```
SPRING_DATA_MONGODB_URI=mongodb://admin:admin@localhost:27017/
```