# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

import numpy as np
from ..uncertainties import round_with_uncertainty

def polynomial_regression(x, y, δx=None, δy=None, degree=3):
    '''
    Perform polynomial regression, with or without uncertainties measurement.
    Based on numpy.polyfit.
    
    Parameters:
        - x : array-like, independent variable
        - y : array-like, dependent variable
        - δx : array-like, uncertainties in x
        - δy : array-like, uncertainties in y
        - degree : int, polynomial degree
    Returns:
        dict, Regression results containing:
            - coefficients: Array of coefficients (highest degree first) 
            - errors: Uncertainties in coefficients
            - poly_model: np.poly1d object
            - degree: int, polynomial
        '''
    
    if δx is None and δy is None:
        coeffs, errors = _polynomial_regression_standard(x, y, degree)
    elif δx is None or δy is None:
        δx = np.zeros_like(x) if δx is None else δx
        δy = np.zeros_like(y) if δy is None else δy
        coeffs, errors = _polynomial_regression_weighted(x, y, δx, δy, degree)
    else:
        coeffs, errors = _polynomial_regression_weighted(x, y, δx, δy, degree)
    
    # Make polynomial model
    poly_model = np.poly1d(coeffs)

    return {
        'coefficients': coeffs,
        'errors': errors,
        'poly_model': poly_model,
    }

def polynomial_format_formula(coeffs, errors, x_magnitude='x', y_magnitude='y'):
    """
    Generate a formatted polynomial formula string.
    
    Parameters:
        - coeffs : array-like, coefficients of the polynomial
        - errors : array-like, uncertainties in the coefficients
        - x_magnitude : str, name of the independent variable
        - y_magnitude : str, name of the dependent variable
    Returns:
        - formula : str, formatted polynomial formula
    """
    
    terms = []
    n = len(coeffs)
    
    for i, (coeff, err) in enumerate(zip(coeffs, errors)):
        power = n - i - 1
        
        # Format coefficient with uncertainty
        coef_str = f"({round_with_uncertainty(coeff, err)})"
        
        if power == 0:
            term = coef_str
        elif power == 1:
            term = f"{coef_str}·{x_magnitude}"
        else:
            term = f"{coef_str}·{x_magnitude}^{power}"
            
        terms.append(term)
    
    formula = f"{y_magnitude}({x_magnitude}) = " + " + ".join(terms)
    return formula

def _polynomial_regression_standard(x, y, degree):
    '''
    Perform polynomial regression without measurement uncertainties.
    Based on numpy.polyfit.

    Parameters:
        - x : array-like, independent variable
        - y : array-like, dependent variable
        - degree : int, polynomial degree
    Retunrs:
        - coefs : array, coefficients of the polynomial
        - err : array, uncertainties of the coefficients (higher exponent first)
    '''
    coeffs, cov = np.polyfit(x, y, degree, cov=True)
    # Errors (based on the covarience diagonal)
    errors = np.sqrt(np.diag(cov))
    
    return coeffs, errors

def _polynomial_regression_weighted(x, y, δx, δy, degree):
    '''
    Perform polynomial regression with measurement uncertainties.
    Based on numpy.polyfit and weighted least squares.

    Parameters:
        - x : array-like, independent variable
        - y : array-like, dependent variable
        - x_err : array-like, uncertainties in x
        - y_err : array-like, uncertainties in y
        - degree : int, polynomial degree
    Returns:
        - coefs : array, coefficients of the polynomial
        - err : array, uncertainties of the coefficients (higher exponent first)
    '''
    # Initial estimate with a non weighted fit
    coeffs_nw, errors_nw = _polynomial_regression_standard(x, y, degree)
    δy_est = np.polyval(coeffs_nw, δx)

    # Weights for the least squares fit
    weights = 1 / np.sqrt((δy_est)**2 + δy**2)
    
    # Perform weighted polynomial fit
    coeffs, cov = np.polyfit(x, y, degree, w=weights, cov=True)
    
    # Errors (based on the covariance diagonal)
    errors = np.sqrt(np.diag(cov))
    
    return coeffs, max(errors_nw, errors)