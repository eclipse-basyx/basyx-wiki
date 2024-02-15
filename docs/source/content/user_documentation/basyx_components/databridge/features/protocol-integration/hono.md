# Hono
The Hono source can be integrated with DataBridge.

## Configuration
To configure Hono consumer in DataBridge you need to provide the **unique id**, and the Hono server details like **host, port**, along with **user credentials**, **tenant id** and **device id**.

### Sample Configuration
```
[
	{
		"uniqueId": "property1",
		"serverUrl": "http://hono.eclipseprojects.io",
		"serverPort": 15672,
		"userName": "consumer@HONO",
		"password": "verysecret",
		"tenantId": "mytenantid",
		"deviceId": "mytenantdevice"
	}
]
```
Similarly, you can configure multiple Hono consumers inside the configuration file.

## Naming Convention
The name of the Hono consumer configuration file should be **honoconsumer.json**.

## Working Example
The integration example with Hono as a data source, JsonAta as a transformer, and AAS as a data sink is on[ GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.hono-jsonata-aas).