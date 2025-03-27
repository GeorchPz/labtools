# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado

This module contains manual implementations of linear regression methods,
as an exercise to understand the underlying mathematics.
"""

import numpy as np
from ..uncertainties import round_with_uncertainty

is_scalar = lambda x: isinstance(x, (int, float))

def linear_regression(x, y, δx=None, δy=None):
    """
    Perform linear regression, with or without uncertainties measurement.
    
    Parameters:
    -----------
    x : array-like
        Independent variable
    y : array-like
        Dependent variable
    δx : array-like or float, optional
        Uncertainty in x
    δy : array-like or float, optional
        Uncertainty in y
        
    Returns:
    --------
    dict
        Regression results containing:
        - a: Intercept
        - b: Slope
        - a_err: Intercept error
        - b_err: Slope error
        - r: Correlation coefficient
    """

    # Calculate correlation coefficient
    r = linear_correlation(x, y)
    
    if is_scalar(δx) and is_scalar(δy):
        a, b, δa, δb = _linear_regression_standard(x, y, δx, δy)
    elif not is_scalar(δx) and not is_scalar(δy):
        a, b, δa, δb = _linear_regression_weighted(x, y, δx, δy)
    else:
        if is_scalar(δx):
            δx = np.full_like(x, δx)
        elif δx is None:
            δx = np.zeros_like(x)
        
        if is_scalar(δy):
            δy = np.full_like(y, δy)
        elif δy is None:
            δy = np.zeros_like(y)
        
        a, b, δa, δb = _linear_regression_weighted(x, y, δx, δy)
    
    coeffs = [a, b]
    errors = [δa, δb]

    return {
        'coefficients': coeffs,
        'errors': errors,
        'r': r,
    }

def linear_format_formula(coeffs, errors, x_magnitude='x', y_magnitude='y'):
    '''
    Generate a formatted string for the linear regression formula.

    Parameters:
        - coeffs : array-like
            Fitted coefficients (a, b)
        - errors : array-like
            Coefficient uncertainties (δa, δb)
        - x_magnitude : str, optional
            Label for the independent variable
        - y_magnitude : str, optional
            Label for the dependent variable
    Returns:
        - str, Formatted formula string
    '''
    a, b = coeffs
    δa, δb = errors
    
    a_str = f"({round_with_uncertainty(a, δa)})"
    b_str = f"({round_with_uncertainty(b, δb)})"
    
    formula = f"{y_magnitude} = {b_str}·{x_magnitude} + {a_str}"
    
    return formula

def linear_correlation(x, y):
    '''
    Calculate Pearson's linear correlation coefficient
    
    Parameters:
        - x : array-like
            Independent variable
        - y : array-like
            Dependent variable
    Returns:
        - float
            Correlation coefficient
    '''
    N_ = len(x) - 1 # n-1 for unbiased estimation

    # Means & standard desviation
    xm, ym = x.mean(), y.mean()
    sx = np.sqrt(sum( (x-xm)**2 ) / N_)
    sy = np.sqrt(sum( (y-ym)**2 ) / N_)
    # Covariance
    sxy = sum( (x-xm)*(y-ym) ) / N_
    
    return sxy / (sx*sy)

def _linear_regression_standard(x, y, δx, δy):
    '''
    Standard least square fitting to y = A + B·x, with constant uncertainties.
    
    Parameters:
        - x : array-like
            Independent variable
        - y : array-like
            Dependent variable
        - δx : float
            Uncertainty in x
        - δy : float
            Uncertainty in y
    Returns:
        - A : float
            Intercept
        - B : float
            Slope
        - δA : float
            Intercept error
        - δB : float
            Slope error
    '''
    N = len(x)
    Σx, Σy = sum(x), sum(y)
    Σx2 = sum(x**2)
    Σxy = sum(x*y)
    Δ = N*Σx2 - Σx**2
    # Regression coefficients
    A = ( Σx2*Σy - Σx*Σxy )/Δ
    B = ( N*Σxy - Σx*Σy )/Δ
    # Theoretical error estimations
    δy_teo = np.sqrt( sum((y - A - B*x)**2) / (N-2) )
    δy_equiv = np.sqrt( δy**2 + (B*δx)**2 )
    δy = max(δy_equiv, δy_teo)
    # Slope uncertainties
    δA = δy*np.sqrt( Σx2/Δ )
    δB = δy*np.sqrt( N/Δ )
    
    return A, B, δA, δB

def _linear_regression_weighted(x, y, δx, δy):
    '''
    Standar least square fitting with variable uncertainties.
    
    Parameters:
        - x : array-like
            Independent variable
        - y : array-like
            Dependent variable
        - δx : array-like
            Uncertainty in x
        - δy : array-like
            Uncertainty in y
    Returns:
        - A : float
            Intercept
        - B : float
            Slope
        - δA : float
            Intercept error
        - δB : float
            Slope error
    '''
    N = len(x)
    # Initial δ estimate with a non weighted B
    B_nw = ( N*sum(x*y) - sum(x)*sum(y) )/( N*sum(x**2) - sum(x)**2 )
    δ = np.sqrt( δy**2 + (B_nw*δx)**2 )
    # Weights
    w = 1 / δ**2
    # Weighted sums
    Σw = sum(w)
    Σwx = sum(w*x)
    Σwx2 = sum(w*x**2)
    Σwy = sum(w*y)
    Σwxy = sum(w*x*y)
    # Weighted regression coefficients
    Δ = Σw*Σwx2-Σwx**2 
    A = (Σwx2*Σwy-Σwx*Σwxy)/Δ
    B = (Σw*Σwxy-Σwx*Σwy)/Δ
    # Their uncertainty
    δA = np.sqrt(Σwx2/Δ)
    δB = np.sqrt(Σw/Δ)
    
    return A, B, δA, δB