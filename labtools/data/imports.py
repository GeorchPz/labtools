# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:05:53 2020

@author: Jorge Pottiez
"""

import pandas as pd

from .path_utils import DATA_DIR, get_file_path

def load_excel(filename, sheet_name=0, extension='.xlsx', directory=None):
    '''
    Read data from Excel file into a pandas DataFrame.
    
    Parameters:
        - filename : str, excel filename (without .xlsx extension)
        - sheet_name : int or str, optional, sheet to read (default: 0, first sheet)
        - directory : str, optional, directory path (default: module's DATA_DIR)
    Returns:
        - pandas.DataFrame, DataFrame containing the Excel data
    '''
    directory = DATA_DIR if directory is None else directory
    file_path = get_file_path(filename, extension=extension, directory=directory)
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {filename} in {directory}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file {filename} is empty")

def load_csv(filename, delimiter=',', extension='.csv', directory=None):
    directory = DATA_DIR if directory is None else directory
    file_path = get_file_path(filename, extension=extension, directory=directory)
    try:
        return pd.read_csv(file_path, delimiter=delimiter)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {filename} in {directory}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file {filename} is empty")