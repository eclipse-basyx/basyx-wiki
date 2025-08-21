# Test Orchestrator

Welcome to the documentation for the BaSyx Test Orchestrator.
This module provides automated validation for Asset Administration Shell (AAS) submodels.

- [Getting Started](getting_started.md)
- [System Components](system_components.md)
- [Validation Logic](validation_logic.md)
- [Recursive Validation](recursive_validation.md)
- [Extending Validation](extending.md)
- [Results Visualization](results_visualization.md)
- [Example](./features/Example.md)
- [Visualization](./features/Visualization.md)
- [MongoDB Integration](./features/mongodbintegration.md)
- Semantic Validation:
    - [ECLASS](./features/SemanticValidation/ECLASS.md)
    - [Generative AI](./features/SemanticValidation/GenerativeAI.md)
- [References](#references)

See also: [BaSyx Submodel Repository](../submodel_repository/index.md)

```{toctree}
:hidden:
:maxdepth: 1

getting_started
system_components
validation_logic
recursive_validation
extending
results_visualization
features/Example
features/Visualization
features/mongodbintegration
features/SemanticValidation/ECLASS
features/SemanticValidation/GenerativeAI
```
## Overview

The Test Orchestrator is a Spring Boot-based extension for validating Asset Administration Shell (AAS) submodels according to IDTA/Industry standards.

It provides:
- Automated structural and semantic validation
- Integration with MQTT for real-time submodel event monitoring
- Result reporting via standardized submodels
- Support for extensible schemas and rule sets

---

## Architecture

The Test Orchestrator integrates with the BaSyx Submodel Repository and listens for submodel creation, update, and deletion events via MQTT.

```{figure} ./images/architecture.pdf
---
width: 100%
alt: architecture
name: architecture
---
```

---

## References

- [IDTA Submodel Templates](https://github.com/admin-shell-io/submodel-templates)
- [Eclipse BaSyx Documentation](https://wiki.basyx.org/en/latest/)
- [AASX Package Explorer](https://github.com/admin-shell-io/aasx-package-explorer)

[Next: Getting Started](getting_started.md)
