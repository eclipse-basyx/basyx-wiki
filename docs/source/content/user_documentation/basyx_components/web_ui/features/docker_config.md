# Docker Configuration

## User Story and Use Case

>As AAS Web UI user
>I want to preconfigure the AAS Web UI through Docker environment variables.
>I also want to be able to mount my own logo folder to display my companies logo in the AAS Web UI.

The Docker Image of the AAS Web UI can be configured through environment variables and volumes. This allows the user to preconfigure the AAS Web UI when starting the Docker container.

## Feature Overview

### Environment Variables

The following environment variables can be used to configure the AAS Web UI:

| Variable Name | Description |
|---------------|-------------|
| AAS_DISCOVERY_PATH | The path to the AAS Discovery Service |
| AAS_REGISTRY_PATH | The path to the AAS Registry |
| SUBMODEL_REGISTRY_PATH | The path to the Submodel Registry |
| AAS_REPO_PATH | The path to the AAS Repository |
| SUBMODEL_REPO_PATH | The path to the Submodel Repository |
| CD_REPO_PATH | The path to the Concept Description Repository |
| DASHBOARD_SERVICE_PATH | The path to the Dashboard Service |
| PRIMARY_COLOR | The primary color of the AAS Web UI |
| PRIMARY_LIGHT_COLOR | The primary color of the AAS Web UI of the light theme (ENV variable available starting with eclipsebasyx/aas-gui:v2-241114) |
| PRIMARY_DARK_COLOR | The primary color of the AAS Web UI of the dark theme (ENV variable available starting with eclipsebasyx/aas-gui:v2-241114) |
| LOGO_PATH | The path to the application logo inside the container `Logo/<your-logo.png>` |
| LOGO_LIGHT_PATH | The path to the application logo of the dark theme inside the container `Logo/<your-logo.png>` (ENV variable available starting with eclipsebasyx/aas-gui:v2-241114) |
| LOGO_DARK_PATH | The path to the application logo of the dark theme inside the container `Logo/<your-logo.png>` (ENV variable available starting with eclipsebasyx/aas-gui:v2-241114) |
| BASE_PATH | The base path of the AAS Web UI |
| INFLUXDB_TOKEN | The token for accessing time series data from an InfluxDB |
| KEYCLOAK_URL | The URL of the Keycloak server used as identity provider for RBAC |
| KEYCLOAK_REALM | The realm of the Keycloak server |
| KEYCLOAK_CLIENT_ID | The client ID of the Keycloak server |
| ENDPOINT_CONFIG_AVAILABLE | Specifies whether the endpoint configuration should be available in the AAS Web UI (ENV variable available starting with eclipsebasyx/aas-gui:v2-241114) |
| SINGLE_AAS | Specifies whether the aas-gui should show only one specific AAS or an List of all AAS "<true/false>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241220) |

| SINGLE_AAS_REDIRECT | Specifies a URL to which redirection should occur in the case of SINGLE_AAS = true and missing `aas` URL query parameter (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241220)

```{tip}
Using environment variables works when building the Docker image yourself or when using the image from Docker Hub.
```

This is how you would use the environment variables when building the Docker image yourself:

1. Build the Docker image from the Dockerfile in the [aas-web-gui](https://github.com/eclipse-basyx/basyx-applications/tree/main/aas-gui/Frontend/aas-web-gui) directory of the AAS Web UI repository:
<br/><sup>Note: If you are behind a proxy, you have to set the shell ENV variable HTTP_PROXY respectively HTTPS_PROXY; see [bootstrap.sh](https://github.com/eclipse-basyx/basyx-aas-web-ui/blob/main/bootstrap.sh).</sup>

  ```bash
  docker build -t aas-web-ui .
  ```
  

2. Start the Docker container with the following command (replace the environment variables with your own values; only an excerpt of the variables are specified in the following example):

  ```bash
  docker run -p 3000:3000 --name=aas-web-ui -e AAS_DISCOVERY_PATH="<discovery_path>" -e AAS_REGISTRY_PATH="<aas_registry_path>" -e SUBMODEL_REGISTRY_PATH="<submodel_registry_path>" -e AAS_REPO_PATH="<aas_repo_path>" -e SUBMODEL_REPO_PATH="<submodel_repo_path>" -e CD_REPO_PATH="<concept_description_repo_path>" aas-web-ui
  ```

This is how you would configure the environment variables when using the AAS Web UI with Docker Compose and the image from Docker Hub:

1. Create a `docker-compose.yml` file in your project directory and add the following content (replace the environment variables with your own values):

```yaml
services:
    aas-web-ui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-ui
        ports:
            - "3000:3000"
        environment:
            AAS_DISCOVERY_PATH: "<discovery_path>" (optional)
            AAS_REGISTRY_PATH: "<aas_registry_path>"
            SUBMODEL_REGISTRY_PATH: "<submodel_registry_path>"
            AAS_REPO_PATH: "<aas_repo_path>"
            SUBMODEL_REPO_PATH: "<submodel_repo_path>"
            CD_REPO_PATH: "<concept_description_repo_path>"
            DASHBOARD_SERVICE_PATH: "<dashboard_service_path>" (optional; Time Series Data)
            PRIMARY_COLOR: "<primary_color>" (optional; Corporate Design)
            PRIMARY_LIGHT_COLOR: "<primary_light_color>" (optional; Corporate Design light theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            PRIMARY_DARK_COLOR: "<primary_dark_color>" (optional; Corporate Design dark theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            LOGO_PATH: "<logo_path_in_container>" (optional; Corporate Design)
            LOGO_LIGHT_PATH: "<logo_light_path_in_container>" (optional; Corporate Design light theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            LOGO_DARK_PATH: "<logo_dark_path_in_container>" (optional; Corporate Design dark theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            BASE_PATH: "<base_path>" (optional)
            INFLUXDB_TOKEN: "<influxdb_token>" (optional; Time Series Data)
            KEYCLOAK_URL: "<keycloak_url>" (optional; RBAC feature)
            KEYCLOAK_REALM: "<keycloak_realm>" (optional; RBAC feature)
            KEYCLOAK_CLIENT_ID: "<keycloak_client_id>" (optional; RBAC feature)
            ENDPOINT_CONFIG_AVAILABLE: "<true/false>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            SINGLE_AAS: "<true/false>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241220)

            SINGLE_AAS_REDIRECT: "<URL>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241220)
```

2. Start the AAS Web UI with the following command:

```bash
docker-compose up -d
```

### Volumes

The following volumes can be used to configure the AAS Web UI:

| Volume Name | Description |
|-------------|-------------|
| /usr/src/app/dist/Logo | The path to the folder containing the company logo in the top left corner and the favicon.ico. |

```{tip}
Using volumes works when building the Docker image yourself or when using the image from Docker Hub.
```

This is how you would use the volumes when building the Docker image yourself:

1. Build the Docker image from the Dockerfile like described above.

2. Start the Docker container with the following command (replace the volumes with your own values):

```bash
docker run -p 3000:3000 --name=aas-web-ui -v <local_path_to_logo>:/usr/src/app/dist/Logo aas-web-ui
```

This is how you would configure the volumes when using the AAS Web UI with Docker Compose and the image from Docker Hub:

1. Create a `docker-compose.yml` file in your project directory and add the following content (replace the volumes with your own values):

```yaml
services:
    aas-web-ui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-ui
        ports:
            - "3000:3000"
        volumes:
            - <local_path_to_logo>:/usr/src/app/dist/Logo
```

```{hint}
Specify the path to the logo in the `LOGO_PATH` environment variable.
```

2. Start the AAS Web UI with docker-compose like described above.
