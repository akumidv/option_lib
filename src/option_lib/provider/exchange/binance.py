"""
Binance api provider
"""
import pandas as pd

from option_lib.provider import DataEngine, RequestParameters
from option_lib.provider.exchange import AbstractExchange
from option_lib.provider.exchange.exchange_entities import ExchangeCode


class BinanceExchange(AbstractExchange):
    """Binance exchange api"""

    def __init__(self, engine: DataEngine = DataEngine.PANDAS):
        """"""
        super().__init__(ExchangeCode.BINANCE.value)

    def load_option(self, symbol: str, params: RequestParameters | None = None) -> pd.DataFrame:
        if params is None:
            params = RequestParameters()
        elif params.columns is None:
            params.columns = self.option_columns
        raise NotImplemented

    def load_future(self, symbol: str, params: RequestParameters | None = None) -> pd.DataFrame:
        if params is None:
            params = RequestParameters()
        elif params.columns is None:
            params.columns = self.future_columns
        raise NotImplemented