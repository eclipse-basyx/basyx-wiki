# BaSyx Python SDK

This documentation provides a step-by-step guide for setting up an AAS (Asset Administration Shell) & Submodel Creation System, running an API server using the BaSyx Python SDK, and visualizing the data using Dash (web-based visualization). An **interactive Jupyter Notebook** is available, allowing users to execute and experiment with the setup step by step.

For more examples and detailed explanations, see:
- BaSyx Python SDK [Tutorials](https://github.com/eclipse-basyx/basyx-python-sdk/blob/main/sdk/README.md#examples-and-tutorials)
- BaSyx Python SDK [Documentation](https://basyx-python-sdk.readthedocs.io/en/latest/)

## Overview

### **Jupyter Notebook for Interactive Execution**
  - [Basyx_Python_SDK_Starter.ipynb](./Basyx_Python_SDK_Starter.ipynb) provides a step-by-step interactive guide for setting up and running AAS & Submodels.
  - Users can perform the below activities step-by-step by executing code cells and modifying parameters dynamically.

* **AAS & Submodel Creation**
  - Creates an AAS with a submodel and its properties.
  - Saves the generated AAS in `aas_data.json` in the designated folder (`/storage`).

* **Hosting AAS and Submodels via BaSyx AAS Repository and Submodel Repository**
  - Reads `aas_data.json` from the designated folder (`/storage`) and serves it through the BaSyx AAS & Submodel Servers at:
    - **AAS Endpoint:** [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells)
    - **Submodel Endpoint:** [http://localhost:8080/api/v3.0/submodels](http://localhost:8080/api/v3.0/submodels)

* **Visualization Dashboards for AAS and its Submodels**
  - **Dash Web Application**  
    - Provides an interactive web-based visualization.
    - Runs on [http://127.0.0.1:8050](http://127.0.0.1:8050).
  

## **Running the Jupyter Notebook**

To install notebook, run:

```bash
pip install notebook
``` 

To open the notebook, run:

```bash
jupyter notebook
```

## Prerequisites
 Ensure you have the following installed on your system:

- Python 3.x (Recommended: 3.8 or higher)
- Pip (Python Package Manager)
- Virtual Environment (Optional but Recommended)


## References

[GitHub - BaSyx Python server](https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/server)

[GitHub - BaSyx AAS in Python](https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/sdk/basyx/aas)
