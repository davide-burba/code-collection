package handlers

import (
	"strconv"
	"tsapi/models"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func (db *wrapDB) listTimeSeries(c *gin.Context) {
	var tseriesList []models.TimeSeries
	if err := db.DB.Find(&tseriesList).Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to retrieve timeseries"})
		return
	}
	c.JSON(200, tseriesList)
}

func (db *wrapDB) getTimeSeries(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	var tseries models.TimeSeries
	if err := db.DB.Where("id = ?", timeSeriesID).First(&tseries).Error; err != nil {
		c.JSON(404, gin.H{"error": "Failed to retrieve timeseries"})
		return
	}
	c.JSON(200, tseries)
}

func (db *wrapDB) postTimeSeries(c *gin.Context) {
	var tseries models.TimeSeries
	c.BindJSON(&tseries)
	if err := db.DB.Create(&tseries).Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to create timeseries"})
		return
	}
	c.JSON(201, tseries)
}

func (db *wrapDB) putTimeSeries(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	var tseries models.TimeSeries
	if err = db.DB.Where("id = ?", timeSeriesID).First(&tseries).Error; err != nil {
		c.JSON(404, gin.H{"error": "Time series not found"})
		return
	}
	c.BindJSON(&tseries)
	if err = db.DB.Save(&tseries).Error; err != nil {
		c.JSON(500, gin.H{"error": "Error while saving"})
	}
	c.JSON(200, tseries)
}

// Delete a timeseries and its values
func (db *wrapDB) deleteTimeSeries(c *gin.Context) {
	timeSeriesID, err := db.checkTimeSeriesID(c)
	if err != nil {
		return
	}
	var tseries models.TimeSeries
	db.DB.Transaction(func(tx *gorm.DB) error {

		// Delete values
		if err := tx.Where("time_series_id = ?", timeSeriesID).
			Delete(&models.TimeSeriesValue{}).Error; err != nil {
			c.JSON(500, gin.H{"error": "Deleting the timeseries failed."})
			return err
		}

		// Delete timeseries
		if err := tx.Where("id = ?", timeSeriesID).
			Delete(&tseries).Error; err != nil {
			c.JSON(500, gin.H{"error": "Deleting the timeseries failed."})
			return err
		}

		c.JSON(200, gin.H{"id #" + strconv.Itoa(timeSeriesID): "deleted"})
		return nil
	})

}

func (db *wrapDB) checkTimeSeriesID(c *gin.Context) (int, error) {
	id := c.Param("tsid")
	// Check if the time series exists can be converted to
	timeSeriesID, err := strconv.Atoi(id)
	if err != nil {
		c.JSON(400, gin.H{"error": "Invalid time series ID"})
		return timeSeriesID, err
	}

	// Check if the time series exists in the TimeSeries table
	var timeSeries models.TimeSeries
	if err := db.DB.First(&timeSeries, timeSeriesID).Error; err != nil {
		c.JSON(404, gin.H{"error": "Time series not found"})
		return timeSeriesID, err
	}
	return timeSeriesID, nil
}
