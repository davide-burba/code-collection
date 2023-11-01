package stats

import (
	"math"
	"sync"
	"time"
)

// Interface for a data point in a time series
type TsValue interface {
	GetTime() time.Time
	GetValue() float64
}

func ComputeStatistics(values []TsValue) map[string]float64 {
	result := make(map[string]float64)

	result["Count"] = Count(values)
	result["Min"] = Min(values)
	result["Max"] = Max(values)
	result["Mean"] = Mean(values)
	result["StdDev"] = StandardDeviation(values)

	return result
}

func ComputeStatisticsConcurrent(values []TsValue) map[string]float64 {
	result := make(map[string]float64)

	var wg sync.WaitGroup
	ch := make(chan struct {
		string
		float64
	})

	statsToCompute := map[string]func([]TsValue) float64{
		"Count":             Count,
		"Min":               Min,
		"Max":               Max,
		"Mean":              Mean,
		"StandardDeviation": StandardDeviation,
	}

	wg.Add(len(statsToCompute))
	for statName, statFunc := range statsToCompute {
		go func(name string, operation func([]TsValue) float64) {
			defer wg.Done()
			value := operation(values)
			ch <- struct {
				string
				float64
			}{name, value}
		}(statName, statFunc)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	for stat := range ch {
		result[stat.string] = stat.float64
	}

	return result
}

func Count(values []TsValue) float64 {
	return float64(len(values))
}

func Min(values []TsValue) float64 {
	if len(values) == 0 {
		return math.NaN()
	}
	min := values[0].GetValue()
	for _, value := range values {
		if value.GetValue() < min {
			min = value.GetValue()
		}
	}
	return min
}

func Max(values []TsValue) float64 {
	if len(values) == 0 {
		return math.NaN()
	}
	max := values[0].GetValue()
	for _, value := range values {
		if value.GetValue() > max {
			max = value.GetValue()
		}
	}
	return max
}

func Mean(values []TsValue) float64 {
	count := Count(values)
	if count == 0 {
		return math.NaN()
	}
	sum := Sum(values)
	return sum / count
}

func StandardDeviation(values []TsValue) float64 {
	count := Count(values)
	if count == 0 {
		return math.NaN()
	}
	mean := Mean(values)
	sumSquare := 0.0
	for _, value := range values {
		sumSquare += math.Pow(value.GetValue()-mean, 2)
	}
	return math.Sqrt(sumSquare / count)
}

func Sum(values []TsValue) float64 {
	if len(values) == 0 {
		return math.NaN()
	}
	sum := 0.0
	for _, value := range values {
		sum += value.GetValue()
	}
	return sum
}
