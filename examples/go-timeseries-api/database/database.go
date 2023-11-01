package database

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"tsapi/models"
)

func GetDatabase(dbFile string) (*gorm.DB, error) {
	return gorm.Open(sqlite.Open(dbFile), &gorm.Config{})
}

func AutoMigrate(db *gorm.DB) {
	db.AutoMigrate(&models.TimeSeries{}, &models.TimeSeriesValue{})
}
