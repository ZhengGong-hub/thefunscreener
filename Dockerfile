FROM python:3.12

WORKDIR /thefunscreener

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv directly and update PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Verify uv is installed correctly
RUN uv --version

# Copy pyproject.toml and uv.lock for dependency management
COPY pyproject.toml uv.lock README.md ./

# Copy the application code
COPY app/ ./app/

# Expose API port
EXPOSE 8033