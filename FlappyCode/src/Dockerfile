# Build Stage
FROM python:3.12-slim AS builder

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory and copy dependencies
WORKDIR /app
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Final Stage
FROM python:3.12-slim

# Create a non-root user for security
RUN groupadd -r floopyuser && useradd -r -g floopyuser floopyuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ACCEPT_EULA=Y \
    PATH="/opt/venv/bin:$PATH"

# Set the KEY_VAULT_NAME environment variable for runtime (so app.py can access it)
ENV KEY_VAULT_NAME=${KEY_VAULT_NAME} 

# Install runtime dependencies and ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY /odbc.ini /
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini
# Copy virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set working directory and copy the app files
WORKDIR /app
COPY . .

# Expose the port for the app
EXPOSE 3000

# Set ownership and switch to non-root user
RUN chown -R floopyuser:floopyuser /opt/venv /app
USER floopyuser

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "3", "app:app"]
