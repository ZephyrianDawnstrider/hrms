# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Set default environment variables for build
ENV SECRET_KEY=build-secret-key-will-be-overridden
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate --noinput

# Expose port
EXPOSE 10000

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 hrms.wsgi:application
