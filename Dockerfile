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

# Optional: Set WORKDIR as an environment variable so it's available in scripts
ENV WORKDIR /llm

# Copy the current directory contents into the container at /llm
COPY . /llm

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for Celery files and set permissions
RUN mkdir -p /var/run/llm && \
    chown -R www-data:www-data /var/run/llm

# Create the staticfiles directory and set the ownership to www-data
RUN mkdir -p /llm/staticfiles && \
    chown -R www-data:www-data /llm/staticfiles

# Set appropriate permissions for the application directory
RUN chown -R www-data:www-data /llm

# Copy .env.example to .env
COPY .env.example .env

# Set executable permissions for entrypoint.sh and reach_database.sh
RUN chmod +x /llm/docker/entrypoint.sh
RUN chmod +x /llm/docker/reach_database.sh

# Switch to non-root user
USER www-data

# Collect static files during the build
RUN python manage.py collectstatic --noinput