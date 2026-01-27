#!/bin/bash
# =============================================================================
# GTM Agent - Azure App Service Startup Script
# =============================================================================
# This script is executed by Azure App Service to start the application.
# Works with Oryx build which extracts to a temp directory.
#
# Supports GitHub Copilot SDK with optional BYOK (Azure OpenAI) mode:
# - Installs Copilot CLI if COPILOT_CLI_URL is set
# - Starts CLI in server mode for the SDK to connect
# =============================================================================

set -e

echo "=========================================="
echo "GTM Agent - Starting Application"
echo "=========================================="

# Oryx extracts the app to a temp directory and sets APP_PATH
# The virtual environment is at ${APP_PATH}/antenv
if [ -n "$APP_PATH" ]; then
    APP_DIR="$APP_PATH"
else
    APP_DIR="/home/site/wwwroot"
fi

echo "Application directory: $APP_DIR"

# Add the app directory to PYTHONPATH so 'src' module can be found
export PYTHONPATH="${APP_DIR}:${PYTHONPATH}"
echo "PYTHONPATH: $PYTHONPATH"

# Activate virtual environment if it exists (created by Oryx)
if [ -d "${APP_DIR}/antenv/bin" ]; then
    echo "Activating virtual environment..."
    source "${APP_DIR}/antenv/bin/activate"
fi

# Change to app directory
cd "$APP_DIR"

# =============================================================================
# GitHub Copilot CLI Setup (for Copilot SDK)
# =============================================================================
# Only install and start the CLI if COPILOT_CLI_URL is configured
# This enables the Copilot SDK to connect to the CLI server

if [ -n "$COPILOT_CLI_URL" ]; then
    echo "=========================================="
    echo "Setting up GitHub Copilot CLI..."
    echo "=========================================="
    
    # Check if Node.js is available
    if command -v node &> /dev/null; then
        echo "Node.js version: $(node --version)"
        
        # Install Copilot CLI globally if not present
        if ! command -v copilot &> /dev/null; then
            echo "Installing GitHub Copilot CLI..."
            npm install -g @github/copilot
        else
            echo "Copilot CLI already installed: $(copilot --version 2>/dev/null || echo 'unknown')"
        fi
        
        # Extract port from COPILOT_CLI_URL (e.g., "localhost:4321" -> "4321")
        COPILOT_PORT="${COPILOT_CLI_URL##*:}"
        if [ -z "$COPILOT_PORT" ] || [ "$COPILOT_PORT" = "$COPILOT_CLI_URL" ]; then
            COPILOT_PORT="4321"  # Default port
        fi
        
        echo "Starting Copilot CLI server on port $COPILOT_PORT..."
        
        # Start Copilot CLI in server mode (background process)
        copilot --server --port "$COPILOT_PORT" &
        COPILOT_PID=$!
        echo "Copilot CLI started with PID: $COPILOT_PID"
        
        # Wait for CLI server to be ready
        echo "Waiting for Copilot CLI to be ready..."
        for i in {1..30}; do
            if nc -z localhost "$COPILOT_PORT" 2>/dev/null; then
                echo "Copilot CLI is ready!"
                break
            fi
            sleep 1
        done
        
        # Update COPILOT_CLI_URL to ensure it points to localhost
        export COPILOT_CLI_URL="localhost:$COPILOT_PORT"
        echo "COPILOT_CLI_URL set to: $COPILOT_CLI_URL"
    else
        echo "WARNING: Node.js not available, skipping Copilot CLI setup"
        echo "The Copilot SDK code tool will not be available"
    fi
fi

# =============================================================================
# Start the Application
# =============================================================================
echo "=========================================="
echo "Starting Gunicorn server..."
echo "=========================================="

# Use app:app (the root app.py file) which handles PYTHONPATH setup
# This ensures 'src' module can be imported correctly on Azure
exec gunicorn app:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --capture-output
