# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:00:35 2021

@author: Jorge Pottiez López-Jurado
"""

import re

from .exports import read_excel

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
    df = read_excel(filename, directory=data_dir)
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
    '''

    headers = dataframe.columns.values
    uncertainty_dict = {}
    
    # Extracting the data and uncertainty from the headers
    for header in headers:
        if '(' in header:
            magnitude, uncert = _get_header_data_and_uncert(header)
            uncertainty_dict[magnitude] = uncert
        else:
            # We remove possible spaces from header (for uncert columns)
            magnitude = header.replace(' ', '')
        
        # Rename each column of the dataframe, removing uncerts
        dataframe = dataframe.rename({header: magnitude}, axis = 'columns')
    
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
    variables_list = [v.strip() for v in variables_list]
    
    variables_data = [dataframe[var] for var in variables_list]
    uncertainties_data = [uncertainty_dict[i] for i in variables_list]
    
    return variables_data, uncertainties_data

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