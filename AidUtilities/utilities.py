#!/usr/bin/env python

import pandas as pd


def clean_col_names(df, old_char=[' '], new_char=['_']):
    '''Replace dataframe col names by removing specified characters.
    Will replace the year columns with just the numeric year.
    Args:
        df(pandas.DataFrame)
        old_char(list): characters to replace. Default is " "(a space).
        new_char(list): new characters to replace. Default is "_".
    Returns:
        pandas.DataFrame with new cleaned column names.'''
    new_col_names = []
    for col in df.columns:
        # Filter Year Columns
        if 'YR' in col:
            # dump [YR...] part of col name
            year, _ = col.split(' ')
            new_col_names.append(year)
        else:
            for old, new in zip(old_char, new_char):
                new_col_names.append(col.replace(old, new))
    df.columns = new_col_names
    return df