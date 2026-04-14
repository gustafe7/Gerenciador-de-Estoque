#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists() or User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '', '${DJANGO_SUPERUSER_PASSWORD}')" | python manage.py shell