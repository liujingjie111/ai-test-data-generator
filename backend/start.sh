#!/bin/bash
set -e

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
