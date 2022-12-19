run:
	poetry run uvicorn main:app --reload --app-dir src --port 8010

lint:
	poetry run isort src
	poetry run flake8 src
	poetry run mypy src

test:
	poetry run pytest src --ignore=src/tests/integration/

cov:
	poetry run pytest src --cov=src
