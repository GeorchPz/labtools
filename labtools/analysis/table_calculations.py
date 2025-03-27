# -*- coding: utf-8 -*-
"""
Module for calculating formula-based values from tabular data.

This module provides functions for applying formulas to tabular data with
uncertainty propagation and exporting the results.
"""

import pandas as pd

from ..uncertainties import rounder, propagate_uncertainty, get_latex_equations
from ..data import get_excel_data_and_uncertainties
from .statistics import calculate_statistics

def calculate_formula_values(variables, equation, data_values, data_uncertainties, dependency='Independent'):
    """
    Calculate formula values and propagate uncertainties for tabular data.
    
    Parameters:
        - variables : str
            Comma-separated variable names
        - equations : str
            Formula equation (with = sign, e.g., "y = a*x + b")
        - data_values : list
            List of arrays with variable values
        - data_uncertainties : list
            List of arrays with variable uncertainties
        - dependency : str
            'Dependent' or 'Independent' variables
    
    Returns:
        - tuple : (result_name, result_values, result_uncertainties, latex_formulas)
    """
    # Split equation into left and right sides
    result_name, expression = equation.split('=')
    result_name = result_name.strip()
    expression = expression.strip()
    
    # Calculate values with uncertainty propagation
    result_values, result_uncertainties = propagate_uncertainty(
        variables, expression, data_values, data_uncertainties, dependency
    )
    
    # Get LaTeX formulas
    _, formula_latex, uncertainty_latex = get_latex_equations(
        variables, equation, dependency, print_latex=False
    )
    
    return result_name, result_values, result_uncertainties, [formula_latex, uncertainty_latex]

def apply_formulas_to_dataframe(dataframe, variables, equations, dependency='Independent'):
    """
    Apply multiple formulas to a dataframe and calculate values with uncertainties.
    
    Parameters:
        - dataframe : pandas.DataFrame
            Data frame containing the variables
        - variables : str
            Comma-separated variable names
        - equations : str, list
            List of formula equations
        - dependency : str or list
            'Dependent' or 'Independent' variables
    
    Returns:
        - tuple : (computed_dataframe, summary_dataframe)
    """
    # Get the variable data and uncertainties from the dataframe
    data_values, data_uncertainties = get_excel_data_and_uncertainties(variables, dataframe)
    computed_df = dataframe.copy()
    summary_data = []
    
    if isinstance(equations, str):
        if ',' in equations:
            equations = equations.replace(' ', '').split(',')
        else:
            equations = [equations]

    if isinstance(dependency, str):
        dependencies = [dependency] * len(equations)
    else:
        dependencies = dependency

    # Process each equation
    for equation, dependency in zip(equations, dependencies):
        # Calculate formula values
        result_name, values, uncertainties, latex_formulas = calculate_formula_values(
            variables, equation, data_values, data_uncertainties, dependency
        )
        # Add to the computed dataframe
        computed_df[f'{result_name} (UNITS)']  = values
        computed_df[f'δ{result_name}'] = uncertainties
        computed_df[f'{result_name}'] = rounder(values, uncertainties)
    
        
        # Calculate mean and relative uncertainty for the summary
        mean_stats = calculate_statistics(result_name, values, uncertainties)
        mean_df = pd.DataFrame(mean_stats)
        
        # Add LaTeX formulas
        latex_df = pd.DataFrame({'LaTeX Formulas': latex_formulas})
        
        # Combine mean stats and LaTeX formulas
        summary_df = pd.concat([mean_df, latex_df], axis='columns')
        summary_data.append(summary_df)
    
    # Combine all summary dataframes
    summary_df = pd.concat(summary_data, axis='index')
    
    return computed_df, summary_df

sheet_names = ['Computed table', 'Summary']