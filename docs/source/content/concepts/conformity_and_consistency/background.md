# Background & Definitions

## Definitions of Conformity
In general, conformity (synonyms: conformance, compliance) indicates whether (or to what extent) something exists/behaves like it was meant/specified/defined/required by something or someone through, e.g., requirements, rules, specifications, etc.
- “The process of conformity assessment demonstrates whether a product, service, process, claim, system or person meets the relevant requirements. Such requirements are stated in standards, regulations, contracts, programmes, or other normative documents.” (https://www.iso.org/conformity-assessment.html)

In computer science, conformity usually refers to whether, e.g., software is built and/or behaves like it is expected based on requirements, specifications, templates, protocols, etc.
- A used term is "conformance testing": "conformance testing where the aim is to check conformance of the SUT to a given specification" [Krichen, 2009, "Conformance testing for real-time systems"] (SUT = system under test)

Therefore, conformity is always a relation between something more "abstract" that acts as specification/plan (ground truth) and then the actual artifact/instance that is specified by the former and thus should be conform to its specification/plan.

## Definitions of Consistency
In general, consistency indicates whether two (or more) objects that share overlapping information represent this shared information in a compatible and non-contradictory way (the joined information would be satisfiable). Unlike conformity, where one object is a specification and the other is an instance of it, consistency concerns peer-level relations between objects.
- Consistency = ""a state in which two or more elements, which overlap in different models of the same system, have a satisfactory joint description" [Lucas et al., 2009, "A systematic
review of UML model consistency management" - based on Spanoudakis & Zisman, 2001, "Inconsistency management in software engineering: Survey and open research issues"]

Based on context:
- In computer science, consistency often refers to the agreement of shared data across different components or systems. For example, in databases, the “C” in ACID stands for consistency, meaning that database transactions must leave the database in a valid state according to predefined integrity rules.
- In model-driven engineering, consistency checking ensures that different models or views that describe overlapping aspects of a system do not contradict each other (consistency of views means “that they do not contradict each other" [Persson et al, 2013, "A Characterization of Integrated Multi-View Modeling in the Context of Embedded and Cyber-Physical Systems"]). For example, a class diagram and a sequence diagram of the same software system should agree on method signatures.
- In general systems engineering, consistency reflects whether multiple artifacts (requirements, architecture descriptions, simulation models, etc.) that describe the same system aspects contain coherent, non-conflicting information.

## Conformity vs. Consistency
Note that "conformity" is similar to but not identical with "consistency". 
- Consistency is a relation between two objects that have an information overlap, i.e., some information exist in both objects and to be called consistent, this information must exist in a specific form/relation in both objects. 
- Conformity is a relation between two objects, where one is usually the specification/plan of the other one (the instance) and the instance needs to match the specification to be called conform (to the specification). 
- Therefore, **conformity can be seen as some kind of specialization of consistency**. For conformity one side is always an instance of something and the other side a specification, whereas both sides can be anything for consistency. For conformity only one direction of the relation is important (from the instance to the specification) instead of both like for consistency. For conformity the overlap or rule is always the same to be called conform: "The instance muss be like the specification has specified", whereas the overlap rule can be anything in the consistency case. 

| Aspect    | Consistency                                                       | Conformity                                             |
| --------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| Relation  | Between peers (two or more artifacts/models with overlap)         | Between instance and specification (directional)       |
| Direction | Bidirectional / multidirectional                                  | One-directional (instance → specification)             |
| Basis     | Shared/overlapping information                                    | Full specification vs. actual instance                 |
| Example   | UML class diagram and sequence diagram agree on method signatures | A digital twin conforms to its metamodel specification |

As a result, we define the "specification/plan" aspect a bit more generic in this project context and partly include consistency in our conformity discussions. Therefore, in the following pages, the [classification theory](./classification_theory.md) is focused on conformity but the actual [implementation and checking](./implementation.md) is then later designed for both conformity and consistency.

## More on Consistency Background
Since we have already published some paper about multi-model consistency checking with enough background information, we will refer to them for further information:
- [Challenges in Multi-View Model Consistency Management for Systems Engineering](https://dl.gi.de/items/01ecc43b-563a-4a0f-b72b-185fd552891e)
- [Towards Confidentiality in Multi-Model Inconsistency Detection for Systems Engineering](https://ieeexplore.ieee.org/abstract/document/10350401)
- [Modular Consistency Checking Between Heterogeneous Models Without Direct Data Exchange Between Collaborators](https://dl.acm.org/doi/10.1145/3652620.3688554)
