test:
	poetry run pytest

lint:
	poetry run isort server tests
	poetry run ruff format $(find . -path "*/migrations/*.py")
	poetry run ruff check server tests --fix --output-format=text
	poetry run djlint --reformat server
	# poetry run flake8 server tests
	# poetry run refurb server tests
	poetry run mypy server tests
