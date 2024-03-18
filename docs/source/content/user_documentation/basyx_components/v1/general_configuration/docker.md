# Docker 
The docker images for the components from the Java SDK are provided on [DockerHub](https://hub.docker.com/search?q=eclipsebasyx). For their documentation, see [here](./index.md). Thus, there is no need for building them before usage.

The following sections for deployment with docker assume an already installed docker environment.

# Java SDK
Additionally, you can either build the available docker images that are contained in the open source repository or create custom docker images by yourself. For both, you will need to [setup the Java SDK](../../download/java_setup.md) beforehand.

## Predefined Docker Images
All components with predefined docker images are contained in the basyx.components project. It is a hierarchical Maven project and consists of two sub-projects itself:

**basyx.components.docker** contains separate Maven sub-projects - one for each component that can be deployed as independent docker containers.

**basyx.components.lib** contains all other components and functions as a shared library - individual components are going to be organized into sub-projects over time.

See the [list of docker components](../basyx_components/index.md) in its own page.

### How to Create Predefined Docker Images?
Each Maven sub-project in **basyx.components.docker** can build a docker image when installing the project. By default, this step is skipped when [installing the Maven artifacts](../../download/components_setup.md) for each sub-project to the local repository. For including the docker image in the build process use the **Maven profile "docker"**:

* Right Click on the respective project (e.g. basyx.components.sqlregistry) -> Run As -> Maven build...
* Goals: *install*
* Profiles: *docker*
* Run
As with all Maven commands, you can also execute this outside of the Eclipse IDE. For this, navigate to the project folder (e.g. ...\basyx\components\basys.components\basyx.components.docker\basyx.components.simple) and execute the following command:
```
mvn install -Pdocker
```
Maven then runs unit tests, build the binaries and the docker image, runs the container and integration tests and then installs the project on success. Similar to the [default](../../download/components_setup.md) project installation without the docker images, it is also possible to skip all the tests and thereby the backend requirements listed in that page.

### How to create Images for ARM?
If you want to build the Image directly on an ARM device, you can just follow the instructions above. The following description shows how to crossbuild an ARM image on an x86 CPU.

As prerequisite you need a Docker installation with the Buildx plugin. Buildx comes prepackaged with Docker Desktop or can easily be installed if missing.

1. Run the **mvn install -Pdocker** command as described above
2. Run the following command in the root directory of the project you want to build. E.g. *.../components/basys.components/basyx.components.docker/basyx.components.AASServer.*
The **JAR_FILE** argument has to be changed to match the name of the .jar file in *.../target*.

Building the AAS-Server:
```
docker buildx build --load --platform linux/arm/v7 --build-arg JAR_FILE=basyx.components.AASServer-1.0.1.jar --build-arg PORT=4001 --tag aas-server:1.0.1-arm32v7 .
```

### How to start docker containers using the predefined docker images?
This depends on the container. Different containers can be configured in different ways and possibly depend on another piece of infrastructure. See the description of the docker component you are interested in for instructions on how to configure and start it. See the [list of docker components](../basyx_components/index.md) to find more information on that.

### How to Build Docker Images
As you already know, all projects inside of basyx.components.docker are Maven projects and therefore follow an automated build process. This process is the same for each individual docker component project and works as follows:

1. **Properties** for the image that has to be built are read from *src/test/resources/.env*
2. The **executable JAR-file is built**. The Maven property *basyx.components.executable* specifies the main class with the entry point for the created docker container. You can find it in the *pom.xml* of the project
3. **Unit tests** located at *src/test/java* are executed (includes files with the naming schema Test*.java, *Test.java, *Tests.java and *TestCase.java)
4. The **docker image** is created by the plugin *com.spotify.dockerfile-maven-plugin* with the provided *Dockerfile*
5. **Integration tests** are executed after composing a test environment using *docker-compose.yml*
6. If everything succeeded, the Maven artifacts are installed to the local repository!

The docker environment file **src/test/resources/.env** specifies variables for the docker-compose.yml and integration tests. Here you can see properties of the created docker image, like its name and the port mappings:
```
BASYX_CONTAINER_PORT=*This is the port inside of the container that is mapped*
BASYX_HOST_PORT=*This is the port at the host machine. Use it to access the container.*
BASYX_IMAGE_NAME=*The name of the created docker image*
BASYX_CONTAINER_NAME=*The name of the container that is started with docker-compose*
BASYX_IMAGE_TAG=*The tag of the created docker image*
```
When changing BASYX_HOST_PORT the created image will stay the same and expose the same port as before (=BASYX_CONTAINER_PORT) but the test environment during integration tests looks different, because this container port is mapped to another host port in the integration environment. You can run this test environment by yourself using the following docker command:

1. Navigate to the project folder /src/test/resources
2. Run the following command:
```
docker-compose up
```
Docker will read the environment file .env located in this resource folder and the *docker-compose.yml* in the parent folder to set up the integration test environment using the docker image that has been created before.

## Custom Docker Projects
To deploy an arbitrary resource (Asset Administration Shell, Sub Model, Registry, ...) with Docker, the resource has to be packaged with a server in a jar first. It is also possible to package several resources into a single jar and deploy them together.

In the following, it is assumed that the resource is already packaged in a jar file.


The following Dockerfile can be used to package arbitrary jars and expose their port(s). ${jar-name} is here the name of the jar file.

```yaml
# Add java runtime environment for execution
FROM java:8-jdk-alpine 
 
COPY ${jar-name}.jar /usr/share/${jar-name}.jar
 
# Expose the appropriate port. In case of Tomcat, this is 8080. 
EXPOSE 8080 
 
# Start the jar
CMD java -jar "/usr/share/${jar-name}.jar"
```

After building the jar, the image named ${image-name} can be build using
```
docker build -t ${image-name} . 
```
You can choose any arbitrary image name. Next, the container can be started. To do this, use the following command:
```
docker run -p${host-port}:8080 ${image-name}
```
*${host-port}* can be an arbitrary chosen port that is currently not in use on the host system. If another port than 8080 was exposed by the Dockerfile, the port has to change appropriately in the *docker run* command.