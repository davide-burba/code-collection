package handlers

import (
	"strconv"
	"time"
	"tsapi/models"

	"github.com/gin-gonic/gin"
)

type tsIDTimeValue struct {
	ID    int       `json:"id"`
	Time  time.Time `json:"time"`
	Value float64   `json:"value"`
}

func (db *wrapDB) listTimeSeriesValues(c *gin.Context) {

	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}

	// Query the database.Database to retrieve specific fields of time series values
	var timeSeriesValues []tsIDTimeValue

	if err := db.DB.Model(&models.TimeSeriesValue{}).
		Where("time_series_id = ?", timeSeriesID).
		Select("id, time, value").
		Find(&timeSeriesValues).
		Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to retrieve time series values"})
		return
	}

	// Return the selected fields in the response
	c.JSON(200, timeSeriesValues)
}

func (db *wrapDB) getTimeSeriesValue(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	timeSeriesValueID, err := db.checkTimeSeriesValueID(c)
	if err != nil {
		return
	}
	var tseriesValue tsIDTimeValue
	if err := db.DB.Model(&models.TimeSeriesValue{}).
		Where("id = ? AND time_series_id = ?", timeSeriesValueID, timeSeriesID).
		First(&tseriesValue).Error; err != nil {
		c.JSON(500, gin.H{"error": "Getting the timeseries value failed."})
		return
	}
	c.JSON(200, tseriesValue)
}

func (db *wrapDB) postTimeSeriesValues(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}

	// Bind the request body to a slice of TimeSeriesValue
	var timeSeriesValues []models.TimeSeriesValue
	if err := c.ShouldBindJSON(&timeSeriesValues); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request data"})
		return
	}
	// Set the TimeSeriesID for the posted values
	for i := range timeSeriesValues {
		timeSeriesValues[i].TimeSeriesID = timeSeriesID
	}

	// Create the values in the database.Database
	if err := db.DB.Create(&timeSeriesValues).Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to create time series values"})
		return
	}
	c.JSON(201, gin.H{"message": "Time series values created"})
}

func (db *wrapDB) putTimeSeriesValue(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	timeSeriesValueID, err := db.checkTimeSeriesValueID(c)
	if err != nil {
		return
	}
	var tseriesValue models.TimeSeriesValue
	if err := db.DB.Where("id = ? AND time_series_id = ?", timeSeriesValueID, timeSeriesID).
		First(&tseriesValue).Error; err != nil {
		c.JSON(500, gin.H{"error": "Updating the timeseries value failed."})
		return
	}
	c.BindJSON(&tseriesValue)
	if err = db.DB.Save(&tseriesValue).Error; err != nil {
		c.JSON(500, gin.H{"error": "Saving the timeseries value failed."})
		return
	}
	c.JSON(200, tsIDTimeValue{
		ID:    tseriesValue.ID,
		Time:  tseriesValue.Time,
		Value: tseriesValue.Value,
	})
}

func (db *wrapDB) deleteTimeSeriesValue(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	timeSeriesValueID, err := db.checkTimeSeriesValueID(c)
	if err != nil {
		return
	}

	if err := db.DB.Where("id = ?", timeSeriesValueID).Where("time_series_id = ?", timeSeriesID).
		Delete(&models.TimeSeriesValue{}).Error; err != nil {
		c.JSON(200, gin.H{"error": "Failed to delete timeseries value"})
		return
	}
	c.JSON(200, gin.H{"id #" + strconv.Itoa(timeSeriesID): "deleted"})
}

func (db *wrapDB) checkTimeSeriesValueID(c *gin.Context) (int, error) {
	id := c.Param("valueid")
	// Check if the time series exists can be converted to
	timeSeriesValueID, err := strconv.Atoi(id)
	if err != nil {
		c.JSON(400, gin.H{"error": "Invalid time series value ID"})
		return timeSeriesValueID, err
	}

	// Check if the time series exists in the TimeSeries table
	var timeSeriesValue models.TimeSeriesValue
	if err := db.DB.First(&timeSeriesValue, timeSeriesValueID).Error; err != nil {
		c.JSON(404, gin.H{"error": "Time series Values not found"})
		return timeSeriesValueID, err
	}
	return timeSeriesValueID, nil
}
