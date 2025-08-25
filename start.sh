#!/bin/sh
# This script is used to start the ADK web server for agents
# It sets the environment variables and runs the adk command    
python /app/mcp/server.py > /dev/null &
adk web /app/adk-app --host 0.0.0.0 --port 8080 