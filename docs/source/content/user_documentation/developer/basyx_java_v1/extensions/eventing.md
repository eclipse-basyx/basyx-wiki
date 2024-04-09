# Java SDK Eventing for AAS

## MqttAASAggregator (Implements IAASAggregator)
**Package**: org.eclipse.basyx.extensions.aas.aggregator.mqtt

**Events list**:

| Method Name                             | Topic Name                 | Payload |
|-----------------------------------------|----------------------------|---------|
| createAAS(AssetAdministrationShell aas) | BaSyxAggregator_createdAAS | $AASId  |
| updateAAS(AssetAdministrationShell aas) | BaSyxAggregator_updatedAAS | $AASId  |
| deleteAAS(IIdentifier aasId)            | BaSyxAggregator_deletedAAS | $AASId  |

## MqttAASRegistryService (Implements IAASRegistryService)
**Package**: org.eclipse.basyx.extensions.aas.registration.mqtt

**Events list**:

| Method Name                                                | Topic Name                       | Payload        |
|------------------------------------------------------------|----------------------------------|----------------|
| register(AASDescriptor deviceAASDescriptor)                | BaSyxRegistry_registeredAAS      | $AASId         |
| register(IIdentifier aas, SubmodelDescriptor smDescriptor) | BaSyxRegistry_registeredSubmodel | ($AASId,$SMId) |
| delete(IIdentifier aasId)                                  | BaSyxRegistry_deletedAAS         | $AASId         |
| delete(IIdentifier aasId, IIdentifier smId)                | BaSyxRegistry_deletedSubmodel    | ($AASId,$SMId) |

## MqttSubmodelAPI (Implements ISubmodelAPI)
**Package**: org.eclipse.basyx.extensions.events.submodel.mqtt

**Events list**:

| Method Name                                                                                               | Topic Name                           | Payload                               |
|-----------------------------------------------------------------------------------------------------------|--------------------------------------|---------------------------------------|
| MqttSubmodelAPI(ISubmodelAPI observedAPI, String serverEndpoint, String clientId)                         | BaSyxSubmodel_createdSubmodel        | $SMId                                 |
| MqttSubmodelAPI(ISubmodelAPI observedAPI, String serverEndpoint, String clientId, String user, char[] pw) | BaSyxSubmodel_createdSubmodel        | $SMId                                 |
| MqttSubmodelAPI(ISubmodelAPI observedAPI, MqttClient client)                                              | BaSyxSubmodel_createdSubmodel        | $SMId                                 |
| addSubmodelElement(ISubmodelElement elem)                                                                 | BaSyxSubmodel_addedSubmodelElement   | ($AASId, $SMId , $ElementId)          |
| addSubmodelElement(String idShortPath, ISubmodelElement elem)                                             | BaSyxSubmodel_addedSubmodelElement   | ($AASId, $SMId , $ElementIdShortPath) |
| deleteSubmodelElement(String idShortPath)                                                                 | BaSyxSubmodel_removedSubmodelElement | ($AASId, $SMId , $ElementIdShortPath) |
| updateSubmodelElement(String idShortPath, Object newValue)                                                | BaSyxSubmodel_updatedSubmodelElement | ($AASId, $SMId , $ElementIdShortPath) |

In **MqttSubmodelAPI**, the event propagation only works if the class variable **useWhiteList** is true or only for whitelisted Submodel IdShort. The class has a class variable- **Set<String> whitelist** which maintains the whitelisted submodel IdShort.


**In Every Class**:

*$AASId = Id of the Identifier of AAS*

*$SMId = Id of the Identifier of Submodel*