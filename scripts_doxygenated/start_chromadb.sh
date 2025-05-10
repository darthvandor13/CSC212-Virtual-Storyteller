## @file start_chromadb_server.sh
# @brief Starts the ChromaDB server, assuming the correct Python virtual environment is ALREADY ACTIVE.
# @details
#   This script performs the following actions:
#   1. Defines configurable paths and server parameters for ChromaDB.
#   2. CRITICAL: Verifies that the 'chroma' command-line tool is available on the PATH.
#      It assumes this command is provided by a Python virtual environment that has
#      been activated BEFORE this script is executed.
#   3. Starts the ChromaDB server using the 'chroma run' command.
#   The server is configured with:
#     - Persistent storage path: '~/chroma_db' (specific to the user running the script).
#     - Host: '0.0.0.0' (listens on all available network interfaces, allowing remote connections).
#     - Port: '8000'.
#
# @usage
#   1. IMPORTANT: Activate the Python virtual environment that contains the 'chromadb'
#      package BEFORE running this script.
#      Example:
#        source ~/chromadb_env/bin/activate
#   2. Make this script executable: chmod +x start_chromadb_server.sh
#   3. Run the script from within the activated environment: ./start_chromadb_server.sh
#   The server will run in the foreground. Press Ctrl+C to stop it.
#
# @Calvin Vandor
# @date 2025-05-10

#!/bin/bash

# --- Configuration ---
# Path for ChromaDB persistent storage (within the current user's home directory)
# This allows multiple users on a system to have their own ChromaDB instances.
CHROMA_DB_PATH="$HOME/chroma_db"

# Host IP to listen on (0.0.0.0 makes it accessible from other machines)
HOST_IP="0.0.0.0"

# Port to listen on
PORT_NUM="8000"

# --- Script Logic ---

echo "------------------------------------"
echo " ChromaDB Server Startup Script "
echo " (Assuming Python venv is active) "
echo "------------------------------------"

# 1. Verify the 'chroma' command is available
#    This is a crucial check to ensure the pre-activated environment is correct.
if ! command -v chroma &> /dev/null; then
    echo "❌ Error: 'chroma' command not found in the current PATH."
    echo "   Please ensure you have activated the correct Python virtual environment"
    echo "   that has the 'chromadb' package installed."
    exit 1
fi
echo "✅ 'chroma' command is available from the current environment."

# 2. Start the ChromaDB server
echo "⏳ Starting ChromaDB server with the following settings:"
echo "   Persistent Storage Path: $CHROMA_DB_PATH"
echo "   Host IP: $HOST_IP"
  echo "   Port: $PORT_NUM"
echo "   (To stop the server, press Ctrl+C)"
echo "------------------------------------"

# The 'chroma run' command is the standard way to start the server
chroma run --path "$CHROMA_DB_PATH" --host "$HOST_IP" --port "$PORT_NUM"
