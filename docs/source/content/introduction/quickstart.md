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

We provide a Starter Kit for setting up BaSyx on our Website [BaSyx.org](https://basyx.org/#/).
By clicking on **Get Started** you will be guided through an interactive setup process including all necessary components and configurations.

```{figure} ./images/starterkit.png
---
width: 80%
alt: BaSyx Starter Kit
name: starterkit
---
```

After you have completed the setup process, you can download the generated configuration files.

Afterwards, you need to unzip the donwloaded file and run the following command inside the folder:

```bash
docker-compose up -d
```

You can acces the BaSyx AAS Web UI by navigating to [http://localhost:3000](http://localhost:3000) in your browser.
From there you are able to interact with the BaSyx components.

One of the first actions could be the upload of a Shell using the upload feature of the AAS Environment.

```{figure} ./images/upload_aas.png
---
width: 80%
alt: BaSyx Starter Kit
name: starterkit
---
```
