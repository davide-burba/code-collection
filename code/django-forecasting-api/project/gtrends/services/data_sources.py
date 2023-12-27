import datetime as dt
from abc import ABC, abstractmethod

import pandas as pd
from gtrends.models import TimeSeries
from pytrends.request import TrendReq


def download_data(timeseries: TimeSeries) -> pd.DataFrame:
    return DATASOURCE_MAP[timeseries.source](timeseries).download()


class DataSource(ABC):
    def __init__(self, timeseries: TimeSeries):
        self.timeseries = timeseries

    @abstractmethod
    def download(self) -> pd.DataFrame:
        """Returns a dataframe with time as index and value as column."""


class GTrendSource(DataSource):
    START_DATE = "2022-01-01"

    def download(self) -> pd.DataFrame:
        # Download data.
        name = self.timeseries.name
        data = self.download_interest_over_time(name)
        # Format new data.
        data = (
            data[~data.isPartial]
            .reset_index()
            .rename(columns={name: "value", "date": "time"})
            .set_index("time")
        )[["value"]]
        data["value"] = data["value"].astype(float)
        return data

    @classmethod
    def download_interest_over_time(cls, search_term: str) -> pd.DataFrame:
        """Download Google Trends data."""
        pytrends = TrendReq()
        timeframe = (
            cls.START_DATE + " " + dt.datetime.now().strftime("%Y-%m-%d")
        )
        pytrends.build_payload([search_term], timeframe=timeframe)
        return pytrends.interest_over_time()


DATASOURCE_MAP = {
    "GOOGLE_TRENDS": GTrendSource,
}
