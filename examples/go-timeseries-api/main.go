package main

import (
	"github.com/gin-gonic/gin"

	"tsapi/database"
	"tsapi/handlers"
)

func main() {

	// set database
	db, err := database.GetDatabase("timeseries.db")
	if err != nil {
		panic("failed to connect database")
	}
	database.AutoMigrate(db)

	// set endpoints
	router := gin.Default()
	router.SetTrustedProxies([]string{"127.0.0.1"})
	handlers.SetEndpoints(router, db)
	router.Run(":8080")

}
