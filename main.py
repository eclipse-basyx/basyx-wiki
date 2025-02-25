import os
import pathlib
import sys, time, threading

from basyx.aas import model, adapter
from basyx.aas.adapter import aasx
from waitress import serve

from basyx.aas.backend.local_file import LocalFileObjectStore
from basyx.aas.adapter.http import WSGIApp

storage_path = os.getenv("STORAGE_PATH", "/storage")
storage_type = os.getenv("STORAGE_TYPE", "LOCAL_FILE_READ_ONLY")
base_path = os.getenv("API_BASE_PATH")

wsgi_optparams = {}

if base_path is not None:
    wsgi_optparams["base_path"] = base_path

if storage_type == "LOCAL_FILE_BACKEND":
    application = WSGIApp(LocalFileObjectStore(storage_path), aasx.DictSupplementaryFileContainer(), **wsgi_optparams)

elif storage_type in "LOCAL_FILE_READ_ONLY":
    object_store: model.DictObjectStore = model.DictObjectStore()
    file_store: aasx.DictSupplementaryFileContainer = aasx.DictSupplementaryFileContainer()

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
                    print(f"ERROR: Failed to load {file}. Reason: {e}") #next check the simple url then with file
        elif file.suffix.lower() == ".xml":
            with open(file) as f:
                adapter.xml.read_aas_xml_file_into(object_store, file)
        elif file.suffix.lower() == ".aasx":
            with aasx.AASXReader(file) as reader:
                reader.read_into(object_store=object_store, file_store=file_store)

    if not list(object_store):  # If empty, add a sample AAS
        print("No AAS found, adding a default AAS...")
        aas = model.AssetAdministrationShell(
            identification=model.Identifier("ExampleAAS"),
            asset_information=model.AssetInformation(global_asset_id=model.Identifier("ExampleAsset")),
        )
        object_store.add(aas)
    application = WSGIApp(object_store, file_store, **wsgi_optparams)
    

else:
    print(f"STORAGE_TYPE must be either LOCAL_FILE or LOCAL_FILE_READ_ONLY! Current value: {storage_type}",
          file=sys.stderr)
    
def watch_storage():
    """Monitor storage directory for changes in AAS JSON."""
    last_modified = os.path.getmtime("storage/aas_data.json")
    
    while True:
        time.sleep(5)  # Check every 5 seconds
        if os.path.getmtime("storage/aas_data.json") > last_modified:
            print("⚠️ Detected changes in AAS JSON. Restarting server...")
            os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == "__main__":
    # Start file watcher in a separate thread
    watcher_thread = threading.Thread(target=watch_storage, daemon=True)
    watcher_thread.start()
    print("Starting BaSyx AAS Server on http://localhost:8080/api/v3.0")
    serve(application, host="0.0.0.0", port=8080)