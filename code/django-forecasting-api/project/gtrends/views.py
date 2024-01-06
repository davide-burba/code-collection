from django.db import transaction
from gtrends import models, serializers
from gtrends.services.pipelines import inference_pipeline, train_pipeline
from gtrends.services.tasks import update_timeseries
from pytrends.exceptions import ResponseError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TimeSeriesViewSet(viewsets.ModelViewSet):
    queryset = models.TimeSeries.objects.prefetch_related("tsversion_set").all()
    serializer_class = serializers.TimeSeriesSerializer
    http_method_names = ["get", "post", "head", "delete"]

    @action(detail=True, url_path="latest-values")
    def latest_values(self, request, pk):
        """Get timeseries values for the last version."""
        versions = self.queryset.get(pk=pk).tsversion_set.order_by("created_at")
        if not versions:
            return Response([])
        return Response(versions.first().tsvalue_set.values("time", "value"))

    @action(detail=True, url_path="update-values")
    @transaction.atomic
    def update_values(self, request, pk):
        """Update timeseries values."""
        timeseries = self.queryset.get(pk=pk)
        try:
            new_version, how_many = update_timeseries(timeseries)
        except ResponseError:
            return Response(
                "Data download failed!", status=status.HTTP_400_BAD_REQUEST
            )
        msg = f"Data updated, {how_many} new values. "
        if new_version:
            msg += " New version created."
        else:
            msg += " Updated latest version."

        return Response(msg)

    @action(detail=False, url_path="update-all-values")
    @transaction.atomic
    def update_all_values(self, request):
        """Update timeseries values."""
        try:
            for timeseries in self.queryset:
                update_timeseries(timeseries)
        except ResponseError:
            return Response(
                "Data download failed!", status=status.HTTP_400_BAD_REQUEST
            )
        msg = f"Data updated, {len(self.queryset)} timeseries updated."
        return Response(msg)


class TSVersionViewSet(viewsets.ModelViewSet):
    queryset = models.TSVersion.objects.prefetch_related("tsvalue_set").all()
    serializer_class = serializers.TSVersionSerializer
    http_method_names = ["get", "head"]

    @action(detail=True)
    def values(self, request, pk, **kwargs):
        """Get timeseries values."""
        values = self.queryset.get(pk=pk).tsvalue_set.values("time", "value")
        return Response(values)


class MLConfigViewSet(viewsets.ModelViewSet):
    queryset = models.MLConfig.objects.all()
    serializer_class = serializers.MLConfigSerializer
    http_method_names = ["get", "post", "head", "delete"]


class DataConfigViewSet(viewsets.ModelViewSet):
    queryset = models.DataConfig.objects.all()
    serializer_class = serializers.DataConfigSerializer
    http_method_names = ["get", "post", "head", "delete"]


class PreprocessingConfigViewSet(viewsets.ModelViewSet):
    queryset = models.PreprocessingConfig.objects.all()
    serializer_class = serializers.PreprocessingConfigSerializer
    http_method_names = ["get", "post", "head", "delete"]


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = (
        models.MLModel.objects.select_related("preprocess_config", "ml_config")
        .prefetch_related(
            "data_config__targets",
            "data_config__features",
            "mlmodelversion_set",
        )
        .all()
    )
    serializer_class = serializers.MLModelSerializer
    http_method_names = ["get", "post", "head", "delete"]

    @action(detail=True)
    def train(self, request, pk, **kwargs):
        ml_model = self.queryset.get(pk=pk)

        ml_model_version = train_pipeline(ml_model)

        return Response(
            serializers.MLModelVersionSerializer(ml_model_version).data
        )

    @action(detail=True)
    def predict(self, request, pk, **kwargs):
        ml_model = self.queryset.get(pk=pk)
        if ml_model.mlmodelversion_set.count() == 0:
            return Response(
                "No model has been trained yet!",
                status=status.HTTP_404_NOT_FOUND,
            )

        predictions = inference_pipeline(ml_model)

        return Response(predictions)


class MLModelVersionViewSet(viewsets.ModelViewSet):
    queryset = models.MLModelVersion.objects.all()
    serializer_class = serializers.MLModelVersionSerializer
    http_method_names = ["get", "head"]
