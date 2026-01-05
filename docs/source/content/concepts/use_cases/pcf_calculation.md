# Product Carbon Footprint

Reducing and transparently reporting the **Product Carbon Footprint (PCF)** is becoming a key requirement across manufacturing industries. Regulations, customer expectations, and initiatives such as Catena-X or Manufacturing-X increasingly demand traceable, product-level carbon data instead of aggregated company-level metrics.

The **Asset Administration Shell (AAS)** is a natural fit for this challenge. It provides a standardized digital twin structure to describe products, materials, and their relationships across the lifecycle. BaSyx builds on this foundation by enabling **PCF calculation and aggregation directly within the AAS ecosystem**, making carbon data actionable, interoperable, and machine-readable.

## Why PCF Calculation in the AAS?

PCF data is inherently contextual:

* It depends on the materials used
* Their amounts and composition
* Their individual emission factors
* The specific product configuration being manufactured

Traditional PCF tools often operate in isolation, disconnected from engineering, production, and digital twin data. By contrast, the AAS allows PCF data to be:

* Linked directly to product types and instances
* Derived from material shells/submodels
* Versioned, exchanged, and validated using standardized interfaces

This enables PCF to become a first-class digital twin property, rather than a static report.

## PCF Support in BaSyx

BaSyx provides an integrated PCF workflow through a dedicated PCF Process module and a PCF submodel plugin in the BaSyx AAS Web UI.

```{figure} images/pcf_material_selection.png
---
name: pcf_material_selection
---
Material selection for PCF calculation in the BaSyx AAS Web UI.
```

Key capabilities include:

* **Product-centric PCF calculation**
  
  PCF is calculated for a concrete product instance based on a selected product type and its used materials.
* **Type → Instance workflow**
  
  A product Type AAS is used as the template. The PCF process creates a new Instance AAS that represents the manufactured product with its calculated PCF.
* **Material-based aggregation**
  
  Users select materials and specify quantities. The resulting PCF is aggregated from the referenced material data.
* **Standard-compliant modeling**
  
  The calculated result is stored as a dedicated PCF Submodel, fully compliant with the AAS metamodel and ready for exchange.
* **End-to-end AAS integration**
  
  The entire workflow is executed using standard AAS concepts and BaSyx components; no external PCF tooling required.

```{hint}
The PCF Process module is meant to serve as a reference implementation and starting point when working with PCF in BaSyx. It can be extended or replaced to fit specific PCF methodologies, data sources, or calculation rules. Scalable implementations may integrate with external LCA databases or services.
```

## Example Setup

BaSyx provides a complete, runnable example that demonstrates the PCF workflow for a product made from multiple materials.

```{note}
PCF calculation <a href="https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/PcfCalculation" target="_blank">Example on GitHub</a>. Feel free to try it out yourself!
```

The example includes:

* Product Type AAS
* Material AAS with emission data
* Automated creation of a Product Instance AAS
* A generated PCF Submodel containing aggregated CO₂ equivalents

The setup can be started locally using Docker Compose and explored via the BaSyx AAS Web UI.

## Role of the PCF Submodel

The generated PCF Submodel serves as a machine-readable carbon footprint representation that can be:

* Queried via AAS APIs
* Exchanged across organizations
* Embedded into AASX packages
* Integrated into sustainability reporting pipelines
* Used as input for higher-level analytics and optimization

Because it is part of the AAS, it can be combined with:

* Bill of Materials (BOM) submodels
* Process or energy submodels
* Supply-chain or lifecycle data

## Real-World Application Scenarios

Typical use cases for PCF calculation with BaSyx include:

* **Sustainable product design**
  
  Compare material choices and configurations based on their PCF impact.
* **Supply-chain transparency**
  
  Exchange PCF-enriched product twins across company boundaries.
* **Regulatory reporting**
  
  Provide auditable, standardized PCF data at product level.
* **Digital Product Passports**
  
  Use PCF Submodels as building blocks for upcoming DPP requirements.
* **Manufacturing-X / Catena-X ecosystems**
  
  Enable interoperable, trusted PCF data exchange using AAS standards.

## Additional Resources

* [BaSyx Web UI Documentation](../../user_documentation/basyx_components/web_ui/index.md)
* <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples" target="_blank">BaSyx Examples on GitHub</a>
* <a href="https://industrialdigitaltwin.org/wp-content/uploads/2025/03/IDTA-02023_Submodel_CarbonFootprint.pdf" target="_blank">PCF Submodel Specification</a>
