[Back: Recursive Validation](recursive_validation.md) | [Next: Extending Validation](features/extending.md)

# 📊 Results Visualization


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

## Viewing Results

- Through the **BaSyx Submodel Repository API**
- Via the **BaSyx Web UI**, where categorized results are displayed
- As downloadable JSON files for further processing

---
```{figure} ./images/filteredResults.PNG
---
width: 100%
alt: filteredResults
name: filteredResults
---
```

*Figure: Example filtered view of validation results in the BaSyx UI*
---

[Back: Recursive Validation](recursive_validation.md) | [Next: Extending Validation](features/extending.md)