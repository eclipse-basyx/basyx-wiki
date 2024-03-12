About Asset Administration Shells

Asset Administration Shells exist for Products, Resources (e.g. devices), and processes
Asset Administration Shells (AAS) are one main concept of Industrie 4.0 for providing information hiding and higher levels of abstraction for assets. The AAS is the standardized self-description of a technical or logical component in production. Essentially, it is a machine-readable, technology & device-agnostic description of a component that provides access to all of its properties and functions. Basically, the concepts of device description and abstraction are not new. In the smart home area, one finds for example Apple Homekit as a defined interface or different ZigBee profiles and clusters. In the IoT area, there are also defined models such as Eclipse Vorto or Eclipse Ditto.

A fundamental difference between existing solutions and the AAS concept is the manufacturer-independent standardization of the management shell meta model. In the field of production automation, there are currently no standards in this respect that provide such a self-description of systems and devices in a technology-neutral and manufacturer-independent way.

An Asset Administration Shell provides information about Industrie 4.0 assets, a unique identifier for this asset, and a generic interface to information regarding this Industrie 4.0 asset. They turn Assets into digitally manageable assets. Every Industrie 4.0 asset has an Asset Administration Shell that provides access to properties, services, and informs about events. AAS exist for physical and non-physical entities; consequently, devices, workers, products, but also processes may have Asset Administration Shells.


Types of Asset Administration Shells
Currently, three types of Asset Administration Shells are distinguished:

Type 1 Asset Administration Shells are serialized files, e.g. XML, or JSON files. Serialized Asset Administration Shells contain static information and may be distributed as files. Eclipse BaSyx components can transmit and receive Type 1 Asset Administration Shells. The data model of type 1 Asset Administration Shells is defined by the AAS meta model.
Type 2 Asset Administration Shells exist as runtime instances. They are hosted on servers, and may contain both static, i.e. less frequently changing information, but may also interact with other components. This way, Type 2 AAS provide a frontend for example to device services, live data from sensors, products, or real-time availability and delivery times for spare parts. Type 2 Asset Administration Shell provide properties and operations, and is able to signal changing conditions with events. The data model of Type 2 AAS is also defined by the AAS meta model. In addition, the AAS defines a generic runtime interface that enables accessing properties, operations, and events. Type 2 Asset Administration Shells therefore can realize unified interfaces to heterogeneous entities.
Type 3 Asset Administration Shells extend type 2 Asset Administration Shells. They additionally implement an active behavior, i.e. they can start to communicate and to negotiate on their own. VDI/VDE 2139 defines a language for type 3 AAS.


Accessing Asset Administration Shells
AAS communication

Every AAS communicates via a HTTP/REST interface that implements the BaSys Industrie 4.0 communication API
An Asset Administration Shell is accessible via Industrie 4.0 compliant communication. For BaSys 4.0 and Eclipse BaSyx, all AAS are accessible at least via a defined HTTP/REST interface. BaSyx provides server components that can host Type 1 AAS. Type 2 AAS can be hosted on a shared AAS server, or they can be deployed as individual executables in the system. However, every type 2 and type 3 AAS may provide additional means of communication, to support for example high throughput communication or required protocols for specific contexts.

AAS layers

Common layers of an AAS include access to AAS specific functions, but also generic access to operations and properties, as well as communication
The AAS turns an entity into a manageable Industrie 4.0 component. It is the logic representation of an Asset in the digital world. In addition to the common AAS interface, an AAS may implement a specific, asset specific API that eases access to Asset Data and services. The AAS provides access to the entirety of information regarding an Asset. The AAS itself provides generic information, AAS submodel provide more detailed. An Asset Administration Shell enumerates AAS submodels and provides access to them. Asset Administration Shells resemble the communication abilities of the underlying asset. Assets may be active or passive, and therefore, AAS may be active or passive entities as well.

We distinguish between type and instance AAS. A type AAS represents a specific type with common properties, e.g. a device type, which could be a specific type of robot. Instance AAS represent one instance, e.g. one specific robot. Every Industrie 4.0 entity is uniquely represented by its Asset Administration Shell, and therefore each AAS must be identifiable by an unique identifier.

