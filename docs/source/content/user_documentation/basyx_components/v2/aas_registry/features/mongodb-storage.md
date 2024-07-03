# MongoDB Storage

This registry storage implementation uses [MongoDB](https://www.mongodb.com/) as document-store and generates a specific data model with MongoDB annotations. Include this dependency if you want to use this storage implementation:

```xml
	<dependency>
		<groupId>org.eclipse.digitaltwin.basyx</groupId>
		<artifactId>basyx.aasregistry-service-mongodb-storage</artifactId>
	</dependency>
```

Once included, you can activate it by setting the active profile:

```
 -Dspring.profiles.active=logEvents,mongoDbStorage
```

You also have to set the mongodb URL.

You can set it as a property like this:

```
-Dspring.data.mongodb.uri=mongodb://admin:admin@localhost:27017/
```

Or by using the Docker environment variable:

```
SPRING_DATA_MONGODB_URI=mongodb://admin:admin@localhost:27017/
```