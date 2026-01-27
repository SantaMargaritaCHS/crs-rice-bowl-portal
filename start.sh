#!/bin/sh
# Startup script for Railway deployment
# Handles PORT environment variable properly

PORT="${PORT:-5000}"
echo "[STARTUP] Starting gunicorn on port $PORT"
exec gunicorn --preload --bind "0.0.0.0:$PORT" --workers 2 --threads 4 --timeout 120 run:app
