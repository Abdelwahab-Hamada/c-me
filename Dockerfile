# Use a slim Python image for efficiency
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies (replace with your actual requirements)
COPY /app/requirements.txt .
RUN pip install -r requirements.txt

# Copy your Django project code
COPY /app/ .

# Run migrations and collect static files (adjust commands if needed)
RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput