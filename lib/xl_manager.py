# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:00:35 2021

@author: Jorge Pottiez López-Jurado
"""

from os import path, makedirs
from re import findall

long_folderdir = r'C:\Users\jorge\OneDrive\Programas_py\Lab_programs\Lab_data'
folderdir = 'Lab_data'

def name2path(name, ext = '.xlsx', filedir = long_folderdir):
    '''Imports the data from an .xlsx'''
    file = name + ext
    return path.join(filedir, file)

def newpath(folder, filedir = folderdir):
    new_dir = path.join(filedir, folder)
    if not path.exists(new_dir):
        makedirs(new_dir)
    return new_dir

def vals_extracter(header):
    '''
    Finds the magnitude and the uncertainty in each header,
    by assuming that if there's a '(', it's a magnitude column
        - If value     → We assume constant uncert
        - If not value → We assume uncert isn't const
    '''
    header_split = header.replace(' ', '').split('(')
    print()
    magnitude, remnant = header_split
    
    # when units are written like 1/s, it gave so much problems, therefore:
    remnant = remnant.replace('1/','')
    # Extract uncert(s) with a regular expression
    uncert_str_arr = findall(r'[-+]?\d*\.\d+|\d+', remnant)
    # If they are uncerts with a coma decimal separator: r'[-+]?\d*\.|\,\d+|\d+'
    
    if len(uncert_str_arr) == 1:
        # uncert_str_arr: list with one single element
        uncert = float(uncert_str_arr[0])
    elif len(uncert_str_arr) == 0:
        uncert = 'not_const'
    else:
        raise ValueError(
            f'Found several uncertainties {uncert_str_arr}'
            + 'for the magnitude {magnitude}')
    
    return magnitude, uncert

def get_data_n_uncert(variab_str, dataframe):
    '''
    Gets the variables & related uncertainties arrays
    in the order of the variables' string
    (works with pandas' classes)
    '''
    headers = dataframe.columns.values
    # Dictionary where data is stored like: 'r': 0.02
    uncert_dict = {}
    
    for header in headers:
        
        if '(' in header:
            f_str, δf_num = vals_extracter(header)
            uncert_dict[f_str] = δf_num
        else:
            # We remove possible spaces from header (for uncert columns)
            f_str = header.replace(' ', '')
        
        # Rename each column of the dataframe, removing uncerts
        dataframe = dataframe.rename({header: f_str}, axis = 'columns')
    
    # Replacing 'not const' by uncert array
    for key in uncert_dict:
        if uncert_dict[key] == 'not_const' and 'δ' not in key:
            try:
                uncert_dict[key] = dataframe['δ' + key]
            except KeyError:
                # This appends when δkey is not found
                print(f'We assume: δ{key} = 0')
                uncert_dict[key] = 0
    
    var_arr = variab_str.split(',')
    # Creates arrays of the dataframe
    variab_data_arr = [dataframe[i] for i in var_arr]
    related_uncert_data_arr = [uncert_dict[i] for i in var_arr]
    
    return variab_data_arr, related_uncert_data_arr