#!/usr/bin/env python3
"""
Test runner script for Little Lemon API

This script provides convenient commands to run different types of tests.

Usage:
    python run_tests.py [options]

Options:
    --all          Run all tests (default)
    --models       Run model tests only
    --api          Run API endpoint tests only
    --auth         Run authentication tests only
    --permissions  Run permission tests only
    --serializers  Run serializer tests only
    --verbose      Run tests with verbose output
    --coverage     Run tests with coverage reporting (requires coverage package)
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description="Running tests"):
    """Run a shell command and return the result"""
    print(f"\n{description}...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode == 0

def main():
    """Main test runner function"""
    base_dir = Path(__file__).parent
    manage_py = base_dir / "manage.py"
    
    if not manage_py.exists():
        print("Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Parse command line arguments
    args = sys.argv[1:]
    verbose = "--verbose" in args or "-v" in args
    coverage = "--coverage" in args
    
    # Base command
    base_cmd = ["python3", str(manage_py), "test"]
    
    # Determine which tests to run
    if "--models" in args:
        base_cmd.append("LittlelemonAPI.tests.ModelTestCase")
        description = "Running model tests"
    elif "--api" in args:
        base_cmd.extend([
            "LittlelemonAPI.tests.MenuAPITestCase",
            "LittlelemonAPI.tests.BookingAPITestCase",
            "LittlelemonAPI.tests.CartAPITestCase",
            "LittlelemonAPI.tests.OrderAPITestCase",
            "LittlelemonAPI.tests.CategoryAPITestCase"
        ])
        description = "Running API endpoint tests"
    elif "--auth" in args:
        base_cmd.extend([
            "LittlelemonAPI.tests.AuthenticationAPITestCase",
            "LittlelemonAPI.tests.CustomAuthenticationTestCase"
        ])
        description = "Running authentication tests"
    elif "--permissions" in args:
        base_cmd.append("LittlelemonAPI.tests.PermissionTestCase")
        description = "Running permission tests"
    elif "--serializers" in args:
        base_cmd.append("LittlelemonAPI.tests.SerializerTestCase")
        description = "Running serializer tests"
    else:
        # Run all tests
        base_cmd.append("LittlelemonAPI.tests")
        description = "Running all tests"
    
    # Add verbosity
    if verbose:
        base_cmd.extend(["--verbosity", "2"])
    
    # Run with coverage if requested
    if coverage:
        coverage_cmd = [
            "coverage", "run", "--source=.", str(manage_py), "test"
        ] + base_cmd[3:]  # Remove "python3 manage.py test" from base_cmd
        
        if not run_command(coverage_cmd, f"{description} with coverage"):
            sys.exit(1)
        
        # Generate coverage report
        print("\nGenerating coverage report...")
        subprocess.run(["coverage", "report"])
        subprocess.run(["coverage", "html"])
        print("HTML coverage report generated in htmlcov/")
    else:
        if not run_command(base_cmd, description):
            sys.exit(1)
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)
    
    main()