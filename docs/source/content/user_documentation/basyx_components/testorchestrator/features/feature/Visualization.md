## Visualization
All validation results are persisted in dedicated Submodels:

- **TestResults** – for successful validations
- **UnsuccessfulTestResults** – for failed or incomplete validations

---

## Result Structure

Each result contains:

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

The Test Orchestrator uses the [Basyx AAS Web UI Module](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/aas-web-ui/src/pages/modules) for displaying the validation results in user-friendly manner. Navigate to the `Test Orchestrator` module to:

- View all test results and statistics.
- See the suggestions for improving the submodel. 

The validation results can be downloaded:
- For individual submodels.
- For all tested submodels as a single JSON file.

```{figure} ./images/Test_Orchestrator_Module.png
---
width: 100%
alt: Test Orchestrator Module
name: Test_Orchestrator_Module
---
```

```{figure} ./images/WebUI_suggestion.png
---
width: 100%
alt: Visualization of Module
name: WebUI_suggestion
---
```
The results can also be filtered so that only specific submodels can be viewed. 

```{figure} ./images/filteredResults.PNG
---
width: 100%
alt: filteredResults
name: filteredResults
---
```