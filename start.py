#!/usr/bin/env python3
"""Startup script for Railway deployment."""
import os
import subprocess
import sys

port = os.environ.get('PORT', '5000')
print(f"[STARTUP] Starting gunicorn on port {port}", flush=True)

cmd = [
    'gunicorn',
    '--preload',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '2',
    '--threads', '4',
    '--timeout', '120',
    'run:app'
]

sys.exit(subprocess.call(cmd))
