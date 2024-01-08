# Quick Start Guide

The quick start guide provides an introductory example for getting started with Eclipse BaSyx V2.
The overall rationale of Eclipse BaSyx is to enable digital manufacturing processes.
Digital manufacturing processes are fully digitized, i.e. they have digital representatives for assets, for the process itself, and for the products.
Digital representatives cover all relevant aspects of their real-world counterpart.
Eclipse BaSyx realizes these digital representatives with the Asset Administration Shell (AAS).
The AAS is therefore a digital substitute for an entity that is relevant for a production process.

## Prerequisites

The introductory example uses the Basyx V2 off-the-shelf Docker components.
Therefore, you need to have Docker installed on your machine.

Dockers official documentation provides a [detailed installation guide](https://docs.docker.com/get-docker/) for Windows, Mac and Linux.

## Setup

To setup the introductory example, you need to clone the BaSyx Java Server SDK Repository:

```bash
git clone https://github.com/eclipse-basyx/basyx-java-server-sdk.git
```

Afterwards, you need to navigate to the `examples` directory inside the cloned `basyx-java-server-sdk` directory and run the following command:

```bash
docker-compose up -d
```

This starts the following components:

- AAS Repository (http://localhost:8081/shells)
- Submodel Repository (http://localhost:8081/submodels)
- ConceptDescription Repository (http://localhost:8081/concept-descriptions)
- AAS Registry (http://localhost:8082/api/v3.0/shell-descriptors)
- AAS Web UI (http://localhost:3000)

```{note}
As of right now you have to register all Asset Administration Shells manually (possible through the UI).
```

You can use the following endpoints to register Asset Administration Shells which are included in the introductory example:

```bash
http://localhost:8081/shells/aHR0cHM6Ly9odHctYmVybGluLmRlL2lkcy9hYXMvZGVtb2Fhc3Yz
```

```bash
http://localhost:8081/shells/aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vMjQxMV83MTYwXzAxMzJfNDUyMw==
```

```bash
http://localhost:8081/shells/aHR0cHM6Ly9hY3BsdC5vcmcvVGVzdF9Bc3NldEFkbWluaXN0cmF0aW9uU2hlbGw=
```

```bash
http://localhost:8081/shells/aHR0cHM6Ly9hY3BsdC5vcmcvVGVzdF9Bc3NldEFkbWluaXN0cmF0aW9uU2hlbGxfTWFuZGF0b3J5
```

```bash
http://localhost:8081/shells/aHR0cHM6Ly9hY3BsdC5vcmcvVGVzdF9Bc3NldEFkbWluaXN0cmF0aW9uU2hlbGwyX01hbmRhdG9yeQ==
```

```bash
http://localhost:8081/shells/aHR0cHM6Ly9hY3BsdC5vcmcvVGVzdF9Bc3NldEFkbWluaXN0cmF0aW9uU2hlbGxfTWlzc2luZw==
```

```{figure} ./images/register_aas.png
---
width: 100%
alt: Register AAS
name: register_aas
---
Register Asset Administrations Shells via the Basyx AAS Web UI.
```