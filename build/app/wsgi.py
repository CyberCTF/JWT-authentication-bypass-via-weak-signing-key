#!/usr/bin/env python3
"""
WSGI configuration for JWT Authentication Bypass lab
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Import Flask application
from app import app

application = app

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=False)