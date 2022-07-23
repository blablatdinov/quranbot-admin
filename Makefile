run:
# 	uvicorn main:app --reload --app-dir src
	python src/main.py

lint:
	isort src && flake8 src

test:
	pytest -m 'not slow'

cov:
	pytest -m 'not slow' --cov=src
