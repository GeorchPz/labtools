# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:00:35 2021

@author: Jorge Pottiez López-Jurado
"""

import os

def get_parent_dir(path, levels=1):
    """Get the parent directory of a path at specified levels."""
    for _ in range(levels):
        path = os.path.dirname(path)
    return path


# Default directories
file_dir = os.path.abspath(__file__)
PROJECT_DIR = get_parent_dir(file_dir, levels=3)
DATA_DIR = os.path.join(PROJECT_DIR, 'data_files')


def get_folder_path(foldername):
    """Get the full path of a folder in the project directory."""
    if foldername == None:
        return None
    else:
        return os.path.join(PROJECT_DIR, foldername)

def get_file_path(filename, extension=None, directory=None):
    """
    Construct a full file path from a filename.
    
    Parameters:
        - filename : str, base filename (with or without extension)
        - extension : str, file extension (default: None)
        - directory : str, directory path (default: DATA_DIR)
    Returns:
        - str, full file path.
    """
    if extension is not None:
        filename = f'{filename}{extension}'

    if directory in [None, 'data']:
        directory = DATA_DIR
    elif directory == 'project':
        directory = PROJECT_DIR
    
    return os.path.join(directory, filename)

def ensure_directory(directory):
    """
    Create directory if it doesn't exist.
    
    Parameter:
        - directory : str, directory path
    """
    if directory is not None:
        os.makedirs(directory, exist_ok=True)
    else:
        pass

if __name__ == '__main__':
    print(f'PROJECT_DIR:\n{PROJECT_DIR}')
    print(f'DATA_DIR:\n{DATA_DIR}')