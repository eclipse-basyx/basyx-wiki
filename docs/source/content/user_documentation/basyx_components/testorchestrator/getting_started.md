[Back to Overview](index.md) | [Next: Validation Logic](validation_logic.md)

## Prerequisites

- BaSyx Submodel Repository
- MQTT broker (e.g., Mosquitto)
- Java 17+
- Spring Boot

---

## Main Entry Point

```java
@SpringBootApplication(
    scanBasePackages = {"org.eclipse.digitaltwin.basyx", "org.eclipse.digitaltwin.basyx.TestOrchestrator"},
    exclude = { MongoAutoConfiguration.class, MongoDataAutoConfiguration.class })
public class TestOrchestrator {
    public static void main(String[] args) {
        ApplicationContext context= SpringApplication.run(TestOrchestrator.class, args);
        SubmodelRepository repo = context.getBean(SubmodelRepository.class);
        repo.createSubmodel(SubmodelFactory.creationSubmodel());
        // Ensures MQTT Subscriber is initialized
        context.getBean(MqttSubscriber.class);
    }
}


