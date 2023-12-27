# Stage 1: Build the Go application
FROM golang:1.21-alpine3.18 AS build
WORKDIR /app
COPY . .
RUN apk add build-base
# Download (and cache) all dependencies.
RUN go mod download
# Build the Go app with static linking
RUN go build -ldflags="-w -s" -o tsapi

# Stage 2: Create a minimal image for running the application
FROM alpine:3.18
WORKDIR /app
COPY --from=build /app/tsapi .
EXPOSE 8080
CMD ["./tsapi"]
