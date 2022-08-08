run:
	uvicorn main:app --reload --app-dir src --port 8010

lint:
	isort src && flake8 src

test:
	pytest src --ignore=src/tests/integration/

cov:
	pytest src --cov=src
