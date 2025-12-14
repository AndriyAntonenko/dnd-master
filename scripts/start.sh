#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping processes..."
    kill $WORKER_PID
    kill $SERVER_PID
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

echo "Starting Redis..."
docker-compose up -d

echo "Starting Worker..."
uv run python -m saq app.core.worker.settings_dict --web &
WORKER_PID=$!

echo "Starting Server..."
uv run uvicorn app.main:app --reload &
SERVER_PID=$!

echo "Environment is running."
echo "Worker PID: $WORKER_PID"
echo "Server PID: $SERVER_PID"
echo "Press Ctrl+C to stop."

# Wait for processes
wait
