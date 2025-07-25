# Why use BaSyx?

Eclipse BaSyx is the official open source reference implementation of the BaSys 4 middleware. It is provided by the Eclipse Foundation under the Massachusetts Institute of Technology License (MIT). Thus it is freely usable and may also be used as part of commercial and closed-source applications. This section introduces central concepts of Eclipse-BaSyx.

## Why using Eclipse Basyx as Industrie 4.0 middleware?

Eclipse BaSyx is a middleware that supports the implementation of Industrie 4.0 production environments. It connects relevant production assets implements all components that are necessary for the end-to-end digitalization of Industrie 4.0. Eclipse Basyx also supports, implements and constantly evaluates existing or still developing standards such as the administration shell of the Industry 4.0 platform. So, there is no need to implement these standards by yourself, just start using our proven implementation! The participation of Eclipse BaSyx representatives in relevant standardization committees ensures that a uniform reference implementation implements and integrates the relevant Industry 4.0 standards.

But why should you use BaSyx, and what does make Eclipse BaSyx special and superior to other Industrie 4.0 solutions? Eclipse BaSyx integrates with numerous open-source tools that create an Industrie 4.0 ecosystem and deliver useable applications out-of-the box.

```{figure} ./images/600px-Basyx.overview.png
---
width: 60%
alt: BaSyx overview
name: basyx_overview
---
Architecture overview and the most important components of eclipse BaSyx. Icons by icons8.com.
```

Core concepts of BaSyx are Asset Administrative Shells (AAS), AAS sub models, and Control Components. AAS and AAS sub models are deployed to AAS servers, and can be located through directories. Backend storage enables persistency; existing data can be integrated as AAS sub models to provide this data through a unified interface. Control components realize a unified and service-based interface to devices, AAS sub models describe the available device services. The serviced-based interface enables the tailored production of every product – every product and work piece may be created using its own unique recipe. Small lot sizes become possible, as every work-piece may define a unique set of parameter, and production steps. The Virtual Automation Bus enables end-to-end communication between all devices, and IT systems, such as ERP, and MES systems. Currently, HTTP, OPC-UA, and MQTT communication is already supported. Furthermore, we plan to integrate Apache PLC4X to connect to field bus systems. Components of Eclipse BaSyx may be used independently from each other. Infrastructure components that include AAS repositories, AAS servers, data connectors for sub models, storage interfaces, and AAS directories empower you to start realizing an Industrie 4.0 solution today. When using Eclipse BaSyx to create your infrastructure, you choose which features you like to use, and at the same time, you create a foundation for future applications. Numerous applications integrate with Eclipse BaSyx to enable a large number of Industrie 4.0 use-cases. The following show applications that were realized with Eclipse BaSyx up to now:

- Create Predictive Maintenance applications with Eclipse StreamSheets
- Create Dashboards with Eclipse StreamPipes
- Connect to MES and ERP Systems, and to other data sources using Node.RED
- React to events in your production – notify operators about exceptions
- Document your production processes and your products using digital twins
- Connect to legacy devices using OPC-UA, http/REST, and proprietary protocols
- And in the future much more that we do not even think about today :-)

Eclipse BaSyx consists of all necessary components for realizing Industrie 4.0, and to stay on the leading edge regarding the relevant standards. And of course, we deliver these components as Open-Source software, and as Containers.

## Eclipse BaSyx USPs

What are the most important USPs of Eclipse BaSyx? We have collected a few shiny properties of Eclipse BaSyx that makes it special:

**Keep data where it belongs:** There is no need to send all data into the cloud. BaSyx integrates with your existing infrastructure, therefore you do not need an additional network to get Data from your machines into the cloud. You decide where your data is stored and processed. Eclipse BaSyx keeps data, data analysis, and control close to where it belongs. Most data is relevant for the process and product only. Are you creating a product documentation? You can either keep raw data in the Digital Twin of the product, or you can have the evaluation algorithms travel through your process, together with the digital twin of your product. Only exceptions need to be stored in this case. And of course, you can forward all data that you like to cloud services. But you do not have to.

**Unified interfaces:** Asset Administration Shells (AAS) realize unified interfaces for all production-relevant assets. We use the AAS and its sub models as technical foundation for Digital Twins: Digital twins contain not only administrative information about assets, but also live sensor data, optional prediction models, and all other asset related information. The unified AAS interface enables the rapid development and integration of new applications.

**Implement decentral production systems:** Asset Administration Shells and sub-models are distributed in your production. You decide where to deploy an AAS, and its sub models. Is it necessary to have a product AAS following its product? No problem. Do you need to provide product documentation to stakeholders? No problem! Asset administration shells can be serialized and transferred either as file, or directly to another BaSyx AAS server. You decide which data is transferred to others, and which sub models will be stripped prior to the AAS transfer.

**Lot-size 1:** The markets are changing, and companies that are able to react quickly to changing markets will have a competitive advantage. An efficiently changeable production has numerous advantages: with decreasing product lifetimes, the product numbers that contribute to earnings decrease. In future, less products will be produced for a product type, and therefore set-up cost for production needs to be distributed on smaller product numbers. Efficiently changeable processes drastically decrease setup-costs and lead to a direct competitive advantage. Furthermore, customers are willing to pay more money for individualized/customized products. Being able to produce small lot sizes efficiently may open up whole new markets.

**Smart products:** Industrie 4.0 enables a new kind of products: Smart products are products that are accompanied by their digital twins. Digital twins document production steps: they are for example certificates of authenticity to prevent plagiarism, documents the CO2 footprint of products, or prove quality standards.

**Tailored system architectures:** Eclipse BaSyx empowers you to realize your tailored and scalable system architectures – right as you need them.

## The Eclipse BaSyx Project

The Eclipse BaSyx project is divided into the following parts:

- Reference implementations of Industrie 4.0 components that provide an Industrie 4.0 middleware layer
- The Software Development Kits (SDKs) that enable the development of own components and applications, as well as the integration of existing devices
- Examples that document the application of Eclipse BaSyx and the creation of Industrie 4.0 environments

All BaSys architecture elements are available as abstract interfaces to enable the realization of components and services independently of the SDKs. Standardized implementations (mappings) for various technologies (e.g. HTTP/REST, OPC UA or BaSyx native) do exist. These mappings ensure the cross-technology communication of the components based on a standardized information model. Additional technologies may be added at any time to integrate them into the BaSyx platform. BaSyx also specifies defined, e.g. OPC-UA and HTTP-rest based interfaces. This enables the development of alternative compatible documents, as well as use of BaSyx components without the SDK, and even from different programming languages. This guarantees interoperability also with implementations that are not based on Eclipse-BaSyx SDKs.

Currently, three different programming languages are supported by Eclipse BaSyx, some with different orientations: The SDKs for Java and C# offer the full functionality of BaSyx and are also suitable for the definition and development of new industry 4.0 applications and services. The functional scope of the C++ SDK mainly aims at the integration of existing devices and real-time controllers.
