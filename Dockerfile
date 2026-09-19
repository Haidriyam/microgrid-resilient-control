FROM python:3.11-slim

WORKDIR /app

# Ensure security updates are applied
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Non-root user execution
USER 10001
CMD ["python", "-m", "src.resilient_consensus"]