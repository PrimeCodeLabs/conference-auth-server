# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY ./alembic/requirements.txt /app/alembic/requirements.txt
RUN pip install --no-cache-dir -r /app/alembic/requirements.txt

# Install Alembic
RUN pip install alembic

# Set the entry point to run Alembic commands
ENTRYPOINT ["alembic"]
