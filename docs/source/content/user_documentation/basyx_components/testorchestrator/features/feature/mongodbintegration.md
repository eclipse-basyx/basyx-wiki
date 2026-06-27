# MongoDB Integration

Test Orchestrator can use both InMemory and MongoDB.

For using MongoDB, There are configurations that needs to be added inside the files in the folder `basyx`. The backend needs to be set to MongoDB instead of InMemory:

```
basyx.backend=MongoDB
```

In `testorchestrator.properties` and `aas-env.properties`, add the following:

```
basyx.backend=MongoDB
spring.mongodb.host=mongo
spring.mongodb.port=27017
spring.mongodb.database=testorchestrator
spring.mongodb.authentication-database=admin
spring.mongodb.username=mongoAdmin
spring.mongodb.password=mongoPassword
```

In `aas-registry.yml` and `sm-registry.yml`, add the following lines:

```
spring:
  mongodb:
    uri: mongodb://mongoAdmin:mongoPassword@mongo:27017
```

In `docker-compose.yml`, add the following lines inside services:

```
  mongo:
    image: mongo:5.0.10
    container_name: mongo
    ports:
      - '27017:27017'
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongoAdmin
      MONGO_INITDB_ROOT_PASSWORD: mongoPassword
    restart: always
    healthcheck:
      test: mongo
      interval: 10s
      timeout: 5s
      retries: 5
```

Now, when all the containers are up, you can access MongoDB in port 27017. MongoDBCompass can be used to see the database and all the documents inside. 

> **Warning:** Restarting the container `TestOrchestrator` might result in an error because the `TestOrchestrator` submodel is not checked for prior existence in the Submodel Repository. It is recommended to restart all containers at once, which ensures that all previously registered submodels are removed.
