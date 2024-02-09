# Health Endpoint
## User Story & Use Case
*As BaSyx components administrator*

*I want a health endpoint for AAS Registry and AAS Server*

*so that I can easily check the healthiness of the used components*

In various contexts, a health endpoint indicating the healthiness of the components is beneficial. For example, it can be utilized for waiting for component startup. Additionally, it can be used in kubernetes as container probes and thus automatically handle container failure.

## Feature Overview
All BaSyx components expose the */health* endpoint at their configured HTTP context. For example, if the AAS Server is running at http://localhost:8081/aasServer/shells/, the respective health endpoint can be accessed via http://localhost:8081/health. If the component is healthy, it will return the HTTP status code *200 OK*.

In the following, an excerpt of a compose.yml file is given where the 'examplecontainer' waits for the 'aas' container startup indicated by the healthcheck using wget and the health endpoint.
```
version: '3.8'
services:
  examplecontainer:
    # image etc. omitted
    depends_on:
      aas:
        condition: service_healthy

  aas:
    # image etc. omitted
    healthcheck:
      test: wget --no-verbose --tries=1 --spider aas:4001/health || exit 1
      interval: 5s
      retries: 3
      start_period: 1s
      timeout: 10s
```
## Feature Configuration
The feature is enabled by default. No additional configuration is necessary.