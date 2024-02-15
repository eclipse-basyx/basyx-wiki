# Routes Configuration
A route is a sequence of steps, executed in order by DataBridge, that consume and process a message. A route starts with a source and is followed by a chain of endpoints and processors such as transformers and sinks. The names utilized in the route configuration have to be equal to the *uniqueIds* defined in the respective jsons.

A route in DataBridge can be configured using Json file. You can specify the Data Sources, Transformers, Data Sinks, and Route trigger. Specifying the trigger in the route instructs the DataBridge about when the route would be started. More information on different types of triggers can be found in [Features](../features/index.md) under **Route Types**.

## Sample Single Route Configuration
```yaml
[
	{
		"routeId": "namedRoute",
		"datasource": "property1",
		"transformers": ["jsonataA"],
		"datasinks": ["ConnectedSubmodel/ConnectedPropertyA"],
		"trigger": "event"
	}
]
```
The datasource, transformers, and datasinks should be defined in their respective configuration files. For details please see [Features](../features/index.md).

Similary, you can configure multiple routes.

## Sample Multiple Routes Configuration
```yaml
[
	{
		"routeId": "namedRoute",
		"datasource": "property1",
		"transformers": ["jsonataA"],
		"datasinks": ["ConnectedSubmodel/ConnectedPropertyA"],
		"trigger": "event"
	},
        {
		"datasource": "property2",
		"transformers": ["jsonataA", "jsonataB"],
		"datasinks": ["ConnectedSubmodel/ConnectedPropertyA", "ConnectedSubmodel/ConnectedPropertyB"],
		"trigger": "event"
	}
]
```
## Naming Conventions
The name of the routes configuration file should be **routes.json**.

## Working Example
There is a working example with overall [device integration](https://github.com/eclipse-basyx/basyx-java-examples/tree/main/basyx.examples.deviceintegration/src/main/resources) scenarios.