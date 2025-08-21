#!/bin/bash

# CLI Hub Demo Script
# This script demonstrates the key features of CLI Hub

echo "🎯 CLI Hub Demo"
echo "==============="

# Get the Python path for the virtual environment
PYTHON_PATH="/Users/vymn/developement/scripts/meta-work/.venv/bin/python"
HUB_CMD="$PYTHON_PATH cli_hub.py"

echo
echo "1. First, let's check the hub status:"
$HUB_CMD status

echo
echo "2. Let's add some example scripts:"
$HUB_CMD add counter "$PYTHON_PATH examples.py counter" --description "A simple counter script"
$HUB_CMD add logger "$PYTHON_PATH examples.py logger" --description "Random log generator"  
$HUB_CMD add server "$PYTHON_PATH examples.py server" --description "Simulated server"

echo
echo "3. List all registered scripts:"
$HUB_CMD list

echo
echo "4. Let's run the counter in the background:"
$HUB_CMD run counter --background

echo
echo "5. And the logger too:"
$HUB_CMD run logger --background

echo
echo "6. Check running processes:"
$HUB_CMD ps

echo
echo "7. Let's see some output from the counter (waiting 5 seconds first):"
sleep 5
$HUB_CMD logs counter --lines 10

echo
echo "8. And output from the logger:"
$HUB_CMD logs logger --lines 5

echo
echo "9. Let's run a direct command:"
$HUB_CMD exec "echo 'Hello from direct execution!'"

echo
echo "10. Stop the background processes:"
$HUB_CMD stop counter
$HUB_CMD stop logger

echo
echo "11. Final status:"
$HUB_CMD status

echo
echo "12. Clean up stopped processes:"
$HUB_CMD cleanup

echo
echo "🎉 Demo completed!"
echo "You can now use 'hub' command after running setup.py"
