package models

import "time"

type TimeSeries struct {
	ID   int    `gorm:"primaryKey"`
	Name string `gorm:"not null"`
}

type TimeSeriesValue struct {
	ID           int `gorm:"primaryKey"`
	Time         time.Time
	Value        float64
	TimeSeriesID int `gorm:"not null"`
}

func (v TimeSeriesValue) GetTime() time.Time { return v.Time }
func (v TimeSeriesValue) GetValue() float64  { return v.Value }
