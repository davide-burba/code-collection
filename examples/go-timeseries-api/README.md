# A time series API in GO

In this example we showcase the implementation of a REST API in GO to perform CRUD operations on timeseries, and compute a set of statistics.

We use [Gin](https://gin-gonic.com/) as Web Framework, and [Gorm](https://gorm.io/index.html) as ORM.


## Quickstart

You can run the API either with Docker or with Go.

**With Docker:**
```bash
# Build the docker image
docker build -t go-timeseries-api .
# Run the docker image
docker run -p 8080:8080 go-timeseries-api
```

**With Go:**

```bash
# Compile the Go program
go build
# Execute the Go binary
./tsapi
```

Or, in one step:
```bash
# Compile in memory and execute
go run main.go
```

## Usage Example

```bash
# Create a time series
curl -i -X POST http://localhost:8080/timeseries -d '{ "Name": "My time series"}'
> {"ID":1,"Name":"My time series"}

# Create time series values
curl -i -X POST http://localhost:8080/timeseries/1/values -d '[{"Time": "2023-10-28T12:00:00Z", "Value": 10.0},{"Time": "2023-10-28T12:15:00Z", "Value": 20.5}]'
> {"message":"Time series values created"}

# Get statistics
curl -i -GET http://localhost:8080/timeseries/1/statistics
> {"Count":2,"Max":20.5,"Mean":15.25,"Min":10,"StandardDeviation":5.25}

# Delete a time series
curl -i -X DELETE http://localhost:8080/timeseries/1
> {"id #1":"deleted"}
```

## Endpoints

This application defines the following endpoints for managing time series data.

### Time Series Endpoints
- `GET /timeseries`: List all time series.
- `GET /timeseries/:tsid`: Get details of a specific time series.
- `POST /timeseries`: Create a new time series.
- `PUT /timeseries/:tsid`: Update an existing time series.
- `DELETE /timeseries/:tsid`: Delete a time series and its values.

### Time Series Values Endpoints
- `GET /timeseries/:tsid/values`: List all values of a time series.
- `GET /timeseries/:tsid/values/:valueid`: Get details of a specific time series value.
- `POST /timeseries/:tsid/values`: Add new values to a time series.
- `PUT /timeseries/:tsid/values/:valueid`: Update a time series value.
- `DELETE /timeseries/:tsid/values/:valueid`: Delete a time series value.

### Statistics Endpoints
- `GET /timeseries/:tsid/statistics`: Generate statistics for a time series.

