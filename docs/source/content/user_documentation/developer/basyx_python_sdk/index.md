# Getting Started with Python Basyx SDK

This documentation provides a step-by-step guide for setting up an AAS (Asset Administration Shell) & Submodel Creation System, running an API server using the BaSyx Python SDK, and visualizing the data using Dash (web-based visualization) and PyQt5 (GUI viewer).

## Overview
The system consists of the following components:

* **AAS & Submodel Creation (visualize_aas.py):**
Creates an AAS with a submodel and its properties.
Saves the generated AAS in aas_data.json (JSON format) in the designated folder (e.g. /storage).

* **Hosting AAS and Submodels via BaSyx AAS Repository and Submodel Repository (main.py):**
Reads aas_data.json from the designated folder (e.g. /storage) and serves it through the BaSyx AAS & Submodel Servers at:
[http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells) & [http://localhost:8080/api/v3.0/submodels](http://localhost:8080/api/v3.0/submodels)

* **Visualization Dashboards for AAS and its submodels:**
- Dash Web Application (dash_app.py)
Provides an interactive web-based visualization of AAS & submodels. It runs on [http://127.0.0.1:8050](http://127.0.0.1:8050).

- [Optional] for visualizing locally PyQt5 GUI Viewer (aas_gui.py) can be used to fetch AAS data from [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells) and display it in a GUI.

## Prerequisites
 Ensure you have the following installed on your system:

- Python 3.x (Recommended: 3.8 or higher)
- Pip (Python Package Manager)
- Virtual Environment (Optional but Recommended)
- Docker (Optional For BaSyx AAS & Submodel Server)

* Install Required Python Libraries
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

## Running the Components

**Step 1:** Create an AAS & Submodel (visualize_aas.py)
Run the script to create an AAS, generate submodels, and save them in JSON format.

```bash
python visualize_aas.py
```

After execution of the script, an aas_data.json file will be created in the project directory containing AAS information. As you see in the below code snippet, you can define the path where you want the generated json file to be stored.

```python
storage_path = r"C:\Users\chakrabo\Documents\Project_David\basyx-python-sdk\server\app\storage\aas_data.json"
```

As part of creating the sample AAS and its submodels you can define their identifier, repective fields and properties in the following format:

```python
aas_identifier = "https://example.com/AAS"
submodel_identifier = "https://example.com/Submodel"

asset_info = model.AssetInformation(asset_kind=model.AssetKind.INSTANCE, global_asset_id="Asset1")

aas = model.AssetAdministrationShell(asset_information=asset_info, id_=model.Identifier(aas_identifier))

submodel = model.Submodel(id_=model.Identifier(submodel_identifier))
submodel_reference = model.ModelReference.from_referable(submodel)

aas.submodel.add(submodel_reference)

# Add Properties
prop1 = model.Property(id_short="Temperature", value_type=model.datatypes.Float, value=25.3, semantic_id=model.ExternalReference(
                (model.Key(
                    type_=model.KeyTypes.GLOBAL_REFERENCE,
                    value='http://acplt.org/Properties/FirstSimpleProperty'
                ),)
            ))
prop2 = model.Property(id_short="Pressure", value_type=model.datatypes.Integer, value=100,  semantic_id=model.ExternalReference(
                (model.Key(
                    type_=model.KeyTypes.GLOBAL_REFERENCE,
                    value='http://acplt.org/Properties/SecondSimpleProperty'
                ),)
            ))
```            

For more details you can refer to the whole script: [visualize_aas.py](./scripts/visualize_aas.py)

**Step 2:** Start the BaSyx AAS & Submodel Server (main.py)
Run the script to serve AAS & submodel data via BaSyx AAS Repository and Submodel Repository APIs:

```bash
python main.py
```
As you can see from the below code snippet, main script will try to read the generated json (aas_data.json) file and host the content through Basyx AAS and submodel servers.

```python
with open("storage/aas_data.json") as f:
        print(f.read())

    for file in pathlib.Path(storage_path).iterdir():
        if not file.is_file():
            continue
        print(f"Loading {file}")

        if file.suffix.lower() == ".json":
            print(f"DEBUG: Attempting to load {file}")
            with open(file) as f:
                try:
                    adapter.json.read_aas_json_file_into(object_store, f)
                    print(f"DEBUG: Successfully loaded {file}. Object store now contains: {list(object_store)}")
                except Exception as e:
                    print(f"ERROR: Failed to load {file}. Reason: {e}") 
```                    

Once started, visit [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells) to verify the AAS data .

```{figure} ./images/Basyx_AAS_server.png
---
figclass: margin
alt: About BaSyx Python SDK's AAS Repository
name: Basyx_AAS_server
---
```

Visit [http://localhost:8080/api/v3.0/submodels](http://localhost:8080/api/v3.0/submodels) to verify the submodel data.

```{figure} ./images/Basyx_submodel_server.png
---
figclass: margin
alt: About BaSyx Python SDK's Submodel Repository
name: Basyx_Submodel_server
---
```

For more reference here's the whole script: [main.py](./scripts/main.py)

**Step 3:** Visualizing AAS Data

A. Using Dash Web Application (dash_app.py)
Run the Dash application:

```bash
python dash_app.py
```

Open [http://127.0.0.1:8050](http://127.0.0.1:8050) in a web browser to visualize the AAS & submodels interactively.

```{figure} ./images/AAS_submodel_visualization_with_dash.png
---
figclass: margin
alt: About visualizing the AAS and submodel data through Dash Web App
name: AAS_&_Submodel_visualization_with_dash_web_app
---
```

For more reference here's the whole script: [dash_app.py](./scripts/dash_app.py)

B. Using PyQt5 GUI (aas_gui.py)
Run the PyQt5 GUI Viewer:

```bash
python aas_gui.py 
```

This fetches AAS data from [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells) and displays it in a Graphical User Interface (GUI).

```{figure} ./images/AAS_visualization_with_pyQt.png
---
figclass: margin
alt: About visualizing the AAS data through PyQt
name: AAS_visualization_with_pyQt
---
```

For more reference here's the whole script: [aas_gui.py](./scripts/aas_gui.py)

Notes: visualize_aas.py ensures that any modifications to aas_data.json are reflected to BaSyx AAS & Submodel Server which get available via [http://127.0.0.1:8050](http://127.0.0.1:8050). The Dash and PyQt5 GUIs dynamically fetch and visualize AAS data.

## References

[GitHub basyx server](https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/server)

[GitHub basyx aas](https://github.com/eclipse-basyx/basyx-python-sdk/tree/main/sdk/basyx/aas)
