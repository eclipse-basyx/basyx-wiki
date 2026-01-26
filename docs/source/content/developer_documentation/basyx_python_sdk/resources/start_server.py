"""
Step 2: Host AAS and Submodels via BaSyx AAS Repository and Submodel Repository

This script demonstrates how to:
- Load AAS data from JSON files
- Set up a BaSyx AAS and Submodel server
- Serve the data via HTTP API endpoints
"""

import os
import sys
import logging
from basyx.aas.adapter import load_directory
from basyx.aas.adapter.aasx import DictSupplementaryFileContainer
from basyx.aas.backend.local_file import LocalFileObjectStore
from basyx.aas.model.provider import DictObjectStore
from interfaces.repository import WSGIApp
from waitress import serve


def setup_logger() -> logging.Logger:
    """Configure a logger for the server startup sequence."""
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(levelname)s [Server Start-up] %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def start_aas_server():
    """Start the BaSyx AAS and Submodel server."""
    
    logger = setup_logger()
    
    print("=" * 60)
    logger.info("Starting BaSyx AAS Server")
    print("=" * 60)
    
    # Configuration from environment variables (with defaults)
    env_input = os.getenv("INPUT", "storage")
    env_storage = os.getenv("STORAGE", "storage")
    env_storage_persistency = os.getenv("STORAGE_PERSISTENCY", "false").lower() in {"1", "true", "yes"}
    env_storage_overwrite = os.getenv("STORAGE_OVERWRITE", "false").lower() in {"1", "true", "yes"}
    env_api_base_path = os.getenv("API_BASE_PATH")
    
    logger.info(
        "Loaded settings API_BASE_PATH=\"%s\", INPUT=\"%s\", STORAGE=\"%s\", PERSISTENCY=%s, OVERWRITE=%s",
        env_api_base_path or "", env_input, env_storage, env_storage_persistency, env_storage_overwrite
    )
    
    # Build storage configuration
    wsgi_optparams = {"base_path": env_api_base_path} if env_api_base_path else {}
    
    if env_storage_persistency:
        # Use persistent storage backend
        storage_files = LocalFileObjectStore(env_storage)
        storage_files.check_directory(create=True)
        
        if os.path.isdir(env_input):
            input_files, input_supp_files = load_directory(env_input)
            added, overwritten, skipped = storage_files.sync(input_files, env_storage_overwrite)
            logger.info(
                "Loaded %d identifiable(s) and %d supplementary file(s) from \"%s\"",
                len(input_files), len(input_supp_files), env_input
            )
            logger.info(
                "Synced INPUT to STORAGE with %d added and %d %s",
                added,
                overwritten if env_storage_overwrite else skipped,
                "overwritten" if env_storage_overwrite else "skipped"
            )
            object_store = storage_files
            file_store = input_supp_files
        else:
            logger.warning("INPUT directory \"%s\" not found, starting empty", env_input)
            object_store = storage_files
            file_store = DictSupplementaryFileContainer()
    else:
        # Use in-memory storage (read-only)
        if os.path.isdir(env_input):
            object_store, file_store = load_directory(env_input)
            logger.info(
                "Loaded %d identifiable(s) and %d supplementary file(s) from \"%s\"",
                len(list(object_store)), len(list(file_store)), env_input
            )
        else:
            logger.warning("INPUT directory \"%s\" not found, starting empty", env_input)
            object_store = DictObjectStore()
            file_store = DictSupplementaryFileContainer()
    
    # Create the WSGI application
    application = WSGIApp(object_store, file_store, **wsgi_optparams)
    
    # Start the server
    print()
    print("=" * 60)
    logger.info("BaSyx AAS Server is running!")
    print("=" * 60)
    print("Available endpoints:")
    print("  • Root:                http://localhost:8080/")
    print("  • AAS Repository:      http://localhost:8080/api/v3.0/shells")
    print("  • Submodel Repository: http://localhost:8080/api/v3.0/submodels")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    serve(application, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    try:
        start_aas_server()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped gracefully")
        sys.exit(0)
