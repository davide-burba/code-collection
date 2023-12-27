from gtrends import models
from gtrends.services.tasks import update_timeseries
from lightgbm import LGBMRegressor
from rest_framework import serializers


class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeSeries
        fields = "__all__"

    def create(self, validated_data):
        ts = super().create(validated_data)
        # Download data for the newly created timeseries.
        update_timeseries(ts)
        return ts


class TSVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TSVersion
        fields = "__all__"


class MLConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MLConfig
        fields = "__all__"

    def validate_params(self, value):
        # At the moment we only support LightGBM model.
        valid_params = LGBMRegressor().get_params()
        invalid_params = [k for k in value if k not in valid_params]
        if invalid_params:
            raise serializers.ValidationError(f"Invalid: {invalid_params}")
        return value


class DataFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataFeatures
        fields = ("timeseries",)


class DataTargetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataTargets
        fields = ("timeseries",)


class DataConfigSerializer(serializers.ModelSerializer):
    features = DataFeaturesSerializer(many=True)
    targets = DataTargetsSerializer(many=True, allow_null=False)

    class Meta:
        model = models.DataConfig
        fields = ("id", "name", "features", "targets")

    def validate_targets(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Must have at least one target.")
        return value

    def create(self, validated_data):
        features_data = validated_data.pop("features")
        targets_data = validated_data.pop("targets")
        config = models.DataConfig.objects.create(**validated_data)

        new_feats = []
        for feature_data in features_data:
            obj = models.DataFeatures(config=config, **feature_data)
            new_feats.append(obj)
        models.DataFeatures.objects.bulk_create(new_feats)

        new_targs = []
        for target_data in targets_data:
            obj = models.DataTargets(config=config, **target_data)
            new_targs.append(obj)
        models.DataTargets.objects.bulk_create(new_targs)

        return config


class PreprocessingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PreprocessingConfig
        fields = "__all__"

    def validate_params(self, value):
        expected_keys = {"horizon", "target_lags", "feature_lags"}
        if set(value.keys()) != expected_keys:
            raise serializers.ValidationError(f"Expected keys: {expected_keys}")

        if not isinstance(value["horizon"], int):
            raise serializers.ValidationError("Horizon must be an int.")

        for key in ["target_lags", "feature_lags"]:
            if not isinstance(value[key], list) or not all(
                isinstance(lag, int) for lag in value[key]
            ):
                raise serializers.ValidationError(f"{key} must be a list[int].")

        return value


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MLModel
        fields = "__all__"


class MLModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MLModelVersion
        fields = "__all__"
