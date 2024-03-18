# Components Setup {How to install BaSyx Components}

<span style="color:red" >!! Building BaSyx Java is only necessary if you would like to access the currently being developed features. All releases are available on [Maven Central](https://central.sonatype.com/search?q=org.eclipse.basyx&smo=true) or [DockerHub](https://hub.docker.com/search?q=eclipsebasyx) and thus don't need to be build locally !!</span>


The complete installation process of the SDK and components is documented in a 15 minutes video:[YouTube](https://www.youtube.com/results?search_query=basyx) The code of the components can be found on [GitHub](https://github.com/eclipse-basyx/basyx-java-components).


The components package depends on [basyx.sdk](java_setup.md) and is a hierarchical maven project that consists of multiple infrastructure components. Each of them is separated in its own maven project. Therefore each component can be built independently and can have its own dependencies.

In order to install all components to the local maven repository, **mvn install** can be used like with installing the [basyx.sdk](java_setup.md). As maven executes all tests before installing the build artifacts into the local repository, you need to make sure all the component's requirements are met beforehand. See the next subsections for the SQL and MongoDB backends. Alternatively, it is possible to directly build the artifacts without these requirements by skipping the maven test phase with **mvn install -DskipTests**.

Additionally, all of the off-the-shelf components can be used in a Docker environment. All maven projects can also build their correspondent [docker images](../user_documentation/basyx_components/docker.md#how-to-build-docker-images).

## SQL components
All SQL components additionally require an SQL backend. This backend can for example be provided by [postgreSQL](https://www.postgresql.org).

During installation of the SQL backend, choose the following credentials:

**user**: postgres

**password**: admin

Note: In order to change these default connection settings for the postgreSQL database, the connection data has to be updated in the properties files for the SQL tests in the components project.

To setup the database for the test cases, open up a console and use the following commands:
```
Create configuration directory:

initdb -D "<db-path>" -U <username>

Where <db-path> is a path to a directory you have the right to write to, and <username> would be "postgres". Now you start the database with

pg_ctl -D "<db-path>" start
```

Save the following commands to an arbitrary text file (named <your-file> in the following). Next, import the database through psql -U postgres -f "<your-file>".
```
CREATE DATABASE "basyx-map";

CREATE DATABASE "basyx-directory";
```

Finally, you can install the basyx.components project using maven. See the instructions for the [Java SDK](java_setup.md) on how to do that.


## MongoDB components
Similarly, the components based on MongoDB need the MongoDB when executed locally. This can for example be provided by the Community version of the MongoDB [MongoDB](https://www.mongodb.com/try/download/community).