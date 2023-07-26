from typing import Dict, List

import pandas as pd
from gtrends.models import TimeSeries


def load_data(
    target_ts: List[TimeSeries], feature_ts: List[TimeSeries]
) -> Dict[str, Dict[str, pd.DataFrame]]:
    targ_feat = {
        "targets": target_ts,
        "features": feature_ts,
    }
    data = {"targets": {}, "features": {}}
    metadata = {"targets": {}, "features": {}}
    for key, items in targ_feat.items():
        for item in items:
            ts = item.timeseries
            version = ts.tsversion_set.last()
            values = version.tsvalue_set.all().values("time", "value")
            df = pd.DataFrame(values)
            df["ts_name"] = ts.name
            df = df.set_index(["time", "ts_name"])
            data[key][ts.name] = df
            metadata[key][ts.name] = version.id
    return data, metadata
