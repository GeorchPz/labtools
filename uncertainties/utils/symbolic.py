# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:13:45 2020

@author: Jorge Pottiez
"""
import sympy as sp

class UncertaintyError(Exception):
    '''Custom exception for errors in uncertainty calculations'''
    pass

def create_formula_and_uncertainty(variables_str, expression_str, dependency):
    '''
    Create symbolic formulas for the given expression and its uncertainty.
    The uncertainty is calculated based on the dependency of the variables.

    Parameters:
        - variables_str: string with the variables separated by commas
        - expression_str: string with the formula expression without "=" sign
        - dependency: string with the dependency type ("Dependent" or "Independent")
    Returns:
        - formula_symb: symbolic expression for the formula
        - uncertainty_symb: symbolic expression for the uncertainty
    '''
    # Initialise pretty printing
    sp.init_printing() # Installing LaTeX would give better results
    
    # Create variables string list & symbols
    variables_list = [v.strip() for v in variables_str.split(',')]
    variables_sy   = sp.symbols(variables_str, real = True)
    
    # Handle single variable case
    if len(variables_list) == 1:
        variables_sy = [variables_sy]
    
    variables_dict = {k: v for k, v in zip(variables_list, variables_sy)}
    
    # Convert formula to sympy
    try:
        formula_symb = sp.sympify(expression_str, locals = variables_dict)
    except Exception as e:
        raise UncertaintyError('Error in formula: ' + str(e))
    
    # Create gradient vector & uncertainties list
    gradient, uncertainties = [], []
    
    for x in variables_sy:
        gradient.append( sp.diff(formula_symb,x) )
        uncertainties.append( sp.Symbol('δ' + str(x), positive = True) )
    
    # Calculate uncertainty based on variable dependency
    if dependency == 'Dependent':
        # Sum of absolutes
        uncertainty_symb = sum([ abs(diffx)*δx for (diffx, δx) in zip(gradient, uncertainties) ])
    
    elif dependency == 'Independent':
        # Square root of sum of squares
        squares_sum = sum([ (diffx*δx)**2 for (diffx, δx) in zip(gradient, uncertainties) ])
        uncertainty_symb = sp.sqrt(squares_sum)
    else:
        raise UncertaintyError(
            f'Invalid dependency type: {dependency}. '
            "Must be 'Dependent' or 'Independent'."
        )
    
    return formula_symb, uncertainty_symb

def create_lambda_functions(variables_str, formula_symb, uncertainty_symb):
    '''
    Create lambda functions for the formula and its uncertainty.

    Parameters:
        - variables_str: string with the variables separated by commas
        - formula_symb: symbolic expression for the formula
        - uncertainty_symb: symbolic expression for the uncertainty
    Returns:
        - formula_func: lambda function for the formula
        - uncertainty_func: lambda function for the uncertainty
    '''
    # Variable names for function arguments
    uncertainties_str = ','.join( 'δ' + x.strip() for x in variables_str.split(',') )
    all_variables_str = variables_str + ',' + uncertainties_str
    
    try:
        # Create lambda functions
        formula_func = sp.lambdify(variables_str, formula_symb)
        uncertainty_func = sp.lambdify(all_variables_str, uncertainty_symb)
    except Exception as e:
        raise UncertaintyError('Error creating lambda functions: ' + str(e))
    
    return formula_func, uncertainty_func