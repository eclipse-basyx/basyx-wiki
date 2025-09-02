# Conformity & Consistency Checking

This subsection introduces the concepts, theoretical foundations, and practical implementation of conformity and consistency checking in the context of digital twins and multi-model systems as the result of the research project BaSys4Transfer. 

Conformity and consistency checking are essential to ensure that models, artifacts, and physical assets behave and interact as intended, follow agreed-upon standards, and remain reliable across their lifecycle. Without such checks, mismatches between specifications and instances or between related models can lead to interoperability issues, errors in system behavior, or even failures in safety-critical domains.
There is a need to detect these inconsistencies as early as possible during the development phase to reduce the cost of solving them (the later an inconsistency is detected, e.g., not until the actual integration/deployment, the more costly it might get to handle it).

The scope of this subsection covers three complementary perspectives:

- [Background & Definitions](./background.md) – providing core terminology and clarifying the distinction between conformity and consistency.
- [Classification Theory](./classification_theory.md) – outlining a structured way to categorize different types of conformity relations and criteria for comparison.
- [Implementation of the Checker](./implementation.md) – presenting the developed tool, its architecture, and how it can be deployed and tried out in an open-source container environment.

Together, these pages provide both the theoretical basis and a concrete implementation for applying conformity and consistency checking in research and practice, with a focus on the digital twin ecosystem but extensible to broader engineering and systems contexts.

```{toctree}
:hidden:
:maxdepth: 1

background
classification_theory
implementation
```
