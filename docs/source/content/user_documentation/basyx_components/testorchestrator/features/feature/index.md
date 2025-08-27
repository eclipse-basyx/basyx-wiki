# Features

Test Orchestrator offers a range of features for validating and analyzing AAS submodels.
Users can upload or link submodels for automated validation against standard or custom submodels. The tool supports semantic validation through both Generative AI (unit verification) and ECLASS-based checks (preferred names and definitions). A MongoDB integration ensures persistent storage of test results, while the user interface provides filtering, visualization, and inspection options to easily explore validation outcomes. Additionally, users can download validation results as JSON files directly from the UI for further processing or archival.

## Feature Types

* [Visualization](./Visualization.md)
* [Extending](./extending.md)
* [MongoDB Integration](./mongodbintegration.md)
* Semantic Validation
    * [ECLASS](./SemanticValidation/ECLASS.md)
    * [Generative AI](./SemanticValidation/GenerativeAI.md)

```{toctree}
:hidden:
:maxdepth: 1

Visualization
extending
mongodbintegration
SemanticValidation/ECLASS
SemanticValidation/GenerativeAI
```
