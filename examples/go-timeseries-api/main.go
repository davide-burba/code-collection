package main

import (
	"flag"
	"fmt"

	"github.com/gin-gonic/gin"

	"tsapi/database"
	"tsapi/handlers"
)

func main() {

	// Define flags for command-line arguments
	dbName := flag.String("db", "timeseries.db", "Database name")
	trustedProxy := flag.String("proxy", "127.0.0.1", "Trusted proxy")
	port := flag.String("port", "8080", "Port number")
	flag.Parse()

	// Initialize the database
	db, err := database.GetDatabase(*dbName)
	if err != nil {
		panic("failed to connect to the database")
	}
	database.AutoMigrate(db)

	// Set the trusted proxies
	router := gin.Default()
	router.SetTrustedProxies([]string{*trustedProxy})

	// Set endpoints and run the server
	handlers.SetEndpoints(router, db)
	router.Run(fmt.Sprintf(":%s", *port))

}
