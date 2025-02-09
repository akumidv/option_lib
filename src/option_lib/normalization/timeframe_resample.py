"""Timeframe conversion"""
import pandas as pd
from option_lib.entities import OptionColumns as OCl, Timeframe

DEFAULT_RESAMPLE_MODEL = {col: col.resample_func for col in OCl if col.resample_func is not None}
RESAMPLE_SORT_COLUMNS = [OCl.TIMESTAMP.nm, OCl.ORIGINAL_TIMESTAMP, OCl.REQUEST_TIMESTAMP]


def convert_to_timeframe(df: pd.DataFrame, timeframe: Timeframe, by_exchange_symbol: bool = True,
                         resample_model: dict[str, str] | None = None):
    """Convert to upper timeframe"""
    if resample_model is None:
        resample_model = DEFAULT_RESAMPLE_MODEL
    columns = list(set([OCl.TIMESTAMP.nm] + [col for col in resample_model if col in df.columns]))
    sort_columns = [col for col in RESAMPLE_SORT_COLUMNS if col in columns]
    df = df[columns].sort_values(by=sort_columns)
    resample_model = {col: action for col, action in resample_model.items() if col in columns}
    df = _resample_by_kind_type_or_exchange_symbol(df,
                                                   timeframe=timeframe,
                                                   by_exchange_symbol=by_exchange_symbol,
                                                   resample_model=resample_model,
                                                   group_columns=None)
    return df


def _get_group_columns_by_type(df: pd.DataFrame):
    """Prepare list of columns by dataframe content"""
    is_spot = OCl.EXPIRATION_DATE.nm not in df.columns or df[OCl.EXPIRATION_DATE.nm].isnull().all()
    is_future = not is_spot and df[OCl.EXPIRATION_DATE.nm].notnull().all() and \
                (OCl.STRIKE.nm not in df.columns or df[OCl.STRIKE.nm].isnull().all())
    is_option = not is_future and OCl.STRIKE.nm in df.columns and OCl.OPTION_TYPE.nm in df.columns and \
                df[[OCl.STRIKE.nm, OCl.OPTION_TYPE.nm]].notnull().all().all()
    if is_spot:
        group_columns = []
    elif is_future:  # Futures
        group_columns = [OCl.EXPIRATION_DATE.nm]
    elif is_option:  # Options
        group_columns = [OCl.EXPIRATION_DATE.nm, OCl.OPTION_TYPE, OCl.STRIKE.nm]
    else:
        raise ValueError(f'Cannot detect type of dataframe by columns and values, '
                         f'try to use {OCl.EXCHANGE_SYMBOL.nm}')
    if OCl.SYMBOL.nm in df.columns and len(df[OCl.SYMBOL.nm].unique()) > 1:
        group_columns = [OCl.SYMBOL.nm] + group_columns
    return group_columns


def _resample_by_kind_type_or_exchange_symbol(df: pd.DataFrame, timeframe: Timeframe, resample_model: dict[str, str],
                                              by_exchange_symbol: bool = True,
                                              group_columns: list[str] | None = None) -> pd.DataFrame:
    """Resample by detection type of asset by column"""
    if group_columns is None:
        if by_exchange_symbol:
            # exchange symbol is uniq for each of futures or option contract and should be single for spot
            group_columns = [OCl.EXCHANGE_SYMBOL.nm]
        else:
            group_columns = _get_group_columns_by_type(df)
        return _resample_by_kind_type_or_exchange_symbol(df,
                                                         timeframe=timeframe,
                                                         resample_model=resample_model,
                                                         group_columns=group_columns,
                                                         by_exchange_symbol=by_exchange_symbol)

    if len(group_columns) > 0:
        group = df.groupby(group_columns[0], group_keys=False)
        return group.apply(_resample_by_kind_type_or_exchange_symbol,
                           timeframe=timeframe,
                           by_exchange_symbol=by_exchange_symbol,
                           group_columns=group_columns[1:],
                           resample_model=resample_model)
    if OCl.EXCHANGE_SYMBOL.nm in df.columns and len(df[OCl.EXCHANGE_SYMBOL.nm].unique()) != 1:
        raise ValueError(f'Resampled dataframe contain more then one '
                         f'exchange symbol {df[OCl.EXCHANGE_SYMBOL.nm].unique()}')

    ffill_columns = [col for col in resample_model if resample_model[col] == 'last' and col in df.columns]
    if len(ffill_columns):
        df[ffill_columns].ffill(inplace=True)
    bfill_columns = [col for col in resample_model if resample_model[col] == 'first' and col in df.columns]
    if len(bfill_columns):
        df[bfill_columns].bfill(inplace=True)
    df_resample = df.resample(rule=timeframe.offset, on=OCl.TIMESTAMP.nm, closed='left', label='left').apply(
        resample_model)
    return df_resample
