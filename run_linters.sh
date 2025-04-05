#!/bin/bash
# Simple script to run all linters from CI workflow locally
# Usage: ./run_linters.sh [--fix]
#   --fix    Apply fixes automatically when possible (black, isort)

# Exit on first error
set -e

# Check if we should fix issues or just check
FIX_MODE=false
if [ "$1" == "--fix" ]; then
    FIX_MODE=true
    echo "Running linters in FIX mode..."
else
    echo "Running linters in CHECK mode (use --fix to auto-format)..."
fi

# Check/fix formatting with black
echo "Running black..."
if [ "$FIX_MODE" = true ]; then
    black kybra_simple_logging tests
else
    black --check kybra_simple_logging tests
fi

# Check/fix imports with isort
echo "Running isort..."
if [ "$FIX_MODE" = true ]; then
    isort kybra_simple_logging tests
else
    isort --check-only kybra_simple_logging tests
fi

# Lint with flake8 (no auto-fix available)
echo "Running flake8..."
flake8 kybra_simple_logging --ignore=E501,W391,W503,F405,F403,F401,E722,F811
flake8 tests/src --ignore=E501,W391,W503,F405,F403,F401,E722

# Type check with mypy (no auto-fix available)
echo "Running mypy..."
mypy kybra_simple_logging tests

echo "All linters completed successfully!"
