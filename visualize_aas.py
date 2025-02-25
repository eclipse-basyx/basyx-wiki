import plotly.graph_objects as go
import networkx as nx
from basyx.aas import model
from basyx.aas.adapter.json import write_aas_json_file
import json, os

storage_path = r"C:\Users\chakrabo\Documents\Project_David\basyx-python-sdk\server\app\storage\aas_data.json"
# Get the absolute path of visualize_aas.py
#current_dir = os.path.dirname(os.path.abspath(__file__))

# Set storage directory relative to the server directory
#storage_path = os.path.abspath(os.path.join(current_dir, "../../../server/app/storage/aas_data.json"))

# Step 1: Create an AAS with a Submodel and Properties
aas_identifier = "https://example.com/AAS"
submodel_identifier = "https://example.com/Submodel"

# Use AssetInformation instead of Asset
#asset_info = model.AssetInformation(global_asset_id=model.Identifier("Asset1"))
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
submodel.submodel_element.add(prop1)
submodel.submodel_element.add(prop2)

# Step 2: Convert to JSON
data = model.DictObjectStore()
data.add(aas)
data.add(submodel)
#write_aas_json_file("aas_data.json", data)
#write_aas_json_file("storage/aas_data.json", data)
write_aas_json_file(storage_path, data)
print(f"AAS data has been successfully saved to {storage_path}")

#print("AAS data has been successfully saved to aas_data.json")

