import numpy as np

from .utils import setup_plot, plot_data_with_errors, plot_prediction_and_uncertainty, save_figure

def plot_polynomial_regression(
        x, y, δx, δy, poly_results,
        x_label, y_label, title=None,
        save=True, directory=None
        ):
    """
    Plots a polynomial regression with its uncertainty band,
    and, optionally, saves the plot.
    
    Parameters:
        - x, y, δx, δy: array-like, data and uncertainties
        - poly_results: dict, polynomial regression data
        - x_label, y_label, title: str, plot's info
        - save: bool, whether to save the plot
    Returns:
        - fig, ax: matplotlib's figure and axis objects
    """
    
    coeffs = poly_results['coefficients']
    errors = poly_results['errors']
    poly_model = poly_results['poly_model']
    format_formula = poly_results['formula']
    
    fig, ax = setup_plot(title, x_label, y_label)
    
    plot_data_with_errors(ax, x, y, δx, δy)
    
    # Predictions
    x_line = np.linspace(min(x), max(x), 100)
    poly_model_u = np.poly1d(coeffs + errors)
    poly_model_d = np.poly1d(coeffs - errors)
    
    print(format(poly_model))

    plot_prediction_and_uncertainty(
        ax, x_line, poly_model(x_line), poly_model_d(x_line), poly_model_u(x_line),
        label='Polynomial regression:\n' + format_formula
        )
    # Legend
    ax.legend(loc='best', labelspacing= 1)
    
    # Export
    if save:
        save_figure(fig, title, prefix='PolyReg__', directory=directory)

    return fig, ax