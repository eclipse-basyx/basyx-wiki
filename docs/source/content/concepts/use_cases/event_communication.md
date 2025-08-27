# Event Communication

In modern industrial environments and Digital Twin architectures, real-time awareness of changes and state updates is crucial for maintaining system coherence and enabling reactive behaviors. Event-driven communication allows systems to respond immediately to changes in Asset Administration Shells, Submodels, and their properties, enabling scenarios such as automated workflows, monitoring dashboards, data synchronization, and compliance tracking.

BaSyx implements comprehensive event communication capabilities that automatically generate and publish events whenever changes occur to AAS, Submodels, properties, or registry descriptors. This event-driven architecture enables loose coupling between components while ensuring that all interested parties are notified of relevant changes in real-time.

The BaSyx ecosystem supports multiple event communication protocols. **Repositories** (AAS Repository, Submodel Repository, ConceptDescription Repository) support both **MQTT** for lightweight IoT scenarios and **Apache Kafka** for high-throughput enterprise environments. **Registries** (AAS Registry, Submodel Registry) currently support **Kafka** event streaming. Third-party applications can subscribe to these event streams to implement custom business logic, analytics, or integration workflows based on AAS lifecycle events.

```{note}
Two comprehensive examples demonstrating different event communication scenarios are available in the <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/" target="_blank">Examples on GitHub</a>:
- <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxMinimal" target="_blank">BaSyx Minimal Setup with MQTT Events</a>
- <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxKafka" target="_blank">BaSyx Kafka Events Example</a>

Feel free to try them out yourself!
```

## Event Communication Architecture

The following diagram illustrates how event-driven communication works across the BaSyx ecosystem:

```{uml} charts/event_architecture.puml
```

### Event Publishing and Consumption Flow

The sequence diagram below shows the detailed process of how events are generated, published, and consumed:

```{uml} charts/event_sequence.puml
```

## Event Types and Triggers

BaSyx generates events for various operations across different components:

### AAS Repository Events (MQTT & Kafka)

- **AAS Created**: Triggered when a new Asset Administration Shell is created
- **AAS Updated**: Fired when AAS metadata or structure is modified
- **AAS Deleted**: Generated when an AAS is removed from the repository
- **Submodel Reference Created**: Triggered when Submodel references are added to an AAS
- **Submodel Reference Deleted**: Generated when Submodel references are removed from an AAS

### Submodel Repository Events (MQTT & Kafka)

- **Submodel Created**: Generated when new Submodels are created
- **Submodel Updated**: Triggered when Submodel structure or metadata changes
- **Submodel Deleted**: Fired when Submodels are removed
- **SubmodelElement Created**: Generated when new SubmodelElements are added
- **SubmodelElement Updated**: Triggered for individual property value updates
- **SubmodelElement Deleted**: Fired when SubmodelElements are removed
- **SubmodelElements Patched**: Generated when multiple elements are updated in batch
- **File Value Updated**: Triggered when file attachments are modified
- **File Value Deleted**: Generated when file attachments are removed

### ConceptDescription Repository Events (MQTT & Kafka)

- **ConceptDescription Created**: Triggered when new ConceptDescriptions are created
- **ConceptDescription Updated**: Fired when ConceptDescription metadata changes
- **ConceptDescription Deleted**: Generated when ConceptDescriptions are removed

### Registry Events (Kafka Only)

- **Descriptor Registration**: Fired when AAS or Submodel descriptors are registered
- **Descriptor Update**: Triggered when registry information is modified
- **Descriptor Deletion**: Generated when descriptors are removed from registries

## Supported Event Protocols

### MQTT Event Communication

MQTT provides lightweight, efficient event communication ideal for IoT scenarios:

- **Low Overhead**: Minimal bandwidth requirements for resource-constrained environments
- **Quality of Service**: Configurable delivery guarantees (QoS 0, 1, 2)
- **Topic-based Routing**: Hierarchical topic structure for selective event subscription
- **Retained Messages**: Last known state available for new subscribers
- **Bi-directional Communication**: Support for both event publishing and command messaging

### Apache Kafka Event Streaming

Kafka offers enterprise-grade event streaming capabilities:

- **High Throughput**: Handle millions of events per second
- **Durability**: Persistent event storage with configurable retention
- **Partitioning**: Parallel processing and horizontal scaling
- **Exactly-Once Semantics**: Guaranteed message delivery without duplicates
- **Schema Evolution**: Support for evolving event structures over time

## Event Payload Structure

BaSyx events follow the same structure as the element that was changed.

### Property Change Event

```json
{
    "modelType" : "Property",
    "valueType" : "xs:string",
    "category" : "VARIABLE",
    "description" : [ {
        "language" : "en-us",
        "text" : "Legally valid designation of the natural or judicial person which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into circulation."
    }, {
        "language" : "de",
        "text" : "Bezeichnung für eine natürliche oder juristische Person, die für die Auslegung, Herstellung und Verpackung sowie die Etikettierung eines Produkts im Hinblick auf das 'Inverkehrbringen' im eigenen Namen verantwortlich ist"
    } ],
    "idShort" : "InstanceId"
}
```

## Industrial Use Cases

### Real-time Monitoring and Alerting

Event-driven monitoring enables immediate response to critical changes:

- **Threshold Monitoring**: Trigger alerts when sensor values exceed predefined limits
- **Equipment Status Tracking**: Monitor machine state changes and availability
- **Quality Control**: Detect and respond to quality parameter deviations
- **Predictive Maintenance**: Correlate events to predict maintenance needs

### Workflow Automation

Events can trigger automated business processes:

- **Supply Chain Orchestration**: Initiate procurement when inventory levels change
- **Quality Assurance**: Automatically trigger inspection workflows for new products
- **Compliance Reporting**: Generate reports when regulatory-relevant data changes
- **Data Synchronization**: Keep external systems synchronized with AAS state

### Analytics and Business Intelligence

Event streams provide valuable data for analysis:

- **Performance Metrics**: Calculate KPIs based on operational events
- **Trend Analysis**: Identify patterns in equipment behavior over time
- **Cost Optimization**: Track resource usage and operational efficiency
- **Customer Insights**: Analyze product usage patterns from connected devices

## Getting Started with BaSyx Events

### 1. Minimal Setup with MQTT

Start with the lightweight MQTT-based event communication:

- Simple Docker Compose setup with MQTT broker
- Pre-configured AAS Repository with MQTT event publishing
- Example event consumers and monitoring tools
- Basic event filtering and routing examples

### 2. Enterprise Kafka Setup

Explore high-throughput event streaming:

- Kafka cluster with AKHQ management interface
- Multiple BaSyx components with Kafka integration
- Advanced event processing and analytics examples
- Event schema management and evolution

```{include} /_external/basyx-java-server-sdk/examples/BaSyxMinimal/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxMinimal
:relative-images:
```

## Advanced Event Processing

### Event Filtering and Routing

- **Content-based Filtering**: Route events based on payload content
- **Pattern Matching**: Use regular expressions for complex event selection
- **Aggregation Windows**: Combine multiple events into summary notifications
- **Rate Limiting**: Control event frequency to prevent system overload

### Event Transformation

- **Format Conversion**: Transform events between different schemas
- **Enrichment**: Add contextual information from external sources
- **Correlation**: Link related events across different AAS components
- **Anonymization**: Remove sensitive data while preserving analytical value

### Error Handling and Reliability

- **Dead Letter Queues**: Handle events that cannot be processed
- **Retry Mechanisms**: Automatic retry with exponential backoff
- **Circuit Breakers**: Prevent cascade failures in event processing
- **Monitoring and Alerting**: Track event processing health and performance

```{include} /_external/basyx-java-server-sdk/examples/BaSyxKafka/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxKafka
:relative-images:
```

## Additional Resources

- [BaSyx Components Documentation](../../user_documentation/basyx_components/index.md)
- [AAS Repository MQTT Events](../../user_documentation/basyx_components/v2/aas_repository/features/mqtt.md)
- [Submodel Repository MQTT Events](../../user_documentation/basyx_components/v2/submodel_repository/features/mqtt.md)
- [AAS Registry Kafka Events](../../user_documentation/basyx_components/v2/aas_registry/features/kafka-events.md)
- [Submodel Registry Kafka Events](../../user_documentation/basyx_components/v2/submodel_registry/features/kafka-events.md)
