from lightgbm import LGBMRegressor


def train(x, y, model_params):
    model = LGBMRegressor(**model_params)
    model.fit(x, y)
    return model
