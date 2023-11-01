package handlers

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

// Create a new type that embeds database.Database to be able to assign new
// methods to it
type wrapDB struct {
	DB *gorm.DB
}

func SetEndpoints(r *gin.Engine, db *gorm.DB) {

	wrapdb := &wrapDB{DB: db}

	// timeseries CRUD
	r.GET("/timeseries", wrapdb.listTimeSeries)
	r.GET("/timeseries/:tsid", wrapdb.getTimeSeries)
	r.POST("/timeseries", wrapdb.postTimeSeries)
	r.PUT("/timeseries/:tsid", wrapdb.putTimeSeries)
	r.DELETE("/timeseries/:tsid", wrapdb.deleteTimeSeries)

	// timeseries values CRUD
	r.GET("/timeseries/:tsid/values", wrapdb.listTimeSeriesValues)
	r.GET("/timeseries/:tsid/values/:valueid", wrapdb.getTimeSeriesValue)
	r.POST("/timeseries/:tsid/values", wrapdb.postTimeSeriesValues)
	r.PUT("/timeseries/:tsid/values/:valueid", wrapdb.putTimeSeriesValue)
	r.DELETE("/timeseries/:tsid/values/:valueid", wrapdb.deleteTimeSeriesValue)

	// statistics
	r.GET("/timeseries/:tsid/statistics", wrapdb.getTimeSeriesStats)
}