AAS submodels

An Asset Administration Shell usually contains numerous submodels that focus on specific data
An AAS usually contains or references several submodels. Submodels define properties and services, and implement a reflexive interface. They provide high-level information, e.g. regarding offered services of assets, asset status models, or plant topology models.

Submodels may contain properties, functions, events, references, relationships, file & web references and BLOBs. This enables the provision of a wide variety of data as submodels, and the inclusion of many data sources. Sub-models may provide a façade to data sources that did previously require the use of a proprietary interface. They therefore serve as common points of interaction in modern Industrie 4.0 systems.

Asset Administration Shells provide access to meta information about the Industrie 4.0 asset that they represent, and they provide access to submodels. The same asset administration shell may provide access to numerous submodels. Submodels provides access to a focused set of data. This may be physical data, the weight and size of assets, dynamic data, e.g. the availability of spare parts, and live data regarding the condition of a device. AAS submodels may as well export operations that enable, for example, the controlling of a device.

Similar to AAS, also AAS sub models can be realized with BaSyx as Type 1, Type 2, and Type 3 sub models.


AAS and submodel interfaces

AAS and submodels structure information in a tree of properties
An AAS uses a strict, and coherent format, that organizes all contained information as tree of properties. The same format is used for structuring of submodel properties. AAS and submodels define a unified API for accessing AAS information, as well as information in AAS submodels. The concrete API for accessing the AAS and its submodels is described here.

An Asset Administration Shell and its submodels may be distributed through the system. While the AAS resides for example on a server to ensure its presence in case of device failures, submodels may be deployed to the physical device. If the submodel provides access to frequently changing data, its deployment to the device may be the best solution, as otherwise a steady stream of data needs to be transmitted from the device to the submodel location. The distributed AAS approach enables the use of AAS and submodels as decentral data storage and unified interface to data sources. Static data, databases, and tools may be equipped with a submodel interface to provide various kinds of data as AAS submodels.

Asset Administration Shell based BaSyx architecture examples
BaSys 4.0 conforming Industrie 4.0 production systems consist of production assets (devices, workers, products), as well as apps, a registry, as well as AAS and submodel providers. AAS and submodels realize unified interfaces to assets and to different kinds of data and data sources. Several hosts may implement submodel providers; some providers for example persist AAS and submodel data in databases, other providers only offer volatile data.

BaSyx.AAS.ArchitectureExample1.png

The example illustrates a simple BaSys 4.0 architecture. It illustrates the main components of a BaSys 4.0 deployment. The directory registers AAS and provides access to registered Asset Administration Shells and their submodels. Smart devices natively support Asset Administration Shells. They register their Asset Administration Shells autonomously with the directory. Applications, in the shown example a dashboard application, access AAS submodels to receive data from the shopfloor. They also set property values and invoke submodel operations to control the production. Live data updates for submodels are provided by the smart device itself in this example.


BaSyx.AAS.ArchitectureExample2.png

The second scenario differs from the first scenario in one aspect: the integrated device is not a smart device, but a legacy device that supports no Industrie 4.0 communication. An explicit device manager registers the AAS and submodels of the device with the directory of the BaSys middleware, communicates with the device using native protocols, and pushes data into submodels of its device.


Asset Administration Shell Meta Model

The AAS meta model defines relevant types as classes, inter-class relationships, properties of the Asset Administration Shell, and related types, e.g. submodels. Source: Details of the Asset Administration Shell, Part 1
The AAS meta model describes the overall structure of Asset Administration Shells and AAS submodels. It describes the minimal amount of properties and their meanings that every AAS and AAS submodel exports. For each property, the description, the type, and the cardinality is given. The cardinality also defines if a property is optional, i.e. whether the minimum amount of values for that property is zero or greater than zero.

The AAS meta model is defined by the Platform Industrie 4.0, the exact meta model definition can be downloaded from the Platform Industrie 4.0 as "Details of the Asset Administration Shell - Part 1". Eclipse BaSyx provides a reference implementation of the AAS standard. The following descriptions are adapted from that document. Every AAS at least defines the properties described in the AAS meta model.

