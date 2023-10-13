run:
	cargo run

lint:
	poetry run isort src
	poetry run flake8 src
	poetry run mypy src

test:
	poetry run pytest src

cov:
	poetry run pytest src --cov=src
