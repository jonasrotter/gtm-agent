"""
Azure App Service Entry Point

This module sets up the Python path correctly for Azure App Service
where Oryx extracts the app to a temp directory.
"""

import os
import sys

# Find the directory containing this file (app.py)
# This works regardless of where Oryx extracts the app
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to Python path so 'src' module can be found
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"App directory: {current_dir}")
print(f"Python path: {sys.path}")
print(f"Directory contents: {os.listdir(current_dir)}")

# Now we can import the FastAPI app
from src.api import app

# Export for gunicorn
application = app

