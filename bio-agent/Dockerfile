# Use Python 3.11 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv for faster dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Set default environment variables (can be overridden)
ENV PORT=5050
ENV HOST=0.0.0.0

# Expose the port
EXPOSE ${PORT}

# Run the server
CMD ["uv", "run", "app.py"]