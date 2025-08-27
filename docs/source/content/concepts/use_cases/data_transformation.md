# Data Transformation

In many industrial scenarios, raw data coming from sensors and assets requires processing before it can be effectively used in Digital Twins. This is where data transformation becomes crucial. By applying various transformation techniques such as format conversion, data validation, calculations, and filtering, raw data can be converted into meaningful information suitable for specific applications or analyses.

Node-RED, a powerful flow-based development tool, serves as an excellent middleware solution for data transformation in the BaSyx ecosystem. It provides a visual programming environment that allows users to create sophisticated data processing pipelines with ease.

This section demonstrates how Node-RED can be integrated with BaSyx components to create a robust data transformation pipeline that processes MQTT sensor data before storing it in an Asset Administration Shell.

```{note}
The example can be found on in the <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxNodeRED" target="_blank">Examples on GitHub</a>. Feel free to try it out yourself!
```

## Data Transformation Architecture

The following diagram illustrates the data flow from an MQTT client through Node-RED for transformation, before being stored in the AAS Environment:

```{uml} charts/data_transformation.puml
```

### Detailed Transformation Process

The sequence diagram below shows the step-by-step process of how Node-RED receives, transforms, and forwards data:

```{uml} charts/nodered_sequence.puml
```

## Key Benefits of Node-RED for Data Transformation

- **Visual Programming**: Create data flows using a drag-and-drop interface
- **Extensive Library**: Access to thousands of pre-built nodes for various protocols and services
- **Real-time Processing**: Handle streaming data with low latency
- **Flexible Transformations**: Apply complex logic, calculations, and data manipulations
- **Protocol Bridge**: Convert between different communication protocols (MQTT, HTTP, OPC-UA, etc.)
- **Error Handling**: Built-in mechanisms for handling data validation and error scenarios

```{include} /_external/basyx-java-server-sdk/examples/BaSyxNodeRED/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxNodeRED
:relative-images:
```

## Additional Resources

For more information about data transformation with BaSyx:

- [BaSyx Components Documentation](../../user_documentation/basyx_components/index.md)
- [Device Integration Concepts](../../user_documentation/concepts%20and%20architecture/device_integration.md)
