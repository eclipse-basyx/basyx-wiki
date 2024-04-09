# HTTP
The HTTP source can be integrated with DataBridge. The data from the specified HTTP endpoint is fetched, processed and then delivered to the sink.

## Configuration
To configure HTTP in DataBridge you need to provide the **unique id**, and the HTTP **serverUrl** that should be queried.

### Sample Configuration
```
[
  {
    "uniqueId": "httpsource",
    "serverUrl": "http://127.0.0.1:1234/test"
  }
]
```
Similarly, you can configure multiple HTTP consumers inside the configuration file.

## Naming Convention
The name of the HTTP consumer configuration file should be **httpconsumer.json.**

## Working Example
The integration example with HTTP as a data source, JSONata as a transformer, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.httppolling-jsonata-aas).