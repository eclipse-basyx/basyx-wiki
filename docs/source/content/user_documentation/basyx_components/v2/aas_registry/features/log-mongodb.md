# Log MongoDB

This project creates a docker image based on the specific spring-boot jar file.

To reduce dependencies and jar file size, we want to produce a docker file for each combination of registry-event-sink and storage combination.

We log registry events and use MongoDB storage in the docker image created here.

To test it on your local PC, invoke the build-image script and try the [docker compose file in the sibling project](https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/basyx.aasregistry/docker-compose/docker-compose.yml).