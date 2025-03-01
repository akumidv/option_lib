""""Public price analytic api class that should hide realization of functions"""
import datetime
import pandas as pd

from option_lib.option_data_class import OptionData
from option_lib.entities import OptionType
from option_lib.analytic.price._time_values import (
    time_value_series_by_strike_to_atm_distance, time_value_series_by_atm_distance
)
from option_lib.enrichment import OptionEnrichment


class OptionAnalyticPrice:
    """
    Wrapper about price analytics modules functions
    """

    def __init__(self, data: OptionData):
        self._data = data
        self._enrichment: OptionEnrichment = OptionEnrichment(self._data)

    def time_value_series_by_strike_to_atm_distance(self, strike: float | None = None,
                                                    expiration_date: pd.Timestamp | None = None,
                                                    option_type: OptionType | None = OptionType.CALL) -> pd.DataFrame:
        """Get time value series by strike to atm distance"""
        self._enrichment.add_intrinsic_and_time_value()
        return time_value_series_by_strike_to_atm_distance(self._data.df_hist, strike, expiration_date, option_type)

    def time_value_series_by_atm_distance(self, distance: float | None = None,
                                          expiration_date: pd.Timestamp | None = None,
                                          option_type: OptionType | None = OptionType.CALL) -> pd.DataFrame:
        """Get time value series by distance from atm"""
        self._enrichment.add_intrinsic_and_time_value()
        return time_value_series_by_atm_distance(self._data.df_hist, distance, expiration_date, option_type)
