run:
	uvicorn src.main:app

lint:
	isort src && flake8 src

test:
	pytest

cov:
	pytest --cov=src
