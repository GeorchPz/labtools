# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 00:45:38 2023

@author: Jorge Pottiez López-Jurado
"""

import math
import warnings

def round_with_uncertainty(value, uncertainty, notation='standard'):
    """
    Round a value based on its uncertainty following standard scientific rules.
    
    Parameters:
        value (float): The measured value
        uncertainty (float): The uncertainty of the measurement
        notation (str): 'standard' or 'sci' for scientific notation
    
    Returns:
        str: Formatted string "value ± uncertainty"
    """
    # Handle special cases
    if math.isnan(value) or math.isnan(uncertainty):
        return "nan ± nan"
    
    elif uncertainty <= 0:
        warnings.warn("Uncertainty must be positive, using absolute value")
        uncertainty = abs(uncertainty)
    
    # Determine significant digits
    elif uncertainty == 0:
        sig_digits = 3  # Default if uncertainty is zero

    else:
        # Find position of first significant digit in uncertainty
        unc_exponent = get_exponent(uncertainty)
        first_digit = uncertainty * 10**(-unc_exponent) 
        
        # Special case: if uncertainty starts with 1, use two significant digits
        if 1 <= first_digit < 2:
            sig_digits = -unc_exponent + 1
        else:
            sig_digits = -unc_exponent
    
    # Round the values
    val_rounded = round(value, sig_digits)
    unc_rounded = round(uncertainty, sig_digits)
    
    # Format the output
    if (
        notation.lower() in ('sci', 'scientific') and
        (abs(val_rounded) < 0.01 or abs(val_rounded) >= 1000)
    ):
        # Scientific notation
        exp_mantissa = get_exponent(abs(val_rounded))
        val_mantissa = val_rounded * 10**(-exp_mantissa)
        unc_mantissa = unc_rounded * 10**(-exp_mantissa)

        format_mant = f".{sig_digits + exp_mantissa}f"
        return f"({val_mantissa:{format_mant}} ± {unc_mantissa:{format_mant}})·10^{exp_mantissa}"

    else:
        # Standard notation with proper decimal places
        format_spec = f".{max(0, sig_digits)}f"
        return f"{val_rounded:{format_spec}} ± {unc_rounded:{format_spec}}"


def rounder(value, uncertainty, notation='standard'):
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

    if isiterable(value):
        return [ round_with_uncertainty(val, err, notation) for val, err in zip(value, uncertainty) ]
    elif math.isnan(value):
        return 'nan ± nan'
    elif isinstance(value, (int, float)):
        return round_with_uncertainty(value, uncertainty, notation)
    else:
        raise TypeError('Invalid input type')


def round_to_sigfigs(value, sigfigs):
    """
    Round a number with the specified number of significant figures,
    formatting it in scientific notation if needed.
    
    Parameters:
        value (float): The value to format
        sigfigs (int): Number of significant figures
    
    Returns:
        str: Formatted string
    """
    if math.isnan(value):
        return "nan"
    elif value == 0:
        return "0." + "0" * (sigfigs - 1)

    # Determine the number of decimal places needed
    exponent = get_exponent(abs(value))
    prec = sigfigs - exponent - 1
    rounded = round(value, prec)
    
    exp_rounded = get_exponent(abs(rounded))
    # For small or large numbers, use scientific notation
    if abs(rounded) < 0.01 or abs(rounded) >= 1000:
        
        mantissa = rounded * 10**(-exp_rounded)
        return f"{mantissa:.{sigfigs-1}f}e{exp_rounded}"
    
    # Calculate decimal places needed
    decimal_places = max(0, sigfigs - exp_rounded - 1)
    
    # Format the number
    return f"{rounded:.{decimal_places}f}"


def get_exponent(x):
    '''Calculate the exponent of a number.'''
    if math.isnan(x):
        return math.nan
    elif x == 0:
        return 0
    else:
        return math.floor(math.log10(x))


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


if __name__ == "__main__":
    
    notation = 'sci'
    print(f"{notation} notation:")
    print(round_with_uncertainty(123.456789, 0.22, notation))
    print(round_with_uncertainty(0.00345678, 0.00021, notation))
    print(round_with_uncertainty(9876.54321, 1.5, notation))
    print(round_with_uncertainty(123.456789*1e10, 0.22*1e10, notation))
    print(round_with_uncertainty(123.456789*1e-6, 0.22*1e-6, notation))

    print("\nSignificant figures:")
    print(round_to_sigfigs(123.456789, 3))
    print(round_to_sigfigs(0.00345678, 3))
    print(round_to_sigfigs(9876.54321, 3))
    print(round_to_sigfigs(0, 3))
    print(round_to_sigfigs(math.nan, 3))