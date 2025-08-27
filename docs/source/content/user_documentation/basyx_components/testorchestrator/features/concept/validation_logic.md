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
- Deserializes the submodel
- Checks the AASX version
- Validates presence of `SemanticId`

**On deletion:**
- Cleans up related test results in the repository.

---

## 2. Validation Logic

###  Validation Sequence

The validation process is illustrated in the sequence diagram below, showing the interactions between the Submodel Repository, Deserializer, Comparator, Recursion Function, SMEComparator, and MQTT/Web UI interface.

```{figure} ./images/ValidationSequence.png
---
width: 100%
alt: ValidationSequence
name: ValidationSequence
---
```
---
**Deserialization:**  
Parses all input submodels and templates using IDTA-compatible JSON:

```java
Environment inputEnv = Deserializer.deserializejsonFile(jsonString);
```

**Comparison Logic:**  
Each input submodel is compared to schema submodels by matching `SemanticId`:

```java
ComparisonResult result = Comparator.compare(schemaSubmodel, inputSubmodel);
```

**Recursive Validation:**  
Main logic for comparing submodel elements recursively:

```java
RecursionFunc.compareSubmodelElements(
    schemaSubmodel.getSubmodelElements(),
    inputSubmodel.getSubmodelElements(),
    result
);
```

This function:
- Checks multiplicity (One, ZeroToOne, etc.)
- Verifies qualifiers (required/optional)
- Compares type, value, and semanticId
- Recurses into nested `SubmodelElementCollection`s
---

**Multiplicity Checks Example:**

```java
if ("One".equals(multiplicity)) {
    SMEComparator.checkMultiplicityOne(schemaElement, inputElementMap, result);
}
```

All four multiplicity types are supported:
- `One`
- `ZeroToOne`
- `OneToMany`
- `ZeroToMany`

---

## 3. Test Results & Reporting

All validation results are written as Submodels in the repository:

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

##  Handling Edge Cases:

### Unsupported AASX Versions

```java
ResultSubmodelFactory.addUnsupportedVersionResult(rawJson);
```

### Missing SemanticId

```java
if (submodel.getSemanticId() == null) {
    ResultSubmodelFactory.addUnsuccessfulResultToSubmodel(submodel);
    return;
}
```
##  Full Comparison Function Example

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

##  Handling New Submodel Event

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



[Next: Extending Validation](extending.md)
