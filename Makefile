install:
	poetry install
lint:
	poetry run flake8 task_manager tests
run:
	python3 manage.py runserver
mig:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
console:
	python3 manage.py shell
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
test:
	python3 manage.py test