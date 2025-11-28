# AAS Query Language

In industrial Digital Twin environments, large numbers of Asset
Administration Shells (AAS), Submodels, and Concept Descriptions are
managed across distributed systems. While standard AAS APIs provide
structured access to individual elements, advanced use cases require
**powerful, flexible, and efficient search capabilities across the
entire AAS landscape**.

The **AAS Query Language** addresses this need by providing a
**unified, expressive query mechanism** to search for AAS, Submodels,
Concept Descriptions, and their descriptors. It enables users to perform
complex filtering, logical operations, and semantic-based searches
across all registered Digital Twin data.

Internally, the BaSyx query functionality is backed by
**Elasticsearch**, providing scalability, high performance, and fuzzy
search capabilities while exposing a domain-specific query interface
tailored to the AAS meta-model.

``` {note}
A fully working example of the AAS Query Language is available in the official BaSyx examples on <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxQueryLanguage" target="_blank">GitHub</a>.
```

------------------------------------------------------------------------

## Motivation and Use Case

As Digital Twin environments grow, organizations quickly face challenges such
as:

-   Finding specific assets among thousands of AAS
-   Searching Submodels by semantic identifiers or versions
-   Locating assets by endpoints, asset kind, or metadata
-   Filtering Concept Descriptions by language or reference relations
-   Querying registries for deployment, discovery, and orchestration

The **AAS Query Language** enables all of these scenarios through
a **single, consistent query interface** that works across multiple
BaSyx repositories and registries.

------------------------------------------------------------------------

## Example Setup Overview

The example provides a **preconfigured BaSyx environment** with:

-   Multiple Asset Administration Shells
-   Several Submodels per AAS
-   Concept Descriptions
-   Registries for AAS and Submodels
-   An integrated Elasticsearch backend

All components are deployed as **Docker containers** to ensure easy
setup and reproducibility.

------------------------------------------------------------------------

## Running the AAS Query Language Example

To start the example environment:

1.  Open a terminal in the example folder
2.  Start all BaSyx containers:

    ``` bash
    docker-compose up -d
    ```

``` {note}
Docker must be installed on your system in order to run this example.
```

------------------------------------------------------------------------

## Exploring the Query Functionality via Web UI

After starting the containers, you can interact with the query system
using the **BaSyx AAS Web UI**:

-   Open the BaSyx Web UI
-   Navigate to the **AAS Query Language Module**
-   Select the target component (Repository or Registry)
-   Enter your query in the text area
-   Execute the query and inspect the result set

------------------------------------------------------------------------

## Inspecting Elasticsearch via Kibana

The BaSyx query infrastructure uses **Elasticsearch** as its search
backend. To explore the indexed data directly, you can access
**Kibana**:

-   URL: `http://localhost:5601`
-   Username: `elastic`
-   Password: `vtzJFt1b`

Kibana allows you to:

-   Inspect AAS, Submodel, and Concept Description indices
-   Perform raw Elasticsearch queries
-   Visualize indexed Digital Twin data
-   Debug indexing and query behavior

------------------------------------------------------------------------

## Query Endpoints Overview

| Component                       | Endpoint                         |
|---------------------------------|----------------------------------|
| AAS Repository                  | `/query/shells`                  |
| Submodel Repository             | `/query/submodels`               |
| Concept Description Repository  | `/query/concept-descriptions`    |
| AAS Registry                    | `/query/shell-descriptors`       |
| Submodel Registry               | `/query/submodel-descriptors`    |

------------------------------------------------------------------------

## Getting Started

1.  Start the BaSyx Docker environment
2.  Explore the Web UI query module
3.  Inspect Elasticsearch via Kibana
4.  Execute the example queries
5.  Integrate the query endpoints into your own applications

------------------------------------------------------------------------

## Additional Resources

For more information about AAS Query Language:

- [BaSyx Components Documentation](../../user_documentation/basyx_components/index.md)
- [IDTA Documentation](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/query-language.html)

