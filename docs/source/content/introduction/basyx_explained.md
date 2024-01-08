# BaSyx explained

## About BaSyx and changeable production

BaSyx is an open source platform that makes Industrie 4.0 useable and implementable for small- and large enterprises, research institutes, universities, and all other public and private entities that are interested in automation. BaSys 4.0 addresses the changeability of production processes as one major goal of Industrie 4.0. Changeable production addresses unplanned changes of production processes, for example product variants that were not known when the production line was created and came into operation. In contrast, a flexible production addresses a production line with a predefined range of flexibility, e.g. a well-known amount of product variants. Changing a production requires (manual) intervention with the production line. The major goal of BaSyx is to reduce the resulting downtime to a minimum.

A changeable production enables the following:

- Manufacturing of different products / recipes on the same production line. A recipe is a plan that describes the production steps that are necessary for manufacturing a product.
- Dynamically add and remove production resources, e.g. devices.
- Dynamically add and remove device capabilities, e.g. in case of added or removed tools.
- Substitution of devices with semantically equivalent devices.
- Moving (re-deployment) of software components

## Main BaSyx Components

This section defines main BaSyx component types, their interactions, and core interfaces of the BaSys platform. BaSyx components are structured into four layers:

- **Field level:** The field level consists of automation devices, sensors, and actuators without a specific BaSys conforming interface.
- **Device level:** The device level consists of automation devices that offer a BaSys 4.0 conforming interface. Bridging devices that implement BaSys 4.0 conforming interfaces for field devices that do not provide a conforming interface by themselves are part of the device level as well.
- **Middleware level:** The middleware level consists of re-useable Industrie 4.0 components that implement required generic, and plant-independent capabilities for Industrie 4.0 production lines. Registry and Discovery services, protocol gateways, and Asset Administration Shell providers for example reside on the middleware level.
- **Plant level:** The plant level consists of high-level plant components that manage, optimize, and monitor the production.

```{figure} ./images/1536px-BaSyx.Architecture_Overview.png
---
width: 100%
alt: BaSyx architecture overview
name: basyx_architecture_overview
---
Main BaSyx architecture components and their interactions.
```

Predefined component types implement well-defined interfaces based on Virtual Automation Bus (VAB) properties and operations. Predefined component types are mostly on middleware and device level. Other, i.e. non-predefined components implement custom interfaces.

## BaSyx component interaction

Control components provide a service based interface to field devices. Control components are implemented either on device PLC controllers, or as individual entities that connect via device-specific protocols to field devices. Smart devices that implement an BaSys 4.0 interface are native control components.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_2.png
---
width: 100%
alt: BaSyx component interaction 1
name: basyx_cc_1
---
```

Devices, and therefore control components have Asset Administration Shells (AAS). AAS contain sub models that provide information that includes offered services, and live status values. Control components register their offered services in AAS sub models. Live data regarding the component status or sensor values is available through AAS sub models as well.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_3.png
---
width: 100%
alt: BaSyx component interaction 2
name: basyx_cc_2
---
```

BaSys AAS register themselves in a Registry. Thus, dependent applications or other AAS are able to locate them, even if their deployment location changes.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_4.png
---
width: 100%
alt: BaSyx component interaction 3
name: basyx_cc_3
---
```

Group components are control components that do not directly interact with devices. Instead, they interact with other group- and control components to provide higher-level services. Group components also have an AAS.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_5.png
---
width: 100%
alt: BaSyx component interaction 4
name: basyx_cc_4
---
```

The Strategy/Optimization component creates a production plan for a product. It uses the directory to lookup the product and production device AAS. From the product AAS, the strategy/optimization component retrieves the product recipe. It receives available production capacities, associated cost, and all other information that is necessary to map requested product production steps to production devices from device AAS. Based on this information, the Strategy/Optimization component creates a production plan for a product in production that contains when which device will be performing a production step.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_6.png
---
width: 100%
alt: BaSyx component interaction 5
name: basyx_cc_5
---
```

The process control component receives the production plan from the Strategy/Optimization component and executes the production plan. It loads the service IDs of required group- and control components from their AAS. Subsequently, the Process control component does no longer need AAS access for executing scheduled production plans. Multiple implementations are possible for the process control component: on one hand, the component may be a generated group component, on the other hand, a dedicated BPMN process engine, e.g. Activiti can be used.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_7.png
---
width: 100%
alt: BaSyx component interaction 6
name: basyx_cc_6
---
```

BaSyx supports the development of Monitoring components that aggregate data from different AAS and analyze this data, or provide condensed data to dashboards for live production evaluation.

```{figure} ./images/1536px-BaSyx.BaSyx10Mins_8.png
---
width: 100%
alt: BaSyx component interaction 7
name: basyx_cc_7
---
```

Our BaSys architecture therefore consists of seven closely coupled component types that realize an Industrie 4.0 production. In context of the Open-Source BaSyx platform, concrete implementations are being developed for Asset Administration Shell providers, sub model providers, and directory services. We are working on providing reference code for control components and group components that integrate legacy devices, or that run on controllers or runtime environments (RTE) of smart devices. Runtime environments provide a development environment to develop the behavior of smart devices using high-level programming paradigms and furthermore support the easy deployment of code without reflashing. To enable this, we support the development of two open source RTEs, ACPLT and Eclipse 4diac that are able to implement natively BaSys control components. BaSyx will also provide integration for existing open source process engines, as well as examples for aggregating AAS that support data analysis and dashboards. Strategy/Optimization components are highly plant specific. Therefore, BaSyx will provide examples in the context of demonstrators.
