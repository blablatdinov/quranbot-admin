run:
	uvicorn main:app --reload --app-dir src --port 8010

lint:
	isort src && flake8 src

test:
	pytest --ignore=src/tests/integration/

cov:
	pytest --cov=src
