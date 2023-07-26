import lightgbm


def save_engine(model, path):
    model.booster_.save_model(path)


def load_engine(path):
    return lightgbm.Booster(model_file=path)
