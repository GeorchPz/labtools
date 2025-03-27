# -*- coding: utf-8 -*-
"""
LabTools Workflow Example - Linear Regression Analysis

This script demonstrates how to use the state-based LabTools unified interface
to perform a complete linear regression analysis workflow.
"""

from . import LabTools
import pandas as pd
import matplotlib.pyplot as plt

def linear_regression_workflow():
    """Perform a complete linear regression analysis workflow using the state-based LabTools."""
    
    # 1. Initialize LabTools with analysis parameters
    x_label = 'λ^{-2} (nm$^{-2}$)'
    y_label = 'n'
    filename = 'spectrum_data'
    equation = "n = b*λ^{-2} + a"
    title = "Refractive Index vs. Inverse Wavelength Squared"
    
    print(f"Initializing analysis for {filename}...")
    lab = LabTools(
        filename=filename,
        variables=f"{x_label}, {y_label}",
        equation=equation,
        title=title
    )
    
    # 2. Load data - data is stored in the LabTools object
    print(f"Loading data from {filename}.xlsx...")
    raw_data, extracted_data = lab.load_data()
    
    print(f"Data loaded: {len(extracted_data['x'])} data points")
    
    # 3. Perform linear regression analysis
    print("Performing linear regression analysis...")
    regression = lab.linear_regression()
    
    # Print results
    a, b = regression['coefficients']
    δa, δb = regression['errors']
    r = regression['r']
    
    print(f"Linear regression results:")
    print(f"Correlation coefficient: r = {r:.4f}")
    print(f"Slope: b = {b:.4f} ± {δb:.4f}")
    print(f"Intercept: a = {a:.4f} ± {δa:.4f}")
    print(f"Equation: {regression['formula']}")
    
    # 4. Generate LaTeX formulas
    print("\nGenerating LaTeX formulas...")
    result_name, formula_latex, uncertainty_latex = lab.get_latex_equations()
    
    print(f"Formula: {formula_latex}")
    print(f"Uncertainty: {uncertainty_latex}")
    
    # 5. Create visualization - uses regression results stored in the LabTools object
    print("\nCreating visualization...")
    fig, ax = lab.plot_regression(save=True)
    
    # 6. Calculate statistics
    print("\nCalculating statistics...")
    variable_name = 'n'
    stats = lab.calculate_statistics(
        variable_name, 
        extracted_data['y'], 
        extracted_data['y_err']
    )
    
    print(f"Statistics for {variable_name}:")
    print(f"Standard mean: {stats['Standard']['Mean']}")
    print(f"Weighted mean: {stats['Weighted']['Mean']}")
    print(f"Relative uncertainty: {stats['Standard']['Rel Uncert']}")
    
    # 7. Prepare results DataFrames
    print("\nPreparing results for export...")
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'Parameter': ['Correlation coefficient', 'Slope', 'Intercept'],
        'Value': [r, b, a],
        'Uncertainty': [None, δb, δa],
        'Formatted': [
            f"{r:.4f}", 
            lab.round_with_uncertainty(b, δb), 
            lab.round_with_uncertainty(a, δa)
        ]
    })
    
    # Create LaTeX DataFrame
    latex_df = pd.DataFrame({
        'Equation': ['Linear Model', 'Uncertainty'],
        'LaTeX': [formula_latex, uncertainty_latex]
    })
    
    # Create statistics DataFrame
    stats_df = pd.DataFrame(stats)
    
    # 8. Export results to Excel - using the state-based save method
    data_to_save = [results_df, latex_df, stats_df]
    sheet_names = ['Regression Results', 'LaTeX Formulas', 'Statistics'] 
    
    print("\nExporting results to Excel...")
    output_path = lab.save_data(
        processed_data=data_to_save,
        new_filename='spectrum_analysis_results',
        sheet_names=sheet_names
    )
    
    print("\nWorkflow completed successfully!")
    print(f"Results saved to: {output_path}")
    print(f"Plot saved to results directory")
    
    # Return useful objects for further analysis if needed
    return fig, regression, stats

if __name__ == "__main__":
    fig, regression, stats = linear_regression_workflow()
    
    # Display the plot after execution if running interactively
    plt.show()
