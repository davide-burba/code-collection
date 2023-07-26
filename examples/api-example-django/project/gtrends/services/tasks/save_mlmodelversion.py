import os
from typing import Dict
from uuid import uuid4

from django.core.files import File
from gtrends import models
from gtrends.services.ml import save_engine
from lightgbm import LGBMRegressor


def save_mlmodelversion(
    engine: LGBMRegressor, ml_model: models.MLModel, metadata: Dict
) -> models.MLModelVersion:
    filename = str(uuid4()).replace("-", "")[:10] + ".txt"
    tmp_path = "/tmp/" + filename
    save_engine(engine, tmp_path)
    with open(tmp_path, "r") as f:
        ml_model_file = File(f, filename)
        ml_model_version = models.MLModelVersion(
            ml_model=ml_model,
            ml_file=ml_model_file,
            metadata=metadata,
        )
        ml_model_version.save()
    os.remove(tmp_path)
    return ml_model_version
