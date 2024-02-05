# Use an official Python runtime as a parent image
FROM python:3.8.1-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY cert-service /app/cert-service
COPY cert-service/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY common_packages /app/common_packages
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/common_packages"
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl
# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run cert_app.py when the container launches
CMD ["python", "cert-service/cert_app.py"]
