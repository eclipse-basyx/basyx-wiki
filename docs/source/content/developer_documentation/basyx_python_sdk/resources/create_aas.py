"""
Step 1: Create a sample AAS with Submodel and its properties

This script demonstrates how to:
- Create an Asset Administration Shell (AAS)
- Define a Submodel with properties
- Save the AAS and Submodel to a JSON file
"""

import os
from basyx.aas import model
from basyx.aas.adapter.json import write_aas_json_file


def create_aas_and_submodel():
    """Create an AAS with a submodel and save it to JSON."""
    
    # Get the current working directory and set storage path
    current_dir = os.getcwd()
    storage_dir = os.path.join(current_dir, "storage")
    storage_path = os.path.join(storage_dir, "aas_data.json")
    
    # Create storage directory if it doesn't exist
    os.makedirs(storage_dir, exist_ok=True)
    
    print("=" * 60)
    print("Step 1: Creating AAS and Submodel")
    print("=" * 60)
    
    # Define identifiers for AAS and Submodel
    aas_identifier = "https://example.com/AAS"
    submodel_identifier = "https://example.com/Submodel"
    
    # Create Asset Information
    # The AssetInformation describes the asset that the AAS represents
    asset_info = model.AssetInformation(
        asset_kind=model.AssetKind.INSTANCE,
        global_asset_id="Asset1"
    )
    
    # Create the Asset Administration Shell
    aas = model.AssetAdministrationShell(
        asset_information=asset_info,
        id_=model.Identifier(aas_identifier)
    )
    
    # Create a Submodel
    # Submodels contain the actual data and functionality
    submodel = model.Submodel(id_=model.Identifier(submodel_identifier))
    
    # Create a reference to the submodel and add it to the AAS
    submodel_reference = model.ModelReference.from_referable(submodel)
    aas.submodel.add(submodel_reference)
    
    # Define Properties for the Submodel
    # Properties are the basic data elements in AAS
    
    # Property 1: Temperature
    prop1 = model.Property(
        id_short="Temperature",
        value_type=model.datatypes.Float,
        value=25.3,
        semantic_id=model.ExternalReference((
            model.Key(
                type_=model.KeyTypes.GLOBAL_REFERENCE,
                value='http://acplt.org/Properties/FirstSimpleProperty'
            ),
        ))
    )
    
    # Property 2: Pressure
    prop2 = model.Property(
        id_short="Pressure",
        value_type=model.datatypes.Integer,
        value=100,
        semantic_id=model.ExternalReference((
            model.Key(
                type_=model.KeyTypes.GLOBAL_REFERENCE,
                value='http://acplt.org/Properties/SecondSimpleProperty'
            ),
        ))
    )
    
    # Add properties to the submodel
    submodel.submodel_element.add(prop1)
    submodel.submodel_element.add(prop2)
    
    # Save the AAS and Submodel to JSON
    data = model.DictObjectStore()
    data.add(aas)
    data.add(submodel)
    
    write_aas_json_file(storage_path, data)
    
    print(f"✓ AAS created with ID: {aas_identifier}")
    print(f"✓ Submodel created with ID: {submodel_identifier}")
    print(f"✓ Added 2 properties: Temperature (25.3°C), Pressure (100 bar)")
    print(f"✓ Data saved to: {storage_path}")
    print()


if __name__ == "__main__":
    create_aas_and_submodel()
