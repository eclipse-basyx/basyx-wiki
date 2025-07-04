# Request
The Request trigger is used to generate message exchanges on demand. The routes would be triggered when a request is made on the configured REST endpoint and the processed data will be returned as a response.

## Configuration
You can specify **"trigger": "request"** in **routes.json**. Apart from this, you have to specify the trigger data in **routes.json**. This trigger data comprises of the **host, port,** and the service **path**, basically this would be the endpoint when requested, triggers the specified route, and return the processed data as a response.

### Sample Route Configuration with Timer
```
[
	{
		"datasource": "httpsource",
		"transformers": [
			"jsonataA"
		],
		"trigger": "request",
		"triggerData": {
			"host": "localhost",
			"port": "8090",
			"path": "/valueA"
		}
	}
]
```
<span style="color:red">Disclaimer: The endpoint configured with trigger data accepts only the GET request.</span>

## Working Example
The integration example with **request triggered** HTTP as a data source, JsonAta as a transformer is available on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.httppolling-jsonata-delegator).