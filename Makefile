run:
	go run src/cmd/main.go

lint:
	go fmt ./src/...
	poetry run flake8 tests