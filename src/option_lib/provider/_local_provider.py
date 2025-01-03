"""
Local provider
Data should be organized like EXCHANGE_CODE/EXCHANGE_SYMBOL/TRADE_TYPE/TIMEFRAME_CODE/YEAR.parquet
Example: LME/WTI/option/EOD/2024.year
TRADE_TYPE can be: option, future, asset (asset - mean tangible assets: currency, stock, crypto)

dataframe columns:
"""

import os
import builtins
import datetime
import pandas as pd
from pydantic import validate_call
from option_lib.provider import AbstractProvider
from option_lib.entities import TimeframeCode, InstrumentType
from option_lib.provider import RequestParameters


class PandasLocalFileProvider(AbstractProvider):
    """Load data from files"""

    def __init__(self, exchange_code: str, data_path: str):
        exchange_data_path = os.path.normpath(os.path.abspath(os.path.join(data_path, exchange_code)))
        if not os.path.isdir(exchange_data_path):
            raise FileNotFoundError(f'Folder {exchange_data_path} is not exist')
        self.exchange_data_path = exchange_data_path
        super().__init__(exchange_code=exchange_code)

    def _fn_path_prepare(self, symbol: str, instrument_type: InstrumentType, timeframe: TimeframeCode, year: int):
        return f'{self.exchange_data_path}/{symbol}/{instrument_type.value}/{timeframe.value}/{year}.parquet'

    def _load_data_for_period(self, instrument_type: InstrumentType, symbol: str,
                              params: RequestParameters, columns: list) -> pd.DataFrame:
        if params.period_from is None:
            match type(params.period_to):
                case None:
                    """Load all data"""
                    raise NotImplemented
                case builtins.int:
                    fn_path = self._fn_path_prepare(symbol, instrument_type, params.timeframe, params.period_to)
                    return pd.read_parquet(fn_path, columns=columns)
                case datetime.date:
                    fn_path = self._fn_path_prepare(symbol, instrument_type, params.timeframe, params.period_to.year)
                    df_opt = pd.read_parquet(fn_path, columns=columns)
                    return df_opt[df_opt['datetime'] == params.period_to].reset_index(True)
                case datetime.datetime:
                    raise NotImplemented
                case _:
                    raise TypeError(f'period_to have incorrect type {type(params.period_to)}')
        else:
            match type(params.period_from):
                case builtins.int:
                    if params.period_to is None:
                        """load from period_from to last year"""
                        raise NotImplemented
                    elif isinstance(params.period_to, int):
                        """Load from year to year"""
                        raise NotImplemented
                    else:
                        raise TypeError(f'Mismatch types period_from {type(params.period_from)} '
                                        f'and period_to {type(params.period_to)}')
                case datetime.date:
                    if params.period_to is None:
                        """load from period_from to last year"""
                        raise NotImplemented
                    elif isinstance(params.period_to, datetime.date):
                        """Load from date to date"""
                        raise NotImplemented
                    else:
                        raise TypeError(f'period_to have incorrect type {type(params.period_to)}')
                case datetime.datetime:
                    raise NotImplemented
                case _:
                    raise TypeError(f'period_to have incorrect type {type(params.period_to)}')

    @validate_call
    def load_option_history(self, symbol: str, params: RequestParameters | None = None,
                            columns: list | None = None) -> pd.DataFrame:
        """Load option by period, timeframe"""
        if params is None:
            params = RequestParameters()
        if columns is None:
            columns = self.option_columns
        df_opt = self._load_data_for_period(instrument_type=InstrumentType.OPTION, symbol=symbol,
                                            params=params, columns=columns)
        return df_opt

    @validate_call
    def load_future_history(self, symbol: str, params: RequestParameters | None = None,
                            columns: list | None = None) -> pd.DataFrame:
        if params is None:
            params = RequestParameters()
        if columns is None:
            columns = self.future_columns
        df_fut = self._load_data_for_period(instrument_type=InstrumentType.FUTURE, symbol=symbol,
                                            params=params, columns=columns)
        return df_fut
