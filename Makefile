SHELL=/bin/bash

runserver:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

gunicorn:
	gunicorn --bind 0.0.0.0:8000 -w 4 meditka.wsgi
