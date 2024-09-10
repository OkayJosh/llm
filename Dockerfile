FROM ubuntu:latest
LABEL authors="Joshua Olatunji"

# Use the official Python image as a base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE llm.settings

# Set the working directory in the container
WORKDIR /llm

# Copy the current directory contents into the container at /bookflow
COPY . /llm

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt


# Set executable permissions for entrypoint.sh
RUN chmod +x docker/entrypoint.sh

RUN chmod +x docker/reach_database.sh

## Set the entry point
#ENTRYPOINT ["/llm/entrypoint.sh"]