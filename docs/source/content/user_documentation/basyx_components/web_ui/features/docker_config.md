# Docker Configuration

## User Story and Use Case

>As AAS Web UI user
>I want to preconfigure the AAS Web UI through Docker environment variables.
>I also want to be able to mount my own folders containing UI plugins and my company logo.

The Docker Image of the AAS Web UI can be configured through environment variables and volumes. This allows the user to preconfigure the AAS Web UI when starting the Docker container.

## Feature Overview

### Environment Variables

The following environment variables can be used to configure the AAS Web UI:

| Variable Name | Description |
|---------------|-------------|
| VITE_REGISTRY_PATH | The path to the BaSyx Registry. |
| VITE_AAS_REPO_PATH | The path to the AAS Repository. |
| VITE_SUBMODEL_REPO_PATH | The path to the Submodel Repository. |
| VITE_CD_REPO_PATH | The path to the Concept Description Repository. |
| VITE_PRIMARY_COLOR | The primary color of the AAS Web UI. |
| VITE_BASE_PATH | The base path of the AAS Web UI. |
| CHOKIDAR_USEPOLLING | Enables polling for file changes (needed when using a plugins folder). |

```{tip}
Using environment variables works when building the Docker image yourself or when using the image from Docker Hub.
```

This is how you would use the environment variables when building the Docker image yourself:

1. Build the Docker image from the Dockerfile in the [aas-web-gui](https://github.com/eclipse-basyx/basyx-applications/tree/main/aas-gui/Frontend/aas-web-gui) directory of the AAS Web UI repository:

```bash
docker build -t aas-web-ui .
```

2. Start the Docker container with the following command (replace the environment variables with your own values):

```bash
docker run -p 3000:3000 --name=aas-web-ui -e CHOKIDAR_USEPOLLING=true -e VITE_REGISTRY_PATH="<registry_path>" -e VITE_AAS_REPO_PATH="<aas_repo_path>" -e VITE_SUBMODEL_REPO_PATH="<submodel_repo_path>" -e VITE_CD_REPO_PATH="<concept_description_repo_path>" -e VITE_PRIMARY_COLOR="<primary_color>" -e VITE_BASE_PATH="<base_path>" aas-web-ui
```

This is how you would configure the environment variables when using the AAS Web UI with Docker Compose and the image from Docker Hub:

1. Create a `docker-compose.yml` file in your project directory and add the following content (replace the environment variables with your own values):

```yaml
version: "3.8"
services:
    aas-web-gui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-gui
        ports:
            - "3000:3000"
        environment:
            CHOKIDAR_USEPOLLING: "true"
            VITE_REGISTRY_PATH: "<registry_path>"
            VITE_AAS_REPO_PATH: "<aas_repo_path>"
            VITE_SUBMODEL_REPO_PATH: "<submodel_repo_path>"
            VITE_CD_REPO_PATH: "<concept_description_repo_path>"
            VITE_PRIMARY_COLOR: "<primary_color>"
            VITE_BASE_PATH: "<base_path>"
```

2. Start the AAS Web UI with the following command:

```bash
docker-compose up -d
```

### Volumes

The following volumes can be used to configure the AAS Web UI:

| Volume Name | Description |
|-------------|-------------|
| /app/src/assets/Logo | The path to the folder containing the company logo in the top left corner and the favicon.ico. |
| /app/src/UserPlugins | The path to the folder containing the UI plugins. |

```{tip}
Using volumes works when building the Docker image yourself or when using the image from Docker Hub.
```

This is how you would use the volumes when building the Docker image yourself:

1. Build the Docker image from the Dockerfile like described above.

2. Start the Docker container with the following command (replace the volumes with your own values):

```bash
docker run -p 3000:3000 --name=aas-web-ui -v <local_path_to_logo>:/app/src/assets/Logo -v <local_path_to_plugins>:/app/src/UserPlugins aas-web-ui
```

This is how you would configure the volumes when using the AAS Web UI with Docker Compose and the image from Docker Hub:

1. Create a `docker-compose.yml` file in your project directory and add the following content (replace the volumes with your own values):

```yaml
version: "3.8"
services:
    aas-web-gui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-gui
        ports:
            - "3000:3000"
        volumes:
            - <local_path_to_logo>:/app/src/assets/Logo
            - <local_path_to_plugins>:/app/src/UserPlugins
```

2. Start the AAS Web UI with docker-compose like described above.

### Example using Docker Compose for a complete BaSyx environment

You can create a complete BaSyx example environment with Docker Compose. This includes the AAS Web UI, the BaSyx Registry and the AAS Environment (AAS Repository, Submodel Repository, Concept Description Repository).

This is a simple example of how to setup the AAS Web UI with Docker Compose in a `docker-compose.yml` file:

```yaml	
version: "3.8"
services:
    aas-env:
        image: eclipsebasyx/aas-environment:2.0.0-SNAPSHOT
        container_name: aas-env
        volumes:
        - ./aas-env.properties:/application/application.properties
        - ./aas:/application/aas
        ports:
            - 8081:8081
        restart: always
            
    aas-registry:
        image: eclipsebasyx/aas-registry-log-mem:2.0.0-SNAPSHOT
        container_name: aas-registry
        ports:
        - 8082:8080
        volumes:
        - ./aas-registry.yml:/workspace/config/application.yml
        restart: always

    aas-web-ui:
        image: eclipsebasyx/aas-gui:v2-231107
        container_name: aas-web-ui
        ports:
        - "3000:3000"
        environment:
            VITE_REGISTRY_PATH: "http://localhost:8082/api/v3.0"
            VITE_AAS_REPO_PATH: "http://localhost:8081/shells"
            VITE_SUBMODEL_REPO_PATH: "http://localhost:8081/submodels"
            VITE_CD_REPO_PATH: "http://localhost:8081/concept-descriptions"
        restart: always
```

```{hint}
You can find a complete example on how to setup BaSyx with Docker in the [Quick Start](../../../../introduction/quickstart) section.
```
