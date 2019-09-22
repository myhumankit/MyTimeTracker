.PHONY: install
install:
	python3 -m virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt
	venv/bin/python manage.py makemigrations
	venv/bin/python manage.py migrate
	venv/bin/python manage.py createsuperuser
	mkdir -p site_media/media
	mkdir -p site_media/static
	venv/bin/python manage.py collectstatic


.PHONY: serve
serve:
	venv/bin/python manage.py runserver

.PHONY: clear
clear:
	rm -f db.sqlite3
	rm -rf venv
	rm -rf site_media
	find . -path "*/migrations/*.py" -not -path "./venv*" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -not -path "./venv*" -delete
	find . -path "*.pyc" -not -path "./venv*" -delete
	find . -path "*/__pycache__" -not -path "./venv*" -delete

.PHONY: generate_secret_key
generate_secret_key:
	venv/bin/python utils/secret_key.py
