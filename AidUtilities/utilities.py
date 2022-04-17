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


def create_series_names(series_names, return_tuple=False):
    '''Designed to take in World Bank dataframe with multiple series(studies).
    Then ask for user input on what the new series name should be.
    If "quit" is entered as a value, the function exits and returns input values to that point.
    Args:
        series_names(pandas.series): expects a series of world bank series
        return_tuple(bool): 
            if True--returns a list of tuples. 
                the tuples contain (old_series_name, new_series_name)
            if False-- returns a list of strings that correspond to 
                the new name for each series
    Returns:
        List of either string elements of tuples.  The return object is based on return_tuple value.
    '''
    new_series_names = []
    for series in series_names:
        print(series)
        new_name = input('new name: ')
        if new_name == 'quit':
            return print(new_series_names)
        # return a list of tuples. 
        if return_tuple:
            new_series_names.append((old_series, new_name))
        else:
            new_series_names.append(new_name)
    return new_series_names


def print_cols(aList, cols=3):
    '''Enter a list and will print the items in
    an organized column/s.'''
    count = 0
    aList.sort()
    for i in aList:
        print(f'{str(i): <30}\t', end='')
        count += 1
        if count > (cols-1):
            print()
            count = 0
    return None

    