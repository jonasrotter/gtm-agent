"""
Gunicorn configuration for GTM Agent on Azure App Service.

This configuration is optimized for:
- FastAPI with async support (Uvicorn workers)
- MCP server with streaming responses
- Azure App Service environment
"""

import multiprocessing
import os
import sys

# =============================================================================
# PYTHONPATH Setup for Azure App Service
# =============================================================================
# Azure App Service (Oryx) extracts the app to a temp directory.
# We need to ensure the app directory is in PYTHONPATH before importing modules.
_app_dir = os.path.dirname(os.path.abspath(__file__))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

# =============================================================================
# Server Socket
# =============================================================================

# Bind to all interfaces on port 8000 (Azure App Service default)
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# =============================================================================
# Worker Processes
# =============================================================================

# Worker class - Use Uvicorn for async support
worker_class = "uvicorn.workers.UvicornWorker"

# Number of worker processes
# For App Service B1 (1 core): 2 workers
# For App Service P1V3 (2 cores): 4 workers
# Formula: 2 * CPU cores + 1 (but capped for memory constraints)
workers = int(os.getenv("GUNICORN_WORKERS", min(multiprocessing.cpu_count() * 2 + 1, 4)))

# Number of threads per worker (not used with UvicornWorker)
threads = 1

# =============================================================================
# Worker Timeout
# =============================================================================

# Timeout for worker processes (seconds)
# Set high for MCP tool calls that may take time
timeout = int(os.getenv("GUNICORN_TIMEOUT", 300))

# Graceful timeout for worker restart
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 30))

# Keep-alive timeout
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 65))

# =============================================================================
# Server Mechanics
# =============================================================================

# Daemonize the Gunicorn process (set to False for Azure App Service)
daemon = False

# PID file location
pidfile = None

# Umask for file creation
umask = 0

# User and group (not used in App Service)
user = None
group = None

# Temporary directory for request body
tmp_upload_dir = None

# =============================================================================
# Logging
# =============================================================================

# Access log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Log to stdout/stderr (captured by App Service)
accesslog = "-"
errorlog = "-"

# Log level
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# Capture output from stdout/stderr in workers
capture_output = True

# =============================================================================
# Process Naming
# =============================================================================

proc_name = "gtm-agent"

# =============================================================================
# Server Hooks
# =============================================================================

def on_starting(server):
    """Called just before the master process is initialized."""
    print("GTM Agent: Gunicorn master starting...")


def on_reload(server):
    """Called before reloading workers."""
    print("GTM Agent: Reloading workers...")


def worker_int(worker):
    """Called when a worker receives SIGINT or SIGQUIT."""
    print(f"GTM Agent: Worker {worker.pid} interrupted")


def worker_abort(worker):
    """Called when a worker receives SIGABRT."""
    print(f"GTM Agent: Worker {worker.pid} aborted")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    print(f"GTM Agent: Worker {worker.pid} spawned")


def post_worker_init(worker):
    """Called just after a worker has initialized."""
    print(f"GTM Agent: Worker {worker.pid} initialized")


def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    print(f"GTM Agent: Worker {worker.pid} exited")


def nworkers_changed(server, new_value, old_value):
    """Called when the number of workers changes."""
    print(f"GTM Agent: Worker count changed from {old_value} to {new_value}")


def on_exit(server):
    """Called just before exiting Gunicorn."""
    print("GTM Agent: Gunicorn shutting down...")
