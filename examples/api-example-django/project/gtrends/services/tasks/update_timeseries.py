from typing import Tuple

import pandas as pd
from gtrends.models import TimeSeries, TSValue, TSVersion
from gtrends.services.data_sources import download_data


def update_all_timeseries():
    """Update all timeseries values."""
    for ts in TimeSeries.object.all():
        update_timeseries(ts)


def update_timeseries(timeseries: TimeSeries) -> Tuple[bool, int]:
    """Update timeseries values.

    Either add the new values (if past values are the same) to the latest
    version, or create a new version.

    Args:
        timeseries: A timeseries object.

    Returns:
        A pair with:
            - bool: True if it created a new version, False otherwise
            - int: The number of new values added.
    """
    new_data = download_data(timeseries)

    # Assign version.
    new_version = True
    versions = timeseries.tsversion_set.order_by("created_at")
    if versions:
        version = versions.last()
        old_data = _build_old_data(version)

        if _is_old_data_in_new_data(old_data, new_data):
            # If old values match, just keep the new values.
            new_version = False
            new_data = new_data.loc[~new_data.index.isin(old_data.index)]
        else:
            # Else, set the old version to expired.
            version.expired = True
            version.save()
    if new_version:
        version = TSVersion(timeseries=timeseries)
        version.save()

    # Store new data.
    objs = [
        TSValue(version=version, time=d[0], value=d[1].value)
        for d in new_data.iterrows()
    ]
    TSValue.objects.bulk_create(objs)

    return new_version, len(objs)


def _build_old_data(version: TSVersion) -> pd.DataFrame:
    old_data = pd.DataFrame(
        version.tsvalue_set.values("time", "value")
    ).set_index("time")
    old_data.index = old_data.index.tz_localize(None)
    return old_data


def _is_old_data_in_new_data(
    old_data: pd.DataFrame, new_data: pd.DataFrame
) -> bool:
    if old_data.index.isin(new_data.index).all() and new_data.loc[
        old_data.index
    ].equals(old_data):
        return True
    return False
