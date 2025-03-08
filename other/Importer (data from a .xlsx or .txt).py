# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:05:53 2020

@author: jorge
"""

import os
import pandas as pd

def importer(path):
    '''Imports the data from a .xlsx or .txt file'''
    f_name, f_extension = os.path.splitext(path)
    
    if f_extension == '.xlsx':
        return pd.read_excel(path)
    elif f_extension == '.txt':
        return pd.read_csv(path, delimiter = '\t')
    else:
        raise ValueError('The {} extension file is not yet supported'.format(f_extension))