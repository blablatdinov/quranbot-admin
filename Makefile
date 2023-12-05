run:
	go run src/cmd/server/main.go

lint:
	go fmt ./src/...
	poetry run flake8 tests