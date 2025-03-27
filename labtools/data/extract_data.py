# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:00:35 2021

@author: Jorge Pottiez López-Jurado
"""

import re

from .imports import load_excel, pd

# NOT IN USE IN THE CURRENT VERSION
def load_experimental_data(x_label, y_label, filename, data_dir=None):
    """
    Load experimental data with uncertainties from file.
    
    Parameters:
        - x_label : str, x-axis label
        - y_label : str, y-axis label
        - filename : str, filename of the data file
        - data_dir : str, optional, directory path (default: module's DATA_DIR)
    Returns:
        - tuple: (x, y, δx, δy), data arrays and their uncertainties
    """
    # Strip math notation if present
    x_magn = x_label.split(' ')[0].replace('$', '')
    y_magn = y_label.split(' ')[0].replace('$', '')
    
    # Import data from file
    df = load_excel(filename, directory=data_dir)
    (x, y), (δx, δy) = get_excel_data_and_uncertainties(f'{x_magn},{y_magn}', df)
    
    return x, y, δx, δy

def get_excel_data_and_uncertainties(variables_str, dataframe):
    '''
    Extracts the data and uncertainty from a dataframe, given a string with the
    variables to extract.
    Returning the data and uncertainty arrays in the order of the variables'
    string.

    Parameters:
        - variables_str: str
            String with the variables to extract from the dataframe
        - dataframe: pd.DataFrame
            DataFrame with the data to extract
    Returns:
        - values_data: list of pd.Series
            List with the data of the variables in the order of the variables'
            string
        - uncertainties_data: list of pd.Series
            List with the uncertainties of the variables in the order of the
            variables' string
    '''
    # Create a copy of the dataframe to avoid modifying the original
    df_copy = dataframe.copy()
    headers = dataframe.columns.values
    uncertainty_dict = {}
    column_mapping = {}
    
    # Extracting the data and uncertainty from the headers
    for header in headers:
        if '(' in header:
            magnitude, uncert = _get_header_data_and_uncert(header)
            uncertainty_dict[magnitude] = uncert
            column_mapping[header] = magnitude
        else:
            # We remove possible spaces from header (for uncert columns)
            magnitude = header.replace(' ', '')
            column_mapping[header] = magnitude
        
    # Create a new dataframe with unique columns
    unique_columns = {}
    for original_col, new_col in column_mapping.items():
        # If this variable name is already assigned, skip duplicates
        if new_col in unique_columns:
            continue
        # Otherwise keep track of the first column for each variable
        unique_columns[new_col] = original_col
    
    # Create a new dataframe with only the columns we need, renamed appropriately
    cleaned_df = pd.DataFrame()
    for new_col, original_col in unique_columns.items():
        cleaned_df[new_col] = dataframe[original_col]
    
    # Handle non-constant uncertainties
    for key in uncertainty_dict:
        if uncertainty_dict[key] == 'not_const' and 'δ' not in key:
            try:
                uncertainty_dict[key] = dataframe['δ' + key]
            except KeyError:
                print(
                    f'The uncertainty column δ{key} was not found',
                    f'Assuming δ{key} = 0'
                )
                uncertainty_dict[key] = 0
    
    # Extract variable data and uncertainties in requested order
    variables_list = variables_str.split(',')
    variables_list = [var.strip() for var in variables_list]
    
    # Ensure we're extracting Series objects, not DataFrames
    values_data = []
    uncertainties_data = []
    
    for var in variables_list:
        # Get the values, ensuring we extract as Series not DataFrame
        if var in cleaned_df.columns:
            values_data.append(cleaned_df[var].reset_index(drop=True))
        else:
            raise KeyError(f"Variable '{var}' not found in dataframe columns: {cleaned_df.columns.tolist()}")
        
        # Get uncertainties
        if var in uncertainty_dict:
            uncertainties_data.append(uncertainty_dict[var])
        else:
            raise KeyError(f"Uncertainty for variable '{var}' not found")
    
    return values_data, uncertainties_data

def _get_header_data_and_uncert(header):
    '''
    Extracts the magnitude and uncertainty from a header of a dataframe
    Assumptions:
        - Magnitude column have a '(', since the units are written in parenthesis
        - If there's a number in the parenthesis, it's the constant uncertainty
        - Else, we assume the uncertainty isn't constant.
        - Uncertainty columns are named like 'δ{magnitude}'
    
    Parameters:
        - header: str, header of the dataframe
    Returns:
        - magnitude: str
        - uncert: float or 'not_const'
    '''

    header_split = header.replace(' ', '').split('(')
    magnitude, remnant = header_split
    
    # if inverse units are written like '1/s',
    # it gave an error detecting it as an uncertainty
    remnant = remnant.replace('1/','')

    # Extract uncertainties from the remnant string (regular expression)
    uncert_values = re.findall(r'[-+]?\d*\.\d+|\d+', remnant)
    # If they are uncerts with a coma decimal separator: r'[-+]?\d*\.|\,\d+|\d+'
    
    if len(uncert_values) == 1:
        # uncert_str_arr: list with one single element
        uncert = float(uncert_values[0])
    elif len(uncert_values) == 0:
        uncert = 'not_const'
    else:
        raise ValueError(
            f'Found several uncertainties {uncert_values}'
            + 'for the magnitude {magnitude}')
    
    return magnitude, uncert