FROM golang:1.21.4-alpine AS build

WORKDIR /src
COPY src go.mod /src
RUN GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o /bin/server /src/cmd/server/main.go

FROM scratch
COPY --from=build /bin/server /bin/server
ENTRYPOINT ["/bin/server"]