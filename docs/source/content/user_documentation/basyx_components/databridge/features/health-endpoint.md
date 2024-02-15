# Health Endpoint
## User Story & Use Case
>As BaSyx components administrator
>I want a health endpoint for DataBridge component
>so that I can easily check the healthiness of the used components

In various contexts, a health endpoint indicating the healthiness of the components is beneficial. For example, it can be utilized for waiting for a component startup. Additionally, it can be used in Kubernetes as container probes and thus automatically handle container failure.

## Feature Overview
All BaSyx components expose the */health* endpoint at their configured HTTP context. For example, if the DataBridge component is running at *http://localhost:8085*, the respective health endpoint can be accessed via *http://localhost:8085/health*. If the component is healthy, it will return the HTTP status code *200 OK* with a response body containing the detailed status of context and routes as a JSON.

### Sample Response Body
```
[
    {
        "message": "",
        "details": {
            "invocation.count": 2,
            "context.name": "camel-1",
            "success.count": 2,
            "invocation.time": "2023-01-30T11:02:54.119537Z[Etc/UTC]",
            "context.version": "3.14.0",
            "context.status": "Started",
            "failure.count": 0
        },
        "state": "UP"
    },
    {
        "message": "",
        "details": {
            "route.id": "app.health.context",
            "invocation.count": 2,
            "route.context.name": "camel-1",
            "success.count": 2,
            "invocation.time": "2023-01-30T11:02:54.119709Z[Etc/UTC]",
            "route.status": "Started",
            "failure.count": 0
        },
        "state": "UP"
    },
    {
        "message": "",
        "details": {
            "route.id": "route1",
            "invocation.count": 2,
            "route.context.name": "camel-1",
            "success.count": 2,
            "invocation.time": "2023-01-30T11:02:54.119845Z[Etc/UTC]",
            "route.status": "Started",
            "failure.count": 0
        },
        "state": "UP"
    }
]
```
In the following, an excerpt of a compose.yml file is given where the 'examplecontainer' waits for the 'databridge' container startup indicated by the healthcheck using wget and the health endpoint.
```yaml
version: '3.8'
services:
  examplecontainer:
    # image etc. omitted
    depends_on:
      databridge:
        condition: service_healthy

  databridge:
    # image etc. omitted
    healthcheck:
      test: wget --no-verbose --tries=1 databridge:8085/health || exit 1
      interval: 20s
      retries: 3
      start_period: 10s
      timeout: 10s
```
<span style="color:red">Disclaimer: The health endpoint defined above is restricted to GET requests only, so please don't use the **--spider** option with **wget**. The **--spider** option in the **wget** command sends an HTTP HEAD request to the server instead of a GET request.</span>

Feature Configuration
The feature is enabled by default and is available on port **8085** only. No additional configuration is necessary.