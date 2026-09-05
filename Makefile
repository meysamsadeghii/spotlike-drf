install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	python manage.py runserver

docker-up:
	docker compose up --build

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser

loaddata:
	docker compose exec web python manage.py loaddata sample_data.json
