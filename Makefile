install:
	poetry install
lint:
	poetry run flake8 task_manager/users
	poetry run flake8 task_manager/labels
	poetry run flake8 task_manager/statuses
	poetry run flake8 task_manager/tasks
run:
	python3 manage.py runserver
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
console:
	python3 manage.py shell
test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml
test:
	poetry run python3 manage.py test