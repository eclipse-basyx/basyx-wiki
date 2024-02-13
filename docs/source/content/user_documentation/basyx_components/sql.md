# SQL Configuration
The component's SQL configuration can be used to specify the SQL driver and location for the SQL database.

## Default Configuration
By default, a PostgreSQL database is assumed with the default port and credentials.
```yaml
dbuser             = postgres
dbpass             = admin
dburl              = //localhost:5432/basyx-directory? 
sqlDriver          = org.postgresql.Driver
sqlPrefix          = jdbc:postgresql:
```
It is possible to use different SQL drivers by configuring the driver and connector prefix string. E.g., to connect to a Microsoft SQL server use the following configuration:
```yaml
sqlDriver          = com.microsoft.sqlserver.jdbc.SQLServerDriver
sqlPrefix          = jdbc:sqlserver:
```
## Custom Configuration
For docker components, the sql.properties file can be mounted inside of the container using a volume during container startup. E.g., to run the registry component with custom configuration, use
```
docker run --name=registry -p 8082:4000 -v C:/tmp:/usr/share/config eclipsebasyx/aas-registry:latest
```
The **sql.properties** file has to be located in C:/tmp in this example.

In order to change the SQL configuration when directly starting the component from the Java executable, you can specifiy the configuration file path via the **BASYX_SQL** parameter. See the following example with the registry:
```
java -jar -DBASYX_SQL="C:/tmp/sql.properties" registry.jar
```