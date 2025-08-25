# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY adk-app ./adk-app

COPY mcp ./mcp

COPY start.sh .

RUN chmod +x start.sh

# Expose the port the app runs on (adjust as needed)
EXPOSE 8080

# Command to run the application (adjust as needed)
# CMD ["adk","web", "agents", "--host", "0.0.0.0", "--port", "8080"]
ENTRYPOINT [ "./start.sh" ]
