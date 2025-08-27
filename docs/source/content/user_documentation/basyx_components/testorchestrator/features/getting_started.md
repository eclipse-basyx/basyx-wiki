# Getting Started

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

## Tool Comparison

| Feature                                      | [aas-test-engines](https://github.com/admin-shell-io/aas-test-engines) | [Twinfix](https://twinfix.twinsphere.io/) | [Basyx AAS Compliance Tool](https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/compliance_tool) | Test Orchestrator (This Repository) |
|---------------------------------------------|------------------|------------|-------------------------------|-------------------------------|
| **IDTA-compliant validation**               | ✅               | ✅         | ✅                            | ✅                            |
| **Validation against Submodel Templates**   | ⚠️ Only ContactInformation and Digital Nameplate | ❌ | ❌                            | ✅ (standardized and custom Submodels) |
| **Meta model conformity check**             | ❌               | ✅         | ✅                            | ❌                            |
| **API validation**                          | ✅               | ❌         | ❌                            | ❌                            |
| **Automatic triggering**                    | ❌               | ❌         | ❌                            | ✅ via MQTT                   |
| **Parallel/concurrent validation**          | ❌               | ✅         | ❌                            | ✅                            |
| **Result storage**                          | ❌ Console output only | ❌     | ❌ Console text output only  | ✅ Persisted in Submodel Repository |
| **Auto-fix suggestions**                    | ❌               | 🧪 Experimental | ❌                        | ✅ Suggestions for fixing errors and warnings |
| **Distribution of the tool**                | local            | online     | local                         | local and online             |
| **User interface**                          | CLI only         | Web Interface | CLI                         | Web UI, REST API            |
| **Supported formats**                       | AASX, JSON, XML  | AASX       | AASX, JSON, XML               | AASX, JSON, XML              |
| **Output format**                           | HTML view / console | Detailed web UI + downloadable JSON report | Console log (CLI steps and errors) | Categorized results + Visualization in Web UI + downloadable JSON report |
| **Result classification**                   | Flat errors      | Flat errors grouped by occurrence | Steps with SUCCESS/FAILED | Categorized – Errors, Warnings, Differences, Infos grouped by Submodel |

---

✅ = Fully Supported  ❌ = Not Supported  ⚠️ = Limited Support  🧪 = Experimental Feature

 
---

## Getting Started 

### Option 1: Run via Docker (Recommended for Fast Start)

You can use a Docker-based setup to quickly run the Test Orchestrator with BaSyx components:

```bash
git clone https://github.com/eclipse-basyx/basyx-applications.git
cd basyx-applications/test-orchestrator/example
docker-compose up -d
```

Then navigate to the local interface at:
```bash
http://localhost:9080
```

> Note: This setup launches the orchestrator, BaSyx backend components, and MQTT broker.

---
### Option 2: Manual Spring Boot Setup

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
