# SQL Submodel Provider 

## Servlet

The SQL sub model provider provides the contents of a SQL database as Asset Administration Shell sub model. It uses JDBC drivers to access the data base. Therefore, most JDBC compatible data base backends will work with this provider class. The SQL sub model provider supports configuration of sub model properties and operations through its configuration file. For properties, the VAB operations create, update, retrieve, and delete may be configured and mapped to SQL statements. The mapping of sub model operations to SQL statements are configured through the configuration file of the SQL sub model provider as well. The SQL sub model provider is implemented by servlet class `org.eclipse.basyx.components.servlets.SQLSubModelProviderServlet.` It accepts the following configuration parameter:

config: Path to configuration file
The following snippet illustrates an Apache Tomcat configuration for the SQL sub model provider Example_SQLProvider. It configures the location of the configuration file inside the WEB-INF folder and configures the URL pattern that is used to access the sub model to /Testsuite/components/BaSys/1.0/provider/sqlsm/*

```html
<servlet>
    <servlet-name>Example_SQLProvider</servlet-name>
    <servlet-class> org.eclipse.basyx.components.servlets.SQLSubModelProviderServlet </servlet-class>
 
    <init-param>
        <param-name>config</param-name>
        <param-value>/WEB-INF/config/sqlprovider/sampledb.properties</param-value>
    </init-param>
 
    <load-on-startup>5</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>Example_SQLProvider</servlet-name>
    <url-pattern>/Testsuite/components/BaSys/1.0/provider/sqlsm/*</url-pattern>
  </servlet-mapping>
```

## Configuration

The main configuration file of the SQL sub model provider contains the sub model ID, the database configuration and access credentials, the SQL driver configuration, and the configuration of the exported sub model. The following keys are supported for the configuration file:

| basyx.submodelID     | ID of sub model                                                            |
|----------------------|----------------------------------------------------------------------------|
| basyx.sql.dbuser     | Database user name that will be used by the SQL sub model provider         |
| basyx.sql.dbpass     | Database password                                                          |
| basyx.sql.dburl      | URL to the data base                                                       |
| basyx.sql.driver     | Java class that implements the JDBC driver                                 |
| basyx.sql.prefix     | Prefix for the JDBC driver                                                 |
| basyx.sql.properties | Sub model properties that are to be exported by the SQL sub model provider |
| basyx.sql.operations | -                                                                          |

The SQL sub model provider understands the following configuration values for each configured property:

| <propertyName>.type              | Type of the property                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------|
| <propertyName>.semanticsInternal | Identifier that identifies the semantics of the property.                                   |
| <propertyName>.category          | Property category value that describes for example which elements are to be expected or not |
| <propertyName>.description       | Human readable property description                                                         |
| <propertyName>.qualifier         | Namespace qualifier of the property                                                         |
| <propertyName>.get               | SQL statement that implements the property get/retrieve operation                           |
| <propertyName>.get.type          | Return type of the SQL statement                                                            |
| <propertyName>.get.result        | Provider operation that converts the SQL result into a conforming VAB/AAS data type         |
| <propertyName>.delete            | SQL statement that implements the property delete operation                                 |
| <propertyName>.create            | SQL statement that implements the property create operation                                 |
| <propertyName>.set               | SQL statement that implements the property set/update operation                             |

Most SQL operations require parameter. The SQL sub model provider supports the definition of named SQL parameter. For example, a create operation could be defined as following:

`sensorNames.create = "INSERT INTO vibrations.sensors (sensorname, sensorid) VALUES ('$sensorname', '$sensorid')"`

Values $sensorname and $sensorid must be provided as JSON serialized map:

```java
Map<String, Object> newTableLine = new HashMap<>();
newTableLine.put("sensorname", "VS_0003");
newTableLine.put("sensorid",   "033542");
```

The BaSyx SDK supports the conforming serialization of the Map as JSON object and realizes the web service call via HTTP REST. However, all of this may also be implemented manually if preferred:

```java
// - Insert line into table
connSubModel.createElement("/aas/submodels/SQLTestSubmodel/properties/sensorNames/value", newTableLine);
```

## Configuration Example
The following example file illustrates the configuration of the SQL sub model provider:

```sql
# ##############################################################
# SQL Sub model provider configuration file
# ##############################################################
 
# ##############################################################
# Sub model provider configuration
 
basyx.submodelID    = SQLTestSubmodel
 
# ##############################################################
# Database configuration
 
basyx.sql.dbuser   = postgres
basyx.sql.dbpass   = admin
basyx.sql.dburl    = //localhost/basyx-sample-vibrations?
 
# ##############################################################
# SQL driver configuration
 
basyx.sql.driver   = org.postgresql.Driver
basyx.sql.prefix   = jdbc:postgresql:
 
# ##############################################################
# SQL sub model configuration
 
basyx.sql.properties          = sensorNames 
basyx.sql.operations          = sensorIDForName addSensorID
 
# ##############################################################
# Properties
 
# sensorNames property
sensorNames.type              = PropertySingleValued
sensorNames.semanticsInternal = basys.semantics.internal.sensorNames
sensorNames.category          = sensorNamesProperty
sensorNames.description       = Sensor names property description
sensorNames.qualifier         = basys.test.sensorNamesScope
 
sensorNames.get               = "SELECT * FROM vibrations.sensors"
sensorNames.get.type          = STRING[]
sensorNames.get.result        = "stringArray(sensorname:String)"
 
sensorNames.delete            = "DELETE FROM vibrations.sensors WHERE sensorid='$sensorid'"
 
sensorNames.create            = "INSERT INTO vibrations.sensors (sensorname, sensorid) VALUES ('$sensorname', '$sensorid')"
 
sensorNames.set               = "UPDATE vibrations.sensors SET sensorname='$sensorname' WHERE sensorid='$sensorid'"
 
 
# ##############################################################
# Operations
 
# sensorIDForName operation
sensorIDForName.operation.parameter     = 1
sensorIDForName.operation.kind          = query
sensorIDForName.operation.type          = OBJECT[]
sensorIDForName                         = "SELECT * FROM vibrations.sensors WHERE sensorname='$1'"
sensorIDForName.operation.result        = "mapArray(sensorid:int, sensorname:String)"
 
# addSensorID operation
addSensorID.operation.parameter         = 2
addSensorID.operation.kind              = update
addSensorID.operation.type              = void
addSensorID                             = "INSERT INTO vibrations.sensors ($1) VALUES ($2)"
addSensorID.operation.result            =
```

## Java Example

The following code snippets illustrate the SQL sub model provider use from the JAVA SDK.

* Connect to SQL sub model provider via directory service. The SQL sub model provider is available with ID SQLTestSubmodel.
```java
// Connect to sub model "CfgFileTestAAS"
VABElementProxy connSubModel = this.connManager.connectToVABElement("SQLTestSubmodel");
```

* Read value of sensorNames property that contains all sensor names
```java 
// Get property value
Object value1 = connSubModel.readElementValue("/aas/submodels/SQLTestSubmodel/properties/sensorNames/value");
```

* Read meta data “category” of sensorNames property
```java
// Get property meta data value
Object value5 = connSubModel.readElementValue("/aas/submodels/SQLTestSubmodel/properties/sensorNames/category");
```

* Read sensorNames property that contains all meta data. The property value is provided in the value attribute.
```java
Object value1a = connSubModel.readElementValue("/aas/submodels/SQLTestSubmodel/properties/sensorNames");
```

* The call returns the following JSON serialized data structure:
```yaml
  { id_semantics               = {idType=2, id=basys.semantics.internal.sensorNames}, 
    parent                     = null, 
    idShort                    = sensorNames, 
    kind                       = 1, 
    qualifier                  = [basys.test.sensorNamesScope], 
    description                = Sensor names property description, 
    category                   = sensorNamesProperty, 
    hasFullSemanticDescription = [], 
    value                      = [VS_0001, VS_0002]
  }
```

* Invoke operation sensorIDForName to resolve sensor ID of sensor named VS_0001.
```java
// Get property value (1)
Object value1 = connSubModel.invoke("/aas/submodels/SQLTestSubmodel/operations/sensorIDForName", "VS_0001");
System.out.println("Value:"+value1);
```

* Invoke operation that adds a sensor with name VS_0005 and id 321.
```java 
connSubModel.invoke("/aas/submodels/SQLTestSubmodel/operations/addSensorID", "sensorname, sensorid", "'VS_0005', '321'");
```

* Create a new sensor using the VAB create primitive <<<cf: VAB primitives>>> on the sensorNames property
```java
// Create a new property
// - HashMap that contains new table line
Map<String, Object> newTableLine = new HashMap<>();
	newTableLine.put("sensorname", "VS_0003");
	newTableLine.put("sensorid",   "033542");
 
// - Insert line into table
connSubModel.createElement("/aas/submodels/SQLTestSubmodel/properties/sensorNames/value", newTableLine);
```

* Delete sensor with ID VS_0005.
```java
// Delete property 'VS_0005'
// - Collection that contains call values
Collection<String> callValues4 = new LinkedList<>();
callValues4.add("VS_0005");
// - Delete sensor from table
connSubModel.deleteElement("/aas/submodels/SQLTestSubmodel/properties/sensorNames", callValues4);
```

* Update sensor with ID 033542 to name VS_0004.
```java
// Update property value
// - Here this adds a new value into the table
// - Collection that contains call values
Map<String, Object> updatedTableLine = new HashMap<>();
	updatedTableLine.put("sensorname", "VS_0004");
	updatedTableLine.put("sensorid", "033542");
// - Update table line
connSubModel.updateElementValue("/aas/submodels/SQLTestSubmodel/properties/sensorNames/value", updatedTableLine);
```