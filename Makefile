run:
	uvicorn main:app --reload --app-dir src

lint:
	isort src && flake8 src

test:
	pytest --ignore=src/tests/integration/

cov:
	pytest --cov=src
