# Concept

The TestOrchestrator is designed to automatically validate AAS submodels against standardized templates defined by the IDTA or custom created submodels. It performs structural, semantic, and unit-based checks to ensure interoperability and compliance. The architecture follows a modular approach with components responsible for fetching, comparing, and reporting validation results. Users can provide AAS JSON data, API links of AAS/submodels and also upload AAS/submodels to receive detailed feedback on errors, warnings, and semantic mismatches.


## Contents

* [System Component](./system_components.md)
* [Recursive Validation](./recursive_validation.md)
* [Validation Logic](./validation_logic.md)

```{toctree}
:hidden:
:maxdepth: 1

system_components
recursive_validation
validation_logic
```
