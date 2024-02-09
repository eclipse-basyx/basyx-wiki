The component's MQTT configuration can be used to specify the MQTT Client data in order to connect to the right MQTT broker. It allows you to add credentials and a Quality of Service level (default: 1) besides the mandatory server address.

Information about what events will be published can be found in the [eventing extension](../../developer/extensions/eventing.md).

## Default Configuration
By default, a MQTT Client only needs a server address. If not specified in the configuration the Quality of Service level will be 1.
```
user=
pass=
server=tcp://localhost:1883
qos=1
```
## Custom Configuration
For docker components, the *mqtt.properties* file can be mounted inside of the container using a volume during container startup. E.g., to run the registry component with custom configuration, use
```
docker run --name=registry -p 8082:4000 -v C:/tmp:/usr/share/config eclipsebasyx/aas-registry:latest
```
The **mqtt.properties** file has to be located in C:/tmp in this example.

In order to change the MQTT configuration when directly starting the component from the Java executable, you can specify the configuration file path via the **BASYX_MQTT** parameter. See the following example with the registry:
```
java -jar -DBASYX_MQTT="C:/tmp/mqtt.properties" registry.jar
```
## Whitelisting
The following lines can be added to the configuration file to filter events (**only applies to an AASServer**):
```
whitelist.{mySmIdentifier}=true
whitelist.element.{mySmIdentifier}.{elementIdShort}=true
```
Whitelisting can be enabled for each submodel to restrict eventing to specific submodelElements of the given submodel. The second line defines for which elements in the submodel events are published, while the first line acts as a switch to enable the whitelisting for the given submodel.