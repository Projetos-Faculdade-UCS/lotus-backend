#!/bin/sh
# wait for db
python3 manage.py makemigrations
python3 manage.py migrate

# create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', '123123')" | python3 manage.py shell

python3 manage.py runserver 0.0.0.0:8000