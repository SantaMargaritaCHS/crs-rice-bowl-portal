"""
Application entry point for the CRS Rice Bowl application.
"""
import os
import sys

# Startup logging for Railway debugging
print(f"[STARTUP] Python version: {sys.version}", flush=True)
print(f"[STARTUP] PORT env: {os.environ.get('PORT', 'not set')}", flush=True)
print(f"[STARTUP] Working dir: {os.getcwd()}", flush=True)

from app import create_app

print("[STARTUP] Creating Flask app...", flush=True)
app = create_app()
print("[STARTUP] Flask app created successfully!", flush=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[STARTUP] Starting development server on port {port}", flush=True)
    app.run(debug=True, host='0.0.0.0', port=port)
