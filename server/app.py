"""
OpenEnv Server Application
Provides HTTP API for the hiring environment
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from openenv_core import create_app
from env.hiring_env import HiringEnv

# Create FastAPI app with OpenEnv integration
app = create_app(HiringEnv)


def main():
    """Entry point for server mode"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
