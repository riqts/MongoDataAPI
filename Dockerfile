# Stage 1: Build stage
FROM python:3.9-slim as requirements-stage

# Set working directory for requirements installation
WORKDIR /tmp

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.9-slim as production-stage

# Create application directory and add non-root user for security
RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/app
ENV APP_HOME=/home/app/code
WORKDIR $APP_HOME

# Copy installed dependencies from build stage to production stage
COPY --from=requirements-stage /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=requirements-stage /usr/local/bin /usr/local/bin

# Copy application code to container
COPY . .

# Expose the application port
EXPOSE 5000

# Healthcheck to monitor container health (install curl if not included)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
HEALTHCHECK --interval=30s CMD curl --fail http://localhost:5000/health || exit 1

# Run the application with a single ASGI worker using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
