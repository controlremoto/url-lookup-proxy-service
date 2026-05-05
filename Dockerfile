# Dockerfile for URL Lookup Service (multi-stage build)

# --- Builder stage ---
FROM python:3.11-slim AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Final image ---
FROM python:3.11-slim
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"
COPY --from=builder /root/.local /root/.local
COPY ./src ./src
COPY requirements.txt ./
EXPOSE 8000
CMD ["uvicorn", "src.api.urlinfo:app", "--host", "0.0.0.0", "--port", "8000"]
