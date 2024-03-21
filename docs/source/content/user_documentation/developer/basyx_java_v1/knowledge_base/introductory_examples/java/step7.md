### Enable MQTT eventing on the AAS Server and Registry
In order to enable MQTT eventing you have to configure the Docker container.

To do that, you have to configure the mqtt.properties, the aas.properties file of the AAS Server Component, and the mqtt.properties and the registry.properties for the Registry Component.

The best way to do that, is to copy the configuration files in a separate folder on your system ( e.g. C:\tmp\aas and C:\tmp\registry )

A more detailed documentation for the configuration of the Off-the-Shelf Components can be found here

In this example all the .properties files are in C:\tmp\aas for the AAS Component and in C:\tmp\registry for the Registry Component.


In the aas.properties you have to change the value aas.events as following:
```
# #############################
# MQTT
# #############################
# Possible to enable MQTT events
#aas.events=NONE
aas.events=MQTT
```

In the registry.properties you have to change the value registry.events as following:
```
# #############################
# MQTT
# #############################
# Possible to enable MQTT events
#registry.events=NONE
registry.events=MQTT
```
In the mqtt.properties you have to configure the server address and, if needed, Username and Password for authentication.

**Note**: `You need to configure the mqtt.properties for both, AAS Component and Registry.`

You also have the ability to configure persistency as: File or InMemory.

**Note**: `InMemory is non-persistent`

To run the AAS Server container with the according configuration, execute:
```
docker run -v C:\tmp\aas:/usr/share/config --name=aas -p 8081:4001 eclipsebasyx/aas-server:1.2.0
```

Same with the Registry Server:
```
docker run -v C:\tmp\registry:/usr/share/config --name=registry -p 8082:4000 eclipsebasyx/aas-registry:1.2.0
```

## Available Topics for subscribing
A list of available Topics can be found [here](../../developer/extensions/eventing.md)

Now you have the AAS Server and Registry connected to your MQTT Broker.