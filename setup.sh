#!/usr/bin/env bash

echo "Setting up the tomd environment..."

# 1. Create virtual environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate

# 3. Install the application in editable mode
pip install -e .

echo "---------------------------------------------------------"
echo "Environment setup complete!"
echo ""
echo "To run the application, you can now:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Run the wrapper directly: ./tomd.sh convert <file>"
echo "---------------------------------------------------------"
