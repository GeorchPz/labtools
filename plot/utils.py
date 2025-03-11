import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# ¿¿¿
# from ..utils.paths import get_figure_path
from ..data.extract_data import name2path
# ???

# Standard font for plots
FONT = {
    'family': 'serif',
    'color': 'black',
    'weight': 'normal',
    'size': 14
}

def setup_plot(
        title, x_label, y_label, figsize=(9,6),
        grid=True, minor_ticks=True
        ):
    """Creates and sets up a basic plot with common settings"""
    fig, ax = plt.subplots(figsize=figsize)
    
    # Labels
    ax.set_title(title, fontdict=FONT, fontsize=16)
    ax.set_xlabel(x_label, fontdict=FONT)
    ax.set_ylabel(y_label, fontdict=FONT)
        
    # Configure grid
    if grid:
        ax.grid(which='major', linestyle='--', alpha=0.6)
    elif grid == 'both':
        ax.grid(which='major', linestyle='--', alpha=0.6)
        ax.grid(which='minor', linestyle='-', alpha=0.3)
    elif grid == 'major':
        ax.grid(which='major', linestyle='--', alpha=0.6)
    elif grid == 'minor':
        ax.grid(which='minor', linestyle='-', alpha=0.3)
    
    # Add minor ticks if requested
    if minor_ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    return fig, ax

def plot_data_with_errors(ax, x, y, δx, δy):
    """Plot data points with error bars"""
    return ax.errorbar(
        x, y, xerr=δx, yerr=δy, fmt='k.',
        ecolor='dimgrey', capsize=4, elinewidth=2
    )

def plot_prediction_and_uncertainty(
        ax, x, y_pred, y_lower, y_upper,
        label=None, color='midnightblue'
        ):
    """
    Plot regression prediction with its uncertainty
    band between lower and upper bounds
    """
    line = ax.plot(
        x, y_pred, label=label,
        linewidth=2, color=color, alpha=0.9
        )
    fill = ax.fill_between(
        x, y_lower, y_upper,
        label='Uncertainty band',
        color=color, alpha=0.2
        )
    return line, fill

def plot_uncertainty_band(
        ax, x, y_lower, y_upper,
        color='midnightblue', alpha=0.2
        ):
    """Plot uncertainty band between lower and upper bounds"""
    return ax.fill_between(
        x, y_lower, y_upper,
        label='Uncertainty band',
        alpha=alpha, color=color
    )

def save_figure(fig, title, prefix='', legend=None, dpi=300, transparent=False):
    """Save plot with standardized naming"""
    fig_name = title.replace('$','').replace('\n','').replace('\\','').replace(' ','_')
    fig_path = name2path(f'{prefix}{fig_name}', ext='.png')
    
    if legend:
        plt.savefig(
            fig_path, bbox_extra_artists=(legend,),
            bbox_inches='tight', dpi=dpi, transparent=transparent
        )
    else:
        plt.savefig(fig_path, dpi=dpi, transparent=transparent)
