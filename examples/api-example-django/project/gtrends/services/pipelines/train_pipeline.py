from gtrends.models import MLModel, MLModelVersion
from gtrends.services.tasks import (
    load_data,
    preprocess,
    save_mlmodelversion,
    train,
)


def train_pipeline(ml_model: MLModel) -> MLModelVersion:
    target_ts = ml_model.data_config.targets.all()
    feature_ts = ml_model.data_config.features.all()
    prep_params = ml_model.preprocess_config.params
    model_params = ml_model.ml_config.params

    data, metadata = load_data(target_ts, feature_ts)
    x, y = preprocess(data, prep_params)
    engine = train(x, y, model_params)
    ml_model_version = save_mlmodelversion(engine, ml_model, metadata)

    return ml_model_version
