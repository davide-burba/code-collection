package handlers

import (
	"math"
	"tsapi/models"
	"tsapi/stats"

	"github.com/gin-gonic/gin"
)

func (db *wrapDB) getTimeSeriesStats(c *gin.Context) {

	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}

	// Query the database.Database to retrieve specific fields of time series values
	var tsValues []models.TimeSeriesValue

	if err := db.DB.Where("time_series_id = ?", timeSeriesID).
		Select("id, time, value").Find(&tsValues).Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to retrieve time series values"})
		return
	}

	// Convert the slice of TimeSeriesValue to a slice of TsValue interfaces
	values := []stats.TsValue{}
	for _, v := range tsValues {
		values = append(values, v)
	}
	c.JSON(200, serializeMap(stats.ComputeStatisticsConcurrent(values)))
}

// SerializeMap serializes a map from string to float64,
// returning null for NaN values
func serializeMap(data map[string]float64) map[string]interface{} {
	serializedData := make(map[string]interface{})
	for key, value := range data {
		if math.IsNaN(value) {
			serializedData[key] = nil
		} else {
			serializedData[key] = value
		}
	}
	return serializedData
}
