# Stage 1: Build the application
FROM python:3.9-slim-buster AS builder

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Production image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Copy the installed dependencies from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the dependencies from the wheels
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY ./app/ /app/

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}