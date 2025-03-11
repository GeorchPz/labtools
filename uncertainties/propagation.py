# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:13:45 2020

@author: Jorge Pottiez
"""
import numpy as np

from .utils.latex import latex_escape_special_characters
from .utils.symbolic import sp, create_formula_and_uncertainty, create_lambda_functions

def propagate_uncertainty(
        variables_str, expression_str, values, uncertainties,
        dependency='Independent'
        ):
    '''
    Calculate the result and uncertainty of a formula for given values and uncertainties.
    Note: if the function is multivariable, each variable must be a subarray.
    Parameters:
        - variables_str: string, variables separated by commas
        - expression_str: string, mathematical expression without "=" sign
        - values: array-like, values of the variables
        - uncertainties: array-like, uncertainties of the variables
        - dependency: string with the dependency type ('Dependent' or 'Independent')
    Returns:
        - result: array-like, calculated result
        - uncertainty: array-like, related uncertainty
    '''
    # Create symbolic expressions
    formula_symb, uncertainty_symb = create_formula_and_uncertainty(
        variables_str, expression_str, dependency
        )
    # Create lambda functions
    formula_func, uncertainty_func = create_lambda_functions(
        variables_str, formula_symb, uncertainty_symb
        )
    
    # Ensure values and uncertainties are arrays
    values = np.asarray(values)
    uncertainties = np.asarray(uncertainties)

    # Calculate result and its uncertainty propagation
    result = formula_func(*values)
    uncertainty = uncertainty_func(*values, *uncertainties)

    return result, uncertainty

def get_latex_equations(
        variables, equation, dependency='Independent', print_latex=True):
    '''
    Get LaTeX representations of formula and uncertainty expressions,
    removing special characters from the LaTeX code.

    Parameters:
        - variables: str,   Variables separated by commas
        - equation: str,    Equation expression
        - dependency: str,  Dependency type ('Dependent' or 'Independent')
        - print_latex: bool, Whether to print the LaTeX code
    Returns:
        - result_variable: str, Result variable name
        - formula_latex: str,   LaTeX formula expression
        - uncertainty_latex: str, LaTeX uncertainty expression
    '''
    
    if '=' in equation:
        result_variable, expression = equation.replace(' ', '').split('=')
    else:
        result_variable = 'f'
        expression = equation

    result_uncert = 'δ' + result_variable

    # Create symbolic expressions
    formula_symb, uncertainty_symb = create_formula_and_uncertainty(
        variables, expression, dependency
    )
    # Create symbolic equations
    formula_eq = sp.Eq(sp.Symbol(result_variable), formula_symb)
    uncertainty_eq = sp.Eq(sp.Symbol(result_uncert), uncertainty_symb)

    if print_latex:
        sp.pprint(formula_eq)
        sp.pprint(uncertainty_eq)
    
    # Convert to LaTeX
    formula_latex = sp.latex(formula_eq)
    uncertainty_latex = sp.latex(uncertainty_eq)

    formula_latex = latex_escape_special_characters(formula_latex, structure=False)
    uncertainty_latex = latex_escape_special_characters(uncertainty_latex, structure=False)

    return result_variable, formula_latex, uncertainty_latex