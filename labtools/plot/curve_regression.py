import numpy as np

from .utils import setup_plot, plot_data_with_errors, plot_prediction_and_uncertainty, save_figure

def plot_curve_regression(
        x, y, δx, δy, curve_results,
        x_label, y_label, title=None,
        save=True, directory=None
        ):
    """
    Plots a curve regression with its uncertainty band,
    and, optionally, saves the plot.

    Parameters:
        - x, y, δx, δy: array-like, data and uncertainties
        - curve_results: dict, curve regression data
        - x_label, y_label, title: str, plot's info
        - save: bool, whether to save the plot
    Returns:
        - fig, ax: matplotlib's figure and axis objects
    """
    params = curve_results['parameters']
    errors = curve_results['errors']
    function = curve_results['function']
    format_formula = curve_results['formula']

    fig, ax = setup_plot(title, x_label, y_label)

    plot_data_with_errors(ax, x, y, δx, δy)

    # Predictions
    x_line = np.linspace(min(x), max(x), 100)
    y_pred = function(params, x_line)
    y_upper = function(params + errors, x_line)
    y_lower = function(params - errors, x_line)
    
    plot_prediction_and_uncertainty(
        ax, x_line, y_pred, y_lower, y_upper,
        label='Curve regression:\nNO ESTA Yet' #+ format_formula
        )
    # Legend
    ax.legend(loc='best', labelspacing=1)
    
    # Export
    if save:
        save_figure(fig, title, prefix='CurveReg__', directory=directory)
    
    return fig, ax