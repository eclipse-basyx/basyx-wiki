---
[Back: Validation Logic](validation_logic.md) | [Next: Results Visualization](results_visualization.md)
---

# 🔁 Recursive Validation

Recursive validation ensures structural and semantic correctness of nested SubmodelElementCollections.

- Validates multiplicity constraints (`One`, `ZeroToOne`, `OneToMany`, `ZeroToMany`).
- Checks qualifiers (required vs optional).
- Matches `SemanticId`, `idShort`, type, and value.
- Recurses into nested collections until the full hierarchy is validated.

---

## Example Workflow

1. The Comparator identifies a matching schema Submodel via `SemanticId`.
2. `RecursionFunc.compareSubmodelElements()` traverses all elements.
3. `SMEComparator` enforces multiplicity rules.
4. Results are collected in `ComparisonResult`.

---
```{figure} ./images/ValidationWorkflow.png
---
width: 100%
alt: ValidationWorkflow
name: ValidationWorkflow
---
```

---

[Back: Validation Logic](validation_logic.md) | [Next: Results Visualization](results_visualization.md)
