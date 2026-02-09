# 1. THE FOUNDATION
# Start with a lightweight version of Linux that has Python 3.9 installed.
FROM python:3.9-slim

# 2. THE SETUP
# Create a folder named "app" inside the container to hold our work.
WORKDIR /app

# 3. THE TRANSFER
# Copy everything from our current Cloud Shell folder (.) into the container's folder (/app).
COPY . /app

# 4. THE INSTALLATION
# Read the shopping list and install Flask and Gunicorn inside the container.
RUN pip install --no-cache-dir -r requirements.txt

# 5. THE CONFIGURATION
# Tell the container that the app will listen on port 8080.
ENV PORT 8080

# 6. THE STARTUP COMMAND
# This is what runs when the container wakes up.
# We use 'gunicorn' (the pro server) to serve the 'app' object from 'main.py'.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
