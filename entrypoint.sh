#!/bin/sh

if [ "$DATABASE_URL" ]; then
  echo "Aguardando o banco..."
  until nc -z db 5432; do
    sleep 1
  done
fi

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"