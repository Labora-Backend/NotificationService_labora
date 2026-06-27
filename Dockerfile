FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/labora \
    JWT_PUBLIC_KEY_PATH=/app/jwt_keys/public.pem \
    DJANGO_SERVICE=notificationservice

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser

COPY labora_shared /opt/labora/labora_shared

COPY NotificationService_labora/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY NotificationService_labora/ /app/

RUN if [ -f /app/entrypoint-asgi.sh ]; then mv /app/entrypoint-asgi.sh /app/entrypoint.sh; fi && \
    chmod +x /app/entrypoint.sh && \
    mkdir -p /app/jwt_keys && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
