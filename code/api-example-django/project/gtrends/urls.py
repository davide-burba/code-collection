from django.urls import include, path
from gtrends import views
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()
router.register("model-config", views.MLConfigViewSet)
router.register("data-config", views.DataConfigViewSet)
router.register("preprocessing-config", views.PreprocessingConfigViewSet)
models = router.register("model", views.MLModelViewSet)
models.register(
    "versions",
    views.MLModelVersionViewSet,
    basename="version",
    parents_query_lookups="model_id",
)

timeseries = router.register("timeseries", views.TimeSeriesViewSet)
timeseries.register(
    "versions",
    views.TSVersionViewSet,
    basename="version",
    parents_query_lookups="timeseries_id",
)

urlpatterns = [
    path("", include(router.urls)),
]
