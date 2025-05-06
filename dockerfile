# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (only if needed for other packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (if using)
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

# Copy dependency files first (for caching)
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN poetry install --no-dev --no-root

# Copy the rest of the app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]