The following tables describe the attributes of each meta class. Type descriptions and tables were adapted from "Details of the Asset Administration Shell - Part 1"[1]. The security attribute and associated security concepts of the AssetAdministrationShell type will be covered in a specific HowTo document. The meaning of table columns are as following:

Attribute: Defines the attribute name
Type: Defines the type of the attribute
Kind: The kind column defines whether an attribute is a reference (ref) to another object, or whether an attribute is contained (aggr) in the object. An aggregation always belongs to one parent object. In case of references, several objects may create a reference to the same referred object.
Cardinality: Defines the number of references or aggregated elements, as well as whether an attribute is mandatory (minimum cardinality >= 1) or whether it is optional (minimum cardinality = 0).
Description: Explanatory description of the attribute.

Class AssetAdministrationShell


Attribute	Type	Kind	Cardinality	Description
derivedFrom	AssetAdministrationShell	ref	0..1	The reference to the AAS the AAS was derived from.
security	Security	aggr	1	Definition of the security relevant aspects of the AAS.
asset	Asset	ref	1	The asset the AAS is representing.
submodel	Submodel	ref	0..*	The asset of an AAS is typically described by one or more submodels.
conceptDictionary	ConceptDictionary	aggr	0..*	An AAS can have one or more concept dictionaries assigned to it. The concept dictionaries typically contain only descriptions for elements that are also used within the AAS (via HasSemantics)
view	View	aggr	0..*	If needed stakeholder specific views can be defined on the elements of the AAS.

Class HasDataSpecification

The HasDataSpecification base class marks elements that can have data specification templates. A template defines the additional attributes an element may or shall have.

Attribute	Type	Kind	Cardinality	Description
derivedFrom	AssetAdministrationShell	aggr	0..*	Global reference to the data specification template used by the element.

Class Identifiable


Identifiable is the base class for all elements with a globally unique identifier Source: Details of the Asset Administration Shell, Part 1
The class Identifiable is the base class for all elements with a globally unique identifier.

Attribute	Type	Kind	Cardinality	Description
administration	AdministrativeInformation	attr	0..1	Administrative information of an identifiable element. Some of the administrative information like the version number might need to be part of the identification, e.g. when several global identifiers exist for different versions of the same identifiable asset.
identification	Identifier	attr	1	The globally unique identification of the element.

Class Identifier


Identifier is the base class for all elements with a globally unique identifier Source: Details of the Asset Administration Shell, Part 1
The Identifier class is used to uniquely identify an entity. The IdentifierType enumeration defines three kinds of identifiers:

IRDI: IRDI according to ISO29002-5 as an Identifier scheme for properties and classifications.
URI: Identifier of type URI
Custom: Custom identifiers like GUIDs (globally unique Identifiers)
With respect to the global kind of an AAS, we propose a URI based format for the AAS identifier.

Attribute	Type	Kind	Cardinality	Description
idType	IdentifierType	attr	1	Type of the Identifier, e.g. URI, IRDI etc. The supported Identifier types are defined in the enumeration IdentifierType.
id	Id	attr	1	Identifier of the element.

Class AdministrativeInformation

The class AdministrativeInformation contains Administrative meta information for elements; currently, this is the version information.

Attribute	Type	Kind	Cardinality	Description
version	String	attr	0..1	Version of the element.
revision	String	attr	0..1	Revision of the element. The presence of revision information requires the presence of a version.

Class Referable


AAS Referable and Identifiable base classes define different kinds of identifiers Source: Details of the Asset Administration Shell, Part 1
The Referable type is the base class for elements that are referable by their idShort property. This short id is not globally unique. It is id unique only within the name space of an enclosing element.

Attribute	Type	Kind	Cardinality	Description
version	String	attr	0..1	Version of the element.
revision	String	attr	0..1	Revision of the element. The presence of revision information requires the presence of a version.
idShort	String	attr	0..1	Identifying string of the element within its name space.
In case of a referable element not being an identifiable element, the idShort is mandatory and used for referring to the element in its name space. Property idShort shall only feature letters, digits, underscore ("_"); starting mandatory with a letter. Property idShort shall be matched case-insensitive.

