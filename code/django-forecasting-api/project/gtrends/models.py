from django.db import models
from django.db.models import CASCADE, PROTECT


class DataSource(models.TextChoices):
    GOOGLE_TRENDS = "GOOGLE_TRENDS"


class TimeSeries(models.Model):
    name = models.CharField(unique=True, max_length=64)
    source = models.CharField(max_length=32, choices=DataSource.choices)


class TSVersion(models.Model):
    timeseries = models.ForeignKey(TimeSeries, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)


class TSValue(models.Model):
    version = models.ForeignKey(TSVersion, on_delete=CASCADE)
    time = models.DateTimeField()
    value = models.FloatField()


class MLConfig(models.Model):
    params = models.JSONField()


class DataConfig(models.Model):
    name = models.CharField(unique=True, max_length=64)


class DataFeatures(models.Model):
    config = models.ForeignKey(
        DataConfig, on_delete=CASCADE, related_name="features"
    )
    timeseries = models.ForeignKey(TimeSeries, on_delete=PROTECT)


class DataTargets(models.Model):
    config = models.ForeignKey(
        DataConfig, on_delete=CASCADE, related_name="targets"
    )
    timeseries = models.ForeignKey(TimeSeries, on_delete=PROTECT)


class PreprocessingConfig(models.Model):
    name = models.CharField(unique=True, max_length=64)
    params = models.JSONField()


class MLModel(models.Model):
    name = models.CharField(unique=True, max_length=64)
    ml_config = models.ForeignKey(MLConfig, on_delete=PROTECT)
    data_config = models.ForeignKey(DataConfig, on_delete=PROTECT)
    preprocess_config = models.ForeignKey(
        PreprocessingConfig, on_delete=PROTECT
    )


class MLModelVersion(models.Model):
    ml_model = models.ForeignKey(MLModel, on_delete=CASCADE)
    ml_file = models.FileField(upload_to="ml_models")
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField()
