from typing import Dict, Tuple

import pandas as pd
from gtrends.services.preprocessing import Preprocessor


def preprocess(data: Dict, prep_params: Dict) -> Tuple[pd.DataFrame, pd.Series]:
    return Preprocessor(**prep_params).build_x_y(data)


def build_x_latest(data: Dict, prep_params: Dict) -> pd.DataFrame:
    return Preprocessor(**prep_params).build_x_latest(data)
