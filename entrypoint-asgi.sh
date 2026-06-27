#!/bin/sh
set -e

echo "Waiting for MySQL..."
until nc -z ${DB_HOST:-mysql} ${DB_PORT:-3306}; do
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Daphne (ASGI)..."
exec daphne -b 0.0.0.0 -p 8000 ${DJANGO_SERVICE}.asgi:application
