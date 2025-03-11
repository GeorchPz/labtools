# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 00:45:38 2023

@author: Jorge Pottiez López-Jurado
"""

import sigfig

def isNaN(obj):
    '''
    Checks if an object is NaN

    from:
    https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
    '''
    return obj != obj

def isiterable(obj):
    '''
    Checks if an object is iterable.

    from:
    https://stackoverflow.com/questions/4668621/how-to-check-if-an-object-is-iterable-in-python
    '''
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def rounder(value, uncertainty, notation='standard'):
    '''
    Rounds a single value with its uncertainty.
    The uncertainty cut-off rounding is 29.
    Scientific notation: change notation to 'sci'
    Example: 3.39 ± 0.44 → 3.4 ± 0.4

    Parameters:
        - value : float, value to round
        - uncertainty : float, uncertainty to round
        - notation : str, optional, 'standard' or 'sci'
    Returns:
        - str : Formatted string "value ± uncertainty"
    '''
    return sigfig.round(value, uncertainty, cutoff=29, notation=notation)

def round_with_uncertainty(value, uncertainty, notation='standard'):
    '''
    Rounds a single value or an iterable of values with their uncertainties.
    The uncertainty cut-off rounding is 29.
    Scientific notation: change notation to 'sci'

    Parameters:
        - value : float or iterable, value(s) to round
        - uncertainty : float or iterable, uncertainty(ies) to round
        - notation : str, optional, 'standard' or 'sci'
    Returns:
        - str or list : Formatted string(s) "value ± uncertainty"
    '''

    if isNaN(value):
        return 'nan ± nan'
    elif isinstance(value, (int, float)):
        return rounder(value, uncertainty)
    elif isiterable(value):
        return [ rounder(val, err) for val, err in zip(value, uncertainty) ]
    else:
        return 'Invalid input'