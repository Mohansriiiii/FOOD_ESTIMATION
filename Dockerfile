# Use a smaller base with security/size benefits
FROM python:3.10-slim

# Prevent .pyc and enable immediate logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps often needed by Pillow / OpenCV / some wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer cache
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app sources (after pip for cache benefit)
COPY . /app

# Create non-root user (recommended)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Streamlit config for container
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false

EXPOSE 8501

# Start Streamlit and bind to 0.0.0.0
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
