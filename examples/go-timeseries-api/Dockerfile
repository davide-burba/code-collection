FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build
EXPOSE 8080
CMD ["./tsapi"]
