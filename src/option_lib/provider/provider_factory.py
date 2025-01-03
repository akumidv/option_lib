"""
A Factory function constructs a provider depending on the storage and engine chosen
"""
import enum
from typing import Dict, Type
from functools import partial
from option_lib.provider import AbstractProvider, DataEngine, DataSource
from option_lib.provider import PandasLocalFileProvider
from option_lib.provider.exchange import get_exchange


_PROVIDERS: Dict[DataSource, Dict[DataEngine, Type[AbstractProvider]]] = {
    DataSource.LOCAL: {
        DataEngine.PANDAS: PandasLocalFileProvider,
        DataEngine.POLARIS: AbstractProvider,
        DataEngine.DASK: AbstractProvider,
        DataEngine.SPARK: AbstractProvider

    },
    DataSource.S3: {
        DataEngine.PANDAS: AbstractProvider,
        DataEngine.POLARIS: AbstractProvider,
        DataEngine.DASK: AbstractProvider,
        DataEngine.SPARK: AbstractProvider
    },
    DataSource.API: {
        DataEngine.PANDAS: partial(get_exchange, engine=DataEngine.PANDAS),
        DataEngine.POLARIS: partial(get_exchange, engine=DataEngine.POLARIS),
        DataEngine.DASK: partial(get_exchange, engine=DataEngine.DASK),
        DataEngine.SPARK: partial(get_exchange, engine=DataEngine.SPARK)

    }
}


def get_provider(exchange_code, storage: DataSource = DataSource.LOCAL,
                 engine: DataEngine = DataEngine.PANDAS, **kwargs) -> AbstractProvider:
    """Fabric"""
    return _PROVIDERS[storage][engine](exchange_code=exchange_code, **kwargs)
