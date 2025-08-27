# AAS Operations

In industrial environments, Asset Administration Shells need to represent not only static data and properties but also dynamic behaviors and functions. Operations in AAS provide a standardized way to expose callable functions that are relevant in the context of a specific asset or its Digital Twin. These operations enable interaction with assets, execution of commands, and implementation of business logic that goes beyond simple data access.

While the Asset Administration Shell itself is primarily a data structure, it can reference operations that trigger actual functionality. BaSyx addresses this challenge through operation delegation, where operations defined in AAS Submodels can be delegated to external services that provide the actual implementation. This approach enables distributed, service-oriented architectures while maintaining the standardized AAS interface.

Operation delegation is particularly valuable in scenarios where different services or systems are responsible for different aspects of an asset's functionality. Using qualifiers, the AAS can specify endpoints to external operation executors, creating a flexible and scalable architecture for Digital Twin implementations.

```{note}
A comprehensive example demonstrating AAS operation delegation is available in the <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxOperationDelegation" target="_blank">Examples on GitHub</a>. Feel free to try it out yourself!
```

## Operation Delegation Architecture

The following diagram illustrates how operation delegation works in the BaSyx ecosystem:

```{uml} charts/operation_architecture.puml
```

### Operation Execution Flow

The sequence diagram below shows the detailed process of how operations are delegated and executed:

```{uml} charts/operation_sequence.puml
```

## Operation Types and Use Cases

Here are some possible Operations and their use cases:

### Simple Operations

- **Simple Calculations**: Mathematical operations on AAS properties
- **Data Validation**: Verify data integrity and constraints
- **State Transitions**: Change asset states based on predefined rules
- **Configuration Updates**: Modify asset configuration parameters

### Complex Operations

- **Asset Control**: Send commands to physical assets or control systems
- **Complex Analytics**: Perform computationally intensive analysis
- **External System Integration**: Interact with ERP, MES, or other enterprise systems
- **Machine Learning Inference**: Execute AI models for predictive analytics

## Operation Delegation Mechanism

### Qualifier-based Endpoint Configuration

BaSyx uses qualifiers to specify how and where operations should be executed:

```json
{
  "modelType": "Operation",
  "idShort": "CalculateEfficiency",
  "qualifiers": [
    {
      "kind": "ConceptQualifier",
      "type": "invocationDelegation",
      "valueType": "xs:string",
      "value": "http://localhost:8087/operations/calculate-efficiency"
    }
  ],
  "inputVariables": [
    {
      "modelType": "OperationVariable",
      "value": {
        "modelType": "Property",
        "idShort": "ProductionRate",
        "valueType": "xs:double"
      }
    }
  ],
  "outputVariables": [
    {
      "modelType": "OperationVariable", 
      "value": {
        "modelType": "Property",
        "idShort": "EfficiencyScore",
        "valueType": "xs:double"
      }
    }
  ]
}
```

### Delegation Process

1. **Operation Invocation**: Client calls operation through standard AAS API
2. **Qualifier Resolution**: BaSyx extracts delegation endpoint from qualifiers
3. **Request Forwarding**: Operation request is forwarded to external service
4. **Execution**: External service performs the actual operation logic
5. **Response Handling**: Results are returned through the standard AAS interface

## Industrial Use Cases

### Manufacturing Process Control

Operations enable direct control of manufacturing processes:

- **Production Line Control**: Start, stop, and configure production lines
- **Quality Checks**: Trigger inspection procedures and validation routines
- **Maintenance Operations**: Schedule and execute maintenance procedures
- **Recipe Management**: Load and execute production recipes

### Asset Monitoring and Diagnostics

Operations can trigger monitoring and diagnostic functions:

- **Health Checks**: Assess asset condition and performance
- **Diagnostic Routines**: Run specialized diagnostic procedures
- **Calibration**: Execute sensor and actuator calibration sequences
- **Performance Analysis**: Calculate efficiency and performance metrics

### Integration with External Systems

Delegated operations enable seamless integration:

- **ERP Integration**: Trigger business processes in enterprise systems
- **Workflow Orchestration**: Initiate complex multi-step workflows
- **Data Synchronization**: Synchronize data with external databases
- **Notification Services**: Send alerts and notifications to external systems

## Service-Oriented Architecture Benefits

### Distributed Functionality

- **Separation of Concerns**: Different services handle different aspects of functionality
- **Independent Scaling**: Scale operation services independently based on demand
- **Technology Diversity**: Use different technologies for different operation types
- **Service Reusability**: Share operation implementations across multiple AAS instances

### Fault Tolerance and Resilience

- **Service Isolation**: Failures in one service don't affect others
- **Redundancy**: Deploy multiple instances of critical operation services
- **Circuit Breakers**: Protect against cascading failures
- **Graceful Degradation**: Continue operating with reduced functionality when services are unavailable

### Development and Deployment Flexibility

- **Independent Development**: Teams can develop operation services independently
- **Continuous Deployment**: Update operation logic without affecting AAS structure
- **Testing Isolation**: Test operation services in isolation
- **Version Management**: Manage different versions of operation implementations

## Getting Started with AAS Operations

### Basic Operation Implementation

Start with simple operations to understand the concept:

- Define operations in AAS Submodels
- Implement basic operation logic
- Test operation invocation through AAS API
- Understand input/output parameter handling

### Operation Delegation Setup

Explore delegation capabilities:

- Configure delegation qualifiers
- Implement external operation services
- Set up service discovery and routing
- Handle error scenarios and timeouts

```{include} /_external/basyx-java-server-sdk/examples/BaSyxOperationDelegation/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxOperationDelegation
:relative-images:
```

## Advanced Operation Patterns

### Asynchronous Operations

- **Long-running Processes**: Handle operations that take significant time to complete
- **Status Polling**: Provide status updates for ongoing operations
- **Callback Mechanisms**: Notify clients when operations complete
- **Queue Management**: Manage operation queues for high-load scenarios

### Composite Operations

- **Workflow Orchestration**: Combine multiple operations into complex workflows
- **Transaction Management**: Ensure consistency across multiple operation calls
- **Parallel Execution**: Execute multiple operations concurrently
- **Conditional Logic**: Implement branching and conditional operation execution

### Security and Access Control

- **Operation Authorization**: Control who can execute specific operations
- **Parameter Validation**: Validate operation inputs for security and consistency
- **Audit Logging**: Track operation executions for compliance and debugging
- **Rate Limiting**: Prevent abuse and ensure fair resource usage

## Additional Resources

For more information about AAS operations and delegation in BaSyx:

- [BaSyx Components Documentation](../../user_documentation/basyx_components/index.md)
- [Operation Delegation Configuration](../../user_documentation/basyx_components/v2/submodel_repository/features/operation-delegation.md)
