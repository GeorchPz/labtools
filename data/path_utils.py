# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:00:35 2021

@author: Jorge Pottiez López-Jurado
"""

from os import path, makedirs

# Default directories
PROJECT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
DATA_DIR = path.join(PROJECT_DIR, 'data_files')
RESULTS_DIR = path.join(PROJECT_DIR, 'results_files')

# print(DATA_DIR)

def get_file_path(filename, extension='.xlsx', directory=None):
    """
    Construct a full file path from a filename.
    
    Parameters:
        - filename : str, base filename (without extension)
        - extension : str, file extension (default: '.xlsx')
        - directory : str, directory path (default: DATA_DIR)
    Returns:
        - str, full file path.
    """
    filename = filename + extension

    if directory is None:
        directory = DATA_DIR
    elif directory == 'results':
        directory = RESULTS_DIR
    elif directory == 'project':
        directory = PROJECT_DIR
        
    return path.join(directory, filename)

def ensure_directory(directory):
    """
    Create directory if it doesn't exist.
    
    Parameter:
        - directory : str, directory path
    """
    if not path.exists(directory):
        makedirs(directory)