In case of an identifiable element idShort is optional but recommended to be defined. It can be used for unique reference in its name space and thus allows better usability and a more performant implementation. In this case it is similar to the “BrowserPath” in OPC UA.

In case the element is a property and the property has a semantic definition (HasSemantics) the idShort is typically identical to the short name in English.

category	String	attr	0..1	The category is a value that gives further meta information with respect to the class of the element. It affects the expected existence of attributes and the applicability of constraints.
The category is not identical to the semantic definition (HasSemantics) of an element. The category could denote that the element is a measurement value whereas the semantic definition of the element would denote that it is the measured temperature.

description	langString	attr	0..1	Description of or comments on the element. The description can be provided in several languages.
parent	Referable	ref	0..1	Reference to the next referable parent element of the element. This element is used to ease navigation in the model and thus it enables more performant implementation. It does not give any additional information.

Class Asset


The Asset base class defines a submodel that provides additional identification information about the managed asset Source: Details of the Asset Administration Shell, Part 1
An Asset describes meta data of an asset that is represented by an AAS. The asset may represent either an asset type or an asset instance. The asset has a globally unique identifier plus – if needed – additional domain specific (proprietary) identifiers.

Attribute	Type	Kind	Cardinality	Description
assetIdentificationModel	Submodel	ref	0..1	A reference to a Submodel that defines the handling of additional domain specific (proprietary) Identifiers for the asset e.g. serial number.

Class HasKind


The HasKind base class defines the Kind property that distinguishes between type and instance AAS Source: Details of the Asset Administration Shell, Part 1
An element with a kind is an element that can represent either a type or an instance. Default for an element is that it is representing an instance.

Attribute	Type	Kind	Cardinality	Description
kind	Kind	attr	0..1	Defines the kind of the element, it is either type or instance. Default value is Instance

Class HasSemantics


The HasSemantics base class enables linking of semantic information Source: Details of the Asset Administration Shell, Part 1
The HasSemantics type is the base type for all elements that link a semantic specification. Semantic specifications are objects that provide a meaning for the element, e.g. an Ontology or a formal specification.

Attribute	Type	Kind	Cardinality	Description
semanticId	Reference	attr	0..1	The identifier of the semantic definition of the element. It is called semantic id of the element. The semantic id may either reference an external global id or it may reference a referable model element of kind=Type that defines the semantics of the element.
In many cases the idShort is identical to the short name within the semantic definition as referenced via this semantic id.

Submodel Meta Model

The submodel meta model defines the submodel type, as well as submodel elements, and base types Source: Details of the Asset Administration Shell, Part 1
A Submodel defines a specific aspect of the asset represented by the AAS. It is used to structure the virtual representation and technical functionality of an AAS into distinguishable parts. Each submodel refers to a well-defined domain or subject matter. Submodels can become standardized and thus become submodel types. Submodels may differ in their life-cycles compared to their respective Asset Administration Shell.

The following tables describes the attributes of submodel and property type meta classes, as well as of their base classes. Type descriptions and tables were adapted from "Details of the Asset Administration Shell - Part 1".


Class Submodel

Attribute	Type	Kind	Cardinality	Description
submodelElement	SubmodelElement	attr	0..*	A submodel consists of zero or more submodel elements.

Class Qualifiable

For qualifiable elements additional qualifiers may be defined. For details on qualifiers and for predefined standardized qualifier types see IEC 62569-1. For example, a level qualifier defining the level type minimal value, maximum value, typical value and nominal value can be found in IEC 62569-1. Additional qualifier types are planned to be defined in the ongoing work of DIN SPEC 92000 like expressions semantics and expression logic.

A formula can be defined if there are no fitting predefined qualifiers or the required qualification is to complex.

Attribute	Type	Kind	Cardinality	Description
qualifier	Constrains	attr	0..*	Additional qualification of a qualifiable element.

Icons on this page are provided by Icons8.com