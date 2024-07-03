# Building Docker Images
Each component (i.e., projects ending with the _components_ suffix) contains a DockerFile describing the Docker Image. 
Please note that for building the docker images and running their tests, the docker compose file in the projects root directory has to be executed beforehand.

For building the Docker Images, Maven is utilized via:

  ```
mvn clean install -Ddocker.namespace=eclipsebasyx
  ```

By defining the _docker.namespace_ property, the maven docker plugin is enabled and the image is build as well as integration tests are being executed.