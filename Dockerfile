# --- Stage 1: Build Dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered output logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install building tools if native modules require C bindings
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a localized wheelhouse path
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Runtime ---
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ensure Cloud Run port configurations match the engine
ENV PORT=8080

# Copy installed site-packages over from builder layer
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Append pathing to locate execution packages safely
ENV PATH=/root/.local/bin:$PATH

# Copy structural backend components
COPY main.py .
COPY app/ ./app/
COPY templates/ ./templates/

# Explicitly create an output directory for generated standalone pages inside the container
RUN mkdir -p generated_spas

# Cloud Run injects the PORT environment variable dynamically, override run.py with direct uvicorn binding
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
