# 1. Use an official lightweight Python image.
# 'slim' versions are smaller and more secure for production.
FROM python:3.9-slim

# 2. Set the working directory inside the container.
WORKDIR /app

# 3. Copy your local code into the container's /app folder.
# This is where your main.py gets moved into the image.
COPY . .

# 4. Install the libraries required by your main.py.
# We install gunicorn as the production-grade web server.
RUN pip install --no-cache-dir \
    Flask \
    google-cloud-storage \
    google-cloud-pubsub \
    google-cloud-bigquery \
    redis \
    gunicorn

# 5. Run the web service on container startup.
# Cloud Run injects a $PORT environment variable; Gunicorn listens on it.
# --workers 1 --threads 8 handles concurrency.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
