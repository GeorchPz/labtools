import numpy as np

from .utils import setup_plot, plot_data_with_errors, plot_prediction_and_uncertainty, save_figure

def plot_linear_regression(
        x, y, δx, δy, regression_results, format_formula,
        x_label, y_label, title=None, save=True
        ):
    """
    Plots a linear regression with its uncertainty band,
    and, optionally, saves the plot and its data.
    
    Parameters:
        - x, y, δx, δy: array-like, data and uncertainties
        - regression_results: dict, linear regression data
        - format_formula: str, formatted formula for the legend
        - x_label, y_label, title: str, plot's info
        - save: bool, whether to save the plot and its data
    Returns:
        - fig, ax: matplotlib's figure and axis objects
    """
    A, B = regression_results['coefficients']
    δA, δB = regression_results['errors']
    r = regression_results['r']

    fig, ax = setup_plot(title, x_label, y_label)

    plot_data_with_errors(ax, x, y, δx, δy)

    # Predictions
    x_line = np.linspace(min(x), max(x), 100)
    y_pred  = A + B*x_line
    y_lower = (A - δA) + (B - δB)*x_line
    y_upper = (A + δA) + (B + δB)*x_line

    plot_prediction_and_uncertainty(
        ax, x_line, y_pred, y_lower, y_upper,
        label='Linear regression' + f':\n{format_formula}'
        )
    # Legend
    ax.legend(loc='best', labelspacing=1)
    
    '''EXPORT'''
    if save:
        save_figure(fig, title, prefix='LinReg__')
    
    return fig, ax