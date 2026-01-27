# CRS Rice Bowl Portal - Flask Application
# Single container for Railway deployment

FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY public/ ./public/
COPY run.py .
COPY start.sh .

# Create data directory for SQLite and make script executable
RUN mkdir -p /app/data && chmod +x /app/start.sh

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000

# Run startup script
CMD ["/app/start.sh"]
