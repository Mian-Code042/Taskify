FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port (Render sets PORT env variable automatically, Gunicorn will read it)
EXPOSE 10000

# Start Gunicorn server
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:create_app()"]
