#!/usr/bin/env python3
"""
Test runner script for AuthFast application.
Provides convenient commands for running different types of tests.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd: list[str], description: str) -> int:
    """Run a command and return the exit code."""
    print(f"\n🧪 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [command]")
        print("\nAvailable commands:")
        print("  all          - Run all tests")
        print("  unit         - Run unit tests only")
        print("  integration  - Run integration tests only")
        print("  coverage     - Run tests with coverage report")
        print("  fast         - Run tests excluding slow tests")
        print("  verbose      - Run tests with verbose output")
        return 1
    
    command = sys.argv[1].lower()
    
    # Set environment variables for testing
    os.environ.setdefault("JWT_SECRET_KEY", "test_secret_key_for_testing")
    os.environ.setdefault("ADMIN_EMAIL", "admin@test.com")
    os.environ.setdefault("ADMIN_USERNAME", "admin")
    os.environ.setdefault("ADMIN_FULL_NAME", "Test Admin")
    os.environ.setdefault("ADMIN_PASSWORD", "testpassword")
    os.environ.setdefault("ADMIN_HASHED_PASSWORD", "hashed_test_password")
    os.environ.setdefault("SENDGRID_API_KEY", "test_sendgrid_key")
    os.environ.setdefault("APPLICATION_HOSTNAME", "http://localhost:5001")
    
    if command == "all":
        return run_command(["python", "-m", "pytest"], "Running all tests")
    
    elif command == "unit":
        return run_command(
            ["python", "-m", "pytest", "-m", "not integration"],
            "Running unit tests only"
        )
    
    elif command == "integration":
        return run_command(
            ["python", "-m", "pytest", "-m", "integration"],
            "Running integration tests only"
        )
    
    elif command == "coverage":
        return run_command(
            ["python", "-m", "pytest", "--cov=app", "--cov-report=html", "--cov-report=term"],
            "Running tests with coverage report"
        )
    
    elif command == "fast":
        return run_command(
            ["python", "-m", "pytest", "-m", "not slow"],
            "Running fast tests (excluding slow tests)"
        )
    
    elif command == "verbose":
        return run_command(
            ["python", "-m", "pytest", "-v", "-s"],
            "Running tests with verbose output"
        )
    
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 