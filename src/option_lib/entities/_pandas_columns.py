"""Pandas columns code, value and types"""
import enum
import datetime
from option_lib.entities.enum_code import EnumColumnType
from option_lib.entities._option_types import OptionPriceStatus


@enum.unique
class OptionColumns(EnumColumnType):
    """
    Pandas option column name, type
    """
    # NAME, value, code, type
    # Base mandatory columns from provider
    DATETIME = 'datetime', datetime.date
    STRIKE = 'strike', float
    EXPIRATION_DATE = 'expiration_date', datetime.date
    TYPE = 'option_type', str  # OptionType
    PRICE = 'price', float
    UNDERLYING_EXPIRATION_DATE = 'underlying_expiration_date', datetime.date

    # Extra columns for options (joined for example)
    SYMBOL = 'symbol', str
    EXCHANGE_SYMBOL = 'exchange_symbol', str
    EXCHANGE_UNDERLYING_SYMBOL = 'exchange_underlying_symbol', str
    KIND = 'kind', str  # AssetKind

    # Added by enrichment
    # Future columns
    # FUTURES_PRICE = 'Futures Price', 'futures_price', float
    UNDERLYING_PRICE = 'underlying_price', float

    # Money columns
    INTRINSIC_VALUE = 'intrinsic_value', float
    TIME_VALUE = 'time_value', float
    PRICE_STATUS = 'price_status', OptionPriceStatus

    # Pricer

    # Greeks


@enum.unique
class FuturesColumns(EnumColumnType):
    """
    Pandas option column name, type
    """
    # NAME, value, code, type
    # Base mandatory columns
    DATETIME = OptionColumns.DATETIME.nm, OptionColumns.DATETIME.type
    EXPIRATION_DATE = OptionColumns.EXPIRATION_DATE.nm,  OptionColumns.EXPIRATION_DATE.type
    PRICE = OptionColumns.PRICE.nm, OptionColumns.PRICE.type

    # Extra columns for futures
    SYMBOL = OptionColumns.SYMBOL.nm, OptionColumns.SYMBOL.type
    KIND = OptionColumns.KIND.nm, OptionColumns.KIND.type
    EXCHANGE_ASSET_SYMBOL = OptionColumns.EXCHANGE_SYMBOL.nm, OptionColumns.EXCHANGE_SYMBOL.type


@enum.unique
class SpotColumns(EnumColumnType):
    """
    Pandas option column name, type
    """
    # NAME, value, code, type
    # Base mandatory columns
    DATETIME = OptionColumns.DATETIME.nm, OptionColumns.DATETIME.type
    PRICE = OptionColumns.PRICE.nm, OptionColumns.PRICE.type

    # Extra columns for futures
    SYMBOL = OptionColumns.SYMBOL.nm, OptionColumns.SYMBOL.type
    KIND = OptionColumns.KIND.nm, OptionColumns.KIND.type
    EXCHANGE_ASSET_SYMBOL = OptionColumns.EXCHANGE_SYMBOL.nm, OptionColumns.EXCHANGE_SYMBOL.type


OPTION_NON_FUTURES_COLUMN_NAMES = [col.nm for col in OptionColumns if col.nm not in [f_col.nm for f_col in FuturesColumns]]
OPTION_NON_SPOT_COLUMN_NAMES = [col.nm for col in OptionColumns if col.nm not in [s_col.nm for s_col in SpotColumns]]
