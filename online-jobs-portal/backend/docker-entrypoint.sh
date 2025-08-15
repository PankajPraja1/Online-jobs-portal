#!/bin/bash
python manage.py migrate --noinput
# create superuser if env vars exist (optional)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
  User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
  User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi

gunicorn jobs_portal.wsgi:application --bind 0.0.0.0:8000
