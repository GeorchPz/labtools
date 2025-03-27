import numpy as np
import matplotlib.cm as cm
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from .utils import setup_plot, plot_data_with_errors, plot_prediction_and_uncertainty, save_figure

def plot_multiple_regressions(
        datasets, regression_results, labels,
        x_label, y_label, title=None, legend_title=None,
        save=True, directory=None
        ):
    """
    Plots multiple regression with their uncertainty bands,
    and, optionally, saves the plot.
    
    Parameters:
        - datasets: (x, y, δx, δy), data and uncertainties
        - regression_results: dict, regression data (linear, polynomial, curve)
        - labels: str, labels for each regression
        - x_label, y_label, title: str, plot's info
        - legend_title: str, optional, title for the legend
        - save: bool, whether to save the plot
    Returns:
        - fig, ax: matplotlib's figure and axis objects
    """
    
    fig, ax = setup_plot(title, x_label, y_label)

    n = len(datasets)
    if n < 8:
        colours = ['blue','orange','green','red','purple','cyan','pink']
        if True:
            markers = ['o', '^', 's', 'v', '<', '*', '>', 'x', 'd']
        else:
            # If we want no markers
            markers = ['.'] * n
    else:
        colours = cm.rainbow(np.linspace(0, 1, n))
        markers = ['.'] * n
    
    legend_handles = []
    
    # Plot each dataset and its regression
    for i, (dataset, reg_result, label) in enumerate(
        zip(datasets, regression_results, labels)
        ):
        x, y, δx, δy = dataset
        
        plot_data_with_errors
        ax.errorbar(
            x, y, xerr= δx, yerr= δy, marker= markers[i],
            color= colours[i], alpha=0.6, ecolor= 'dimgray',
            capsize= 2, elinewidth= 1.5
            )
        x_line = np.linspace(min(x), max(x), 100)
        
        if 'a' in reg_result and 'b' in reg_result:
            # Linear regression
            reg_result = reg_result
            A = reg_result['a']
            B = reg_result['b']
            δA = reg_result['a_err']
            δB = reg_result['b_err']
            r = reg_result['r']
            
            # Predictions
            y_pred = A + B*x_line
            y_lower = (A - δA) + (B - δB)*x_line
            y_upper = (A + δA) + (B + δB)*x_line

            plot_prediction_and_uncertainty(
                ax, x_line, y_pred, y_lower, y_upper, color= colours[i]
                )
            # Legend
            label += ' (r = {r:.3f})'
        
        elif 'poly_model' in reg_result:
            # Polynomial regression
            poly_model = reg_result['poly_model']
            coeffs = reg_result['coefficients']
            errors = reg_result['errors']
            
            # Create models with the upper and lower bounds of the uncertainty
            poly_model_u = np.poly1d(coeffs + errors)
            poly_model_d = np.poly1d(coeffs - errors)

            plot_prediction_and_uncertainty(
                ax, x_line, poly_model(x_line),
                poly_model_d(x_line), poly_model_u(x_line), color= colours[i]
                )
        
        elif 'parameters' in reg_result:
            # Curve regression
            params = reg_result['parameters']
            errors = reg_result['errors']
            function = reg_result['function']
            # Predictions
            y_pred = function(params, x_line)
            y_upper = function(params + errors, x_line)
            y_lower = function(params - errors, x_line)

            plot_prediction_and_uncertainty(
                ax, x_line, y_pred, y_lower, y_upper, color= colours[i]
                )
        
        else:
            raise ValueError('Unknown regression type')

        legend_handles.append(mlines.Line2D(
            [], [], color= colours[i], marker= markers[i], markersize=8, label=label
            ))
    
    # Add uncertainty band to legend
    uncertainty_patch = mpatches.Patch(
        color= 'grey', alpha= 0.2,
        label= 'Uncertainty bands'
        )
    legend_handles.append(uncertainty_patch)
    
    # Legend, depending on the number of datasets
    if n % 2 == 0:
        # Legend at the bottom
        legend = ax.legend(
            title= legend_title, handles= legend_handles, bbox_to_anchor= (0,-0.12,1,0),
            loc= 'upper left', ncol= 2, mode= 'expand', labelspacing= 1, borderaxespad= 0.
            ) # Should 'expand' be used?
    elif n < 4:
        # Legend inside the plot
        legend = ax.legend(
            title = legend_title, handles= legend_handles,
            loc= 'best', fancybox= True
            )
    else:
        # Legend at the right
        legend = ax.legend(
            title= legend_title, handles= legend_handles, bbox_to_anchor= (1.01,0.5),
            loc= 'center left', labelspacing= 1, borderaxespad= 0.
            )
    
    if save:
        save_figure(fig, title, prefix='MultiRegs_', legend=legend, directory=directory)
    
    return fig, ax