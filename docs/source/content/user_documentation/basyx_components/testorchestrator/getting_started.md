[Back to Overview](index.md) | [Next: System Components](system_components.md)

# 🚀 Getting Started


# 🛠 Getting Started with the Test Orchestrator
## Overview

The **Test Orchestrator** is a Java/Spring Boot validation engine that automates the verification of AAS (Asset Administration Shell) Submodels against IDTA‑compliant templates. It ensures **structural integrity** and **semantic correctness** by matching uploaded Submodels to reference schemas (via `SemanticId`) and running a recursive, rule‑based check across all elements.

The orchestrator is designed for **production use**: it validates on every create/update event (MQTT), persists detailed results as standardized Submodels, and supports gradual extension with new templates and domain rules.

---

## Key Features

- **Automated Schema Matching**  
  Detects the correct template using the Submodel’s `SemanticId` and validates without manual intervention.

- **Recursive, Semantic‑Aware Validation**  
  Checks nested `SubmodelElementCollection`s, multiplicity (`One`, `ZeroToOne`, `OneToMany`, `ZeroToMany`), qualifiers (required/optional), idShort, types, and values.

- **Event‑Driven Operation**  
  Subscribes to Submodel lifecycle events (created/updated/deleted) via MQTT for continuous QA in live repositories.

- **Actionable Test Reports**  
  Persists categorized findings (**Errors**, **Warnings**, **Differences**, **Infos**) under dedicated Test Result Submodels.

- **Extensible by Design**  
  Add new IDTA templates or custom schemas; extend rules in comparator utilities to cover domain constraints.

---

## System Architecture 

At a high level, the orchestrator integrates with the BaSyx Submodel Repository, listens to MQTT events, deserializes incoming Submodels, performs template matching and recursive comparison, and stores the outcome as result Submodels.

```{figure} ./images/ValidationWorkflow.pdf
---
width: 100%
alt: ValidationWorkflow
name: ValidationWorkflow
---
```
**Core components (see paper / architecture page):**
- **Deserializer** – Parses AAS JSON into model objects and enforces version compatibility.  
- **Comparator** – Selects the right schema via `SemanticId` and orchestrates the check.  
- **RecursionFunc / SMEComparator** – Implements the depth‑first traversal and rule set (multiplicity, qualifiers, idShort/type/value checks).  
- **ResultSubmodelFactory** – Writes standardized results, including special cases (unsupported version, missing `SemanticId`).  

For deeper details, continue to [Validation Logic](validation_logic.md).

---

## Getting Started (Quick)

1. **Prerequisites**  
   - BaSyx Submodel Repository  
   - MQTT broker (e.g., Mosquitto)  
   - Java 17, Maven

2. **Run the Orchestrator**  
   Start the Spring Boot application with access to your Submodel Repository and MQTT broker.  
   The service registers its own Submodel and begins listening for events automatically.

3. **Validate a Submodel**  
   Upload or update a Submodel in the repository (via Web UI or API).  
   The orchestrator will detect the event, match the template, run validation, and write results.

4. **Inspect Results**  
   Query the repository for the **TestResults** Submodel related to your Submodel to review categorized findings.

---

## Configuration Notes

- **Schema Sources**  
  - Local: place JSON templates under `schema/` (classpath).  
  - Remote: extend predefined links to official IDTA SMT endpoints or internal registries.

- **Topics**  
  Default MQTT topics cover create/update/delete events. You can add domain‑specific topics for custom triggers.

- **Extending Rules**  
  Add domain checks by extending the comparator utilities (e.g., numeric ranges, unit consistency, cross‑element constraints).

---

## What’s Next?

- Understand the **recursive rule set** and result categories in [Validation Logic](validation_logic.md).  
- Learn how to **add new templates and rules** in [Extending Validation](features/extending.md).  
- See the full **architecture/methodology** in the scientific page (paper‑style) if included in your wiki.


---

[Back to Overview](index.md) | [Next: System Components](../system_components.md)