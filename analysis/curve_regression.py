# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

import numpy as np
from scipy.odr import ODR, Model, RealData

from ..uncertainties.format import rounder

# Does Correct fitting with scipy curve_fit including errors in x?
# https://stackoverflow.com/questions/26058792/correct-fitting-with-scipy-curve-fit-including-errors-in-x

def curve_regression(x, y, δx, δy, function, initial_params=None, fit_type=0):
    '''
    Perform regression with a custom function using Orthogonal Distance Regression (ODR).

    Parameters:
        - x : array-like
            Independent variable
        - y : array-like
            Dependent variable
        - δx : array-like or float
            Uncertainty in x
        - δy : array-like or float
            Uncertainty in y
        - function : callable
            Function to fit: f(params, x) -> y
        - initial_params : optional list
            Initial parameter estimates
        - fit_type : optional int
            0: explicit ODR, 1: implicit ODR, 2: ordinary least-squares

    Returns:
        dict, Regression results containing:
            - parameters: Fitted parameters
                (ordered according to function)
            - errors: Parameter uncertainties
            - function: The function used for fitting
    '''
    # Handle default uncertainties
    if isinstance(δx, (int, float)):
        δx = np.full_like(x, δx)
    if isinstance(δy, (int, float)):
        δy = np.full_like(y, δy)
    
    # Default initial parameters
    if initial_params is None:
        initial_params = [1.0, 1.0] # Default to 2 parameters
    
    data = RealData(x, y, δx, δy)
    model = Model(function)
    # Perform ODR
    odr = ODR(data, model, beta0=initial_params)
    odr.set_job(fit_type=fit_type)
    output = odr.run()
    
    return {
        'parameters': output.beta,
        'errors': output.sd_beta,
        'function': function
    }

def curve_format_formula(parameters, errors, parameter_symbols, formula_template, x_symbol='x', y_symbol='y'):
    '''
    Generate a formatted string for the curve formula with parameter values.

    Parameters:
        - parameters : array-like
            Fitted parameter values
        - errors : array-like
            Parameter uncertainties
        - parameter_symbols : list
            List of parameter symbols in the formula
        - formula_template : str
            Formula template with parameter symbols
        - x_symbol : str
            Symbol for the independent variable
        - y_symbol : str
            Symbol for the dependent variable
    Returns:
        str, Formatted formula with parameter values
    '''
    # Create a copy of the template
    formula = formula_template

    # Replace parameter symbols with values
    for symbol, value, uncert in zip(parameter_symbols, parameters, errors):
        formula = formula.replace(symbol, rounder(value, uncert))
    
    return formula