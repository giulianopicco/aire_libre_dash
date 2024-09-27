.PHONY: runserver
runserver:
	python manage.py runserver

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: superuser
superuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('max', 'admin@example.com', 'password'); user.set_password('asdf'); user.save()" | python manage.py shell

.PHONY: setup
setup: migrations migrate superuser

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: shell
shell:
	python manage.py shell -i ipython

.PHONY: venv
venv:
	python -m venv .env && source .env/bin/activate && pip install -r requirements.txt

.PHONY: requirements
requirements:
	pip install -r requirements.txt

.PHONY: start
start: requirements migrate superuser runserver