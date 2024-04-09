# MongoDB Configuration
The component's MongoDB configuration can be used to specify the MongoDB database and its used collection names for the containers.

## Default Configuration
By default, a MongoDB database is assumed with the default port and credentials:

```
dbuser			        = admin
dbname			        = admin
dbconnectionstring	    = mongodb://localhost:27017/
dbcollectionRegistry	= registry
dbcollectionAAS		    = assetadministrationshells
dbcollectionSubmodels	= submodels
```
The collection names are used by the [AAS Server Component](../../../basyx_components/v1/aas-server/index.md)and the [Registry Component](../../../basyx_components/v1/registry/index.md) to specifiy the collection within the MongoDB to store the AAS, submodels and registry entries.

## Custom Configuration
For docker components, the mongodb.properties file can be mounted inside of the container using a volume during container startup. E.g., to run the registry component with custom configuration, use
```
docker run --name=registry -p 8082:4000 -v C:/tmp:/usr/share/config eclipsebasyx/aas-registry:latest
```
The **mongodb.properties** file has to be located in C:/tmp in this example.

In order to change the MongoDB configuration when directly starting the component from the Java executable, you can specifiy the configuration file path via the **BASYX_MONGODB** parameter. See the following example with the registry:
```
java -jar -DBASYX_MONGODB="C:/tmp/mongodb.properties" registry.jar
```