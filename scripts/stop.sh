#!/bin/bash

echo "Stopping Worker..."
pkill -f "saq app.core.worker.settings_dict"

echo "Stopping Server..."
pkill -f "uvicorn app.main:app"

echo "Stopping Redis..."
docker-compose stop redis

echo "All stopped."
