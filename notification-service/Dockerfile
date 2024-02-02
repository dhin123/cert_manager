# Use an official Python runtime as a parent image
FROM python:3.8.1-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY notification-service /app/notification-service
COPY notification-service/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY common_packages /app/common_packages
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/common_packages"
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl
# Make port 8001 available to the world outside this container
EXPOSE 8001

# Create a shell script to run multiple commands
RUN echo -e '#!/bin/sh\npython notification-service/notification_app.py &\ncd notification-service && celery -A tasks worker --loglevel=INFO' > /app/run.sh
RUN chmod +x /app/run.sh

# Run the shell script when the container launches
CMD ["/bin/sh", "/app/run.sh"]