# Multiple Data Sinks

The Databridge supports the configuration of multiple data sinks per route also including the transformation per sink. This allows for a flexible and powerful data routing mechanism, enabling users to direct data to various endpoints with specific transformations applied as needed.

## Configuration

To configure multiple data sinks, you can define them in the `routes.json` file under the `datasinks` section. Each sink can have its own transformation rules, allowing for tailored data processing.

This is what an example configuration might look like for one route:

```json
[
    {
        "datasource": "EnvironmentalSensorMQTT",
        "transformers": [
            "TemperatureTransformer",
            "HumidityTransformer",
            "AirQualityTransformer"
        ],
        "datasinks": [
            "TemperatureAAS",
            "HumidityAAS",
            "AirQualityAAS"
        ],
        "datasinkMappingConfiguration":
		{
			"TemperatureAAS": ["TemperatureTransformer"],
			"HumidityAAS": ["HumidityTransformer"],
			"AirQualityAAS": ["AirQualityTransformer"]
		},
        "trigger": "event"
    }
]
```

## Working Example

You can find an example that you can try out yourself in the [examples directory](https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxDatabridge) on our GitHub repository. This example demonstrates how to set up multiple data sinks with different transformations applied to each sink for a simple MQTT data source. Please follow the instructions in the README file of the example to run the scenario.
