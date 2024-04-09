# Json Jackson
The Json Jackson transformer can be integrated with DataBridge. Jackson is a Data Format that uses the [Jackson Library](https://github.com/FasterXML/jackson-core).

## Configuration
To configure Json Jackson transformer in DataBridge you need to provide the **unique id**, the **operation** you want to perform, and **Jackson modules**.

### Sample Configuration
```
[
	{
		"uniqueId": "dataValueToJson",
		"operation": "marshal",
		"jacksonModules": "com.fasterxml.jackson.datatype.jsr310.JavaTimeModule"
	}
]
```
For other Jackson modules please refer [Jackson Modules](https://github.com/FasterXML/jackson-modules-java8).

<span style="color:red">Disclaimer: Please use only fully qualified name (FQN) in the **jacksonModules**.</span>

<span style="color:green">To use custom Jackson modules com.fasterxml.jackson.databind.Module specified as a String with FQN class names. Multiple classes can be separated by comma. Refer [Jackson Options](https://camel.apache.org/components/3.14.x/dataformats/json-jackson-dataformat.html#_jackson_options)</span>

## Naming Convention
The name of the Json Jackson configuration file should be **jsonjacksontransformer.json**.

## Working Example
The integration example with timer triggered OPC UA as a data source, with two transformers JSONata and **Json Jackson**, and AAS as a data sink is on [GitHub DataBridge Example](https://camel.apache.org/components/3.14.x/dataformats/json-jackson-dataformat.html#_jackson_options).