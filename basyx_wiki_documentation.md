Getting Started with Python Basyx SDK:

This documentation provides a step-by-step guide for setting up an AAS (Asset Administration Shell) & Submodel Creation System, running an API server using the BaSyx Python SDK, and visualizing the data using Dash (web-based visualization) and PyQt5 (GUI viewer).

1. Overview
The system consists of the following components:

* AAS & Submodel Creation (visualize_aas.py):
Creates an AAS with a submodel and its properties.
Saves the generated AAS in aas_data.json (JSON format) in the designated folder (e.g. /storage).

* Hosting AAS and Submodels via BaSyx AAS Repository and Submodel Repository (main.py):
Reads aas_data.json from the designated folder (e.g. /storage) and serves it through the BaSyx AAS & Submodel Servers at:
http://localhost:8080/api/v3.0/shells & http://localhost:8080/api/v3.0/submodels

* Visualization Dashboards for AAS and its submodels:
Dash Web Application (dash_app.py)
Provides an interactive web-based visualization of AAS & submodels.
Runs on http://127.0.0.1:8050.

 [Optional] for visualizing locally PyQt5 GUI Viewer (aas_gui.py) can be used to fetch AAS data from (http://localhost:8080/api/v3.0/shells) and displays it in a GUI.

2. Prerequisites
Ensure you have the following installed on your system:

* Python 3.x (Recommended: 3.8 or higher)
* Pip (Python Package Manager)
* Virtual Environment (Optional but Recommended)
* Docker (Optional For BaSyx AAS & Submodel Server)

Install Required Python Libraries
Run the following command to install dependencies:

```bash
pip install dash pyqt5 requests json
``` 

Alternatively, create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install dash pyqt5 requests json
```

3. Running the Components
Step 1: Create an AAS & Submodel (visualize_aas.py)
Run the script to create an AAS, generate submodels, and save them in JSON format.

```bash
python visualize_aas.py
```

After execution, an aas_data.json file will be created in the project directory (e.g. storage_path = r"C:\Users\chakrabo\Documents\Project_David\basyx-python-sdk\server\app\storage\aas_data.json"), containing AAS information.


Step 2: Start the BaSyx AAS & Submodel Server (main.py)
Run the script to serve AAS & submodel data via BaSyx AAS Repository and Submodel Repository APIs:

```bash
python main.py
```
Once started, visit http://localhost:8080/api/v3.0/shells to verify the AAS data and http://localhost:8080/api/v3.0/submodels are being served.
Example API Response:

{
  "id": "AAS_001",
  "submodels": [
    {
      "id": "SM_001",
      "properties": {
        "name": "Example Submodel",
        "value": "42"
      }
    }
  ]
}

Step 3: Visualizing AAS Data
A. Using Dash Web Application (dash_app.py)
Run the Dash application:

```bash
python dash_app.py
```
Open http://127.0.0.1:8050 in a web browser to visualize the AAS & submodels interactively.

B. Using PyQt5 GUI (aas_gui.py)
Run the PyQt5 GUI Viewer:

```bash
python aas_gui.py
```
This fetches AAS data from http://localhost:8080/api/v3.0/shells and displays it in a Graphical User Interface (GUI).

Notes: visualize_aas.py ensures that any modifications to aas_data.json are reflected to BaSyx AAS & Submodel Server which get available via http://127.0.0.1:8050.
The Dash and PyQt5 GUIs dynamically fetch and visualize AAS data.

4. References

https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/server

https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/sdk/basyx/aas/examples
