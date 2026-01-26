#!/usr/bin/env python3
"""
BaSyx Python SDK Example - Main Script

This script provides a convenient way to run the different parts of the
BaSyx Python SDK example:
  1. Create AAS and Submodel
  2. Start the BaSyx server
  3. Start the visualization dashboard

You can run all steps sequentially or individual steps.
"""

import sys
import subprocess
import os
import time
import threading


def print_header(title):
    """Print a formatted header."""
    print("\n")
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def print_menu():
    """Display the main menu."""
    print_header("BaSyx Python SDK Example")
    print("Choose an option:")
    print()
    print("  1. Create AAS and Submodel (Step 1)")
    print("  2. Start BaSyx Server (Step 2)")
    print("  3. Start Visualization Dashboard (Step 3)")
    print("  4. Run Server and Dashboard together")
    print("  5. Run all steps (1 → 2 → 3)")
    print("  0. Exit")
    print()


def run_script(script_name, wait=True):
    """Run a Python script."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Error: Script {script_name} not found!")
        return False
    
    try:
        if wait:
            result = subprocess.run([sys.executable, script_path], check=True)
            return result.returncode == 0
        else:
            subprocess.Popen([sys.executable, script_path])
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n✓ Interrupted by user")
        return False


def run_step_1():
    """Run Step 1: Create AAS and Submodel."""
    print_header("Running Step 1: Create AAS and Submodel")
    return run_script("create_aas.py")


def run_step_2():
    """Run Step 2: Start BaSyx Server."""
    print_header("Running Step 2: Start BaSyx Server")
    print("⚠️  The server will run until you press Ctrl+C")
    print()
    return run_script("start_server.py")


def run_step_3():
    """Run Step 3: Start Visualization Dashboard."""
    print_header("Running Step 3: Start Visualization Dashboard")
    print("⚠️  The dashboard will run until you press Ctrl+C")
    print()
    return run_script("visualization.py")


def run_server_and_dashboard():
    """Run the server and dashboard in parallel."""
    print_header("Running Server and Dashboard")
    print("Starting BaSyx server and visualization dashboard...")
    print()
    print("⚠️  Both services will run until you press Ctrl+C")
    print()
    print("Access points:")
    print("  • BaSyx API:    http://localhost:8080/api/v3.0/shells")
    print("  • Dashboard:    http://127.0.0.1:8050")
    print()
    
    # Start server in a separate thread
    server_thread = threading.Thread(
        target=run_script,
        args=("start_server.py", False),
        daemon=True
    )
    server_thread.start()
    
    # Give server time to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Start visualization (this will block until Ctrl+C)
    try:
        run_script("visualization.py")
    except KeyboardInterrupt:
        print("\n\n✓ Services stopped gracefully")


def run_all_steps():
    """Run all steps in sequence."""
    print_header("Running All Steps")
    
    # Step 1: Create AAS
    if not run_step_1():
        print("❌ Step 1 failed. Stopping.")
        return False
    
    print("\n✓ Step 1 completed successfully!")
    print("\nPress Enter to continue to Step 2...")
    input()
    
    # Step 2 & 3: Run server and dashboard
    try:
        run_server_and_dashboard()
    except KeyboardInterrupt:
        print("\n\n✓ All services stopped gracefully")
    
    return True


def main():
    """Main function."""
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        
        if choice == "1":
            run_step_1()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            run_step_2()
            
        elif choice == "3":
            run_step_3()
            
        elif choice == "4":
            run_server_and_dashboard()
            
        elif choice == "5":
            run_all_steps()
            
        elif choice == "0":
            print("\nGoodbye!")
            sys.exit(0)
            
        else:
            print("\n❌ Invalid choice. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
