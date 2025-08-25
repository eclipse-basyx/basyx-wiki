# Test Orchestrator

Welcome to the documentation for the BaSyx Test Orchestrator.
This module provides automated validation for Asset Administration Shell (AAS) submodels.

- [Getting Started](./features/getting_started.md)
- [Example](./features/Example.md)
- [System Components](./features/concept/system_components.md)
- [Validation Logic](./features/concept/validation_logic.md)
- [Recursive Validation](./features/concept/recursive_validation.md)
- [Extending Validation](./features/feature/extending.md)
- [Results Visualization](./features/Visualization.md)
- [MongoDB Integration](./features/feature/mongodbintegration.md)
- Semantic Validation:
    - [ECLASS](./features/feature/SemanticValidation/ECLASS.md)
    - [Generative AI](./features/feature/SemanticValidation/GenerativeAI.md)
- [References](#references)

See also: [BaSyx Submodel Repository](../submodel_repository/index.md)

```{toctree}
:hidden:
:maxdepth: 1

features/getting_started
features/Example
features/concept/index
features/feature/index
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

```{figure} ./images/architecture.png
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
