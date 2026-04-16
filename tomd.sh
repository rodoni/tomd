#!/usr/bin/env bash
# Wraps the local python virtual environment to easily run the CLI
# Usage: ./tomd.sh <command> <arguments>

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtual environment
source "$DIR/venv/bin/activate"

# Execute the actual tomd command, passing along any arguments
exec tomd "$@"
