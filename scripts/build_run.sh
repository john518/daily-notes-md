#!/bin/bash
set -e # Exit immediately if any command fails

# Get the project root directory (one level up from the script)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Build the client
npm --prefix client run build

# Run the python script
PYTHONPATH=. python -u scripts/main.py
