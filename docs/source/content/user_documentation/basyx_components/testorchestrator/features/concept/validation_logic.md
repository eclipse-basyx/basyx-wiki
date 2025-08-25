[Back to Getting Started](getting_started.md) | [Next: Extending Validation](extending.md)

---

# Validation Logic

The Test Orchestrator validates submodels in three main steps:

---

## 1. Event-driven Submodel Processing

The `MqttSubscriber` listens for submodel creation, update, and deletion events:

```java
client.subscribe(TOPIC_NEW);
client.subscribe(TOPIC_UPDATE);
client.subscribe(TOPIC_DELETE);
```

**On creation/update:**
- Deserializes the submodel, checks the AASX version, and validates the presence of a SemanticId.

**On deletion:**
- Cleans up related test results in the repository.

---

## 2. Validation Logic

**Deserialization:**  
All submodels and schemas are parsed using the IDTA-compatible JSON format:

```java
Environment inputEnv = Deserializer.deserializejsonFile(jsonString);
```

**Comparison:**  
Each input submodel is compared to all available schema submodels (from IDTA or custom sources) by matching their SemanticId:

```java
ComparisonResult result = Comparator.compare(schemaSubmodel, inputSubmodel);
```

**Recursive Validation:**  
The main routine for comparing submodel elements:

```java
RecursionFunc.compareSubmodelElements(
    schemaSubmodel.getSubmodelElements(),
    inputSubmodel.getSubmodelElements(),
    result
);
```

This function:
- Validates multiplicity rules
- Checks required/optional elements (using qualifiers)
- Compares properties, types, values, and semantic IDs
- Recurses into nested SubmodelElementCollections

**Multiplicity Checks Example:**

```java
if ("One".equals(multiplicity)) {
    SMEComparator.checkMultiplicityOne(schemaElement, inputElementMap, result);
}
```

All multiplicity rules (`One`, `ZeroToOne`, `OneToMany`, `ZeroToMany`) are supported according to IDTA specifications.

---

## 3. Test Results & Reporting

All validation outcomes are written as `SubmodelElementCollections` in a dedicated `TestResults` submodel in the repository.

```java
ResultSubmodelFactory.addResultToSubmodel(comparisonResult, inputSubmodel);
```

**Example structure of a result:**

```json
{
  "ComparedSubmodelId": "...",
  "SemanticId": "...",
  "Errors": "...",
  "Warnings": "...",
  "Differences": "...",
  "Infos": "..."
}
```

---

## Handling Unsupported Versions and Missing Semantic IDs

**Unsupported AASX version:**  
Detected early, and a result is recorded using:

```java
ResultSubmodelFactory.addUnsupportedVersionResult(rawJson);
```

**Missing SemanticId:**  
Triggers a warning and skips validation.

---

## Example: Submodel Comparison Core Logic

```java
public static ComparisonResult compare(Submodel schemaSubmodel, Submodel inputSubmodel) {
    ComparisonResult result = new ComparisonResult();
    RecursionFunc.compareSubmodelElements(
        schemaSubmodel.getSubmodelElements(),
        inputSubmodel.getSubmodelElements(),
        result
    );
    return result;
}
```

---

## Example: Handling a New Submodel Event

```java
private void processSubmodel(String submodelJson) {
    if (!isAASXv3Format(submodelJson)) {
        ResultSubmodelFactory.addUnsupportedVersionResult(submodelJson);
        return;
    }
    Submodel submodel = deserializer.read(submodelJson, Submodel.class);
    if (submodel.getSemanticId() == null) {
        ResultSubmodelFactory.addUnsuccessfulResultToSubmodel(submodel);
        return;
    }
    SubmodelFactory.processReceivedSubmodel(submodel);
}
```
---

## 📊 Validation Sequence

The validation process is also represented in the following sequence diagram, which highlights the interaction between the Submodel Repository, Deserializer, Comparator, Recursion Function, SMEComparator, and the MQTT/Web UI integration.

```{figure} ./images/ValidationSequence.png
---
width: 100%
alt: ValidationSequence
name: ValidationSequence
---
```

This sequence shows:
- **Upload/Edit** of a Submodel via MQTT/Web UI  
- **Deserialization** of input and schema JSON files  
- **Recursive comparison** of elements, including SemanticId mapping  
- **Multiplicity checks** (Zero/One/Many)  
- **Result generation** stored in the Submodel Repository and displayed to the user


[Next: Extending Validation](extending.md)
