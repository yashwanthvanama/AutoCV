#!/bin/bash
# Script to start the FastAPI backend server

cd "$(dirname "$0")"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
