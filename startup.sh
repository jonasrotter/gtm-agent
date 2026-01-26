#!/bin/bash
# =============================================================================
# GTM Agent - Azure App Service Startup Script
# =============================================================================
# This script is executed by Azure App Service to start the application.
# Works with Oryx build which extracts to a temp directory.
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

# Start the application with Gunicorn + Uvicorn workers
echo "Starting Gunicorn server..."
exec gunicorn src.api:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --capture-output
