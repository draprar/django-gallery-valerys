# Use the official Python image as a base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app

# Collect static files (only for production builds)
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Default command to run Gunicorn
CMD ["gunicorn", "base.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
