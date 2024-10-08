run:
	poetry run python manage.py runserver

test:
	poetry run pytest

lint:
	poetry run isort server tests
	poetry run ruff format $(find . -path "*/migrations/*.py")
	poetry run ruff check server tests --fix --output-format=concise
	poetry run djlint --reformat server
	poetry run djlint --lint server
	# poetry run flake8 server tests
	# poetry run refurb server tests
	poetry run mypy server tests
	poetry run yamllint -d '{"extends": "default", "ignore": [".venv", ".github"], "rules": {"line-length": {"max": 120}}}' -s .
	DJANGO_ENV=production DJANGO_COLLECTSTATIC_DRYRUN=1 poetry run python manage.py collectstatic --no-input --dry-run
