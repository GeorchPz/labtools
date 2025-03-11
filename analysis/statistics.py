import numpy as np
from ..uncertainties.format import isiterable, round_with_uncertainty

'Basic statistics functions with uncertainties'
# Standard mean & its error
mean  = lambda x  : np.mean(x)
δmean = lambda δx : np.sqrt(np.sum(δx**2)) / len(δx)
# Weighted mean formulas
w = lambda δx : 1/(δx**2)
mean_weighted  = lambda x,δx : np.sum(x*w(δx)) / np.sum(w(δx))
δmean_weighted = lambda δx   : 1 / np.sqrt(np.sum(w(δx)))
# Standard deviation & its error
std  = lambda x  : np.std(x)
std_weighted  = lambda x,δx : (
    np.sqrt(np.sum(w(δx)*(x - mean_weighted(x,δx))**2) / np.sum(w(δx)))
)

def relative_uncertainty(x, δx):
    """
    Calculate relative(s) uncertainty(ies) as a percentage.
    
    Parameters:
        - x : float or array-like, value(s)
        - δx : float or array-like, uncertainty(ies)
    Returns:
        - str or list : Formatted string(s) "xx.xx %"
    """
    if isiterable(x):
        rel_uncertainties = [ relative_uncertainty(xi, δxi) for xi, δxi in zip(x, δx) ]
        return [ relative_uncertainty(xi, δxi) for xi, δxi in zip(x, δx) ]
    else:
        if x == 0:
            return "∞ %" if δx != 0 else "0.00 %"
        else:
            return f"{abs(δx/x)*100:.2f} %"

def relative_error(x_obs, x_exp):
    '''
    Calculate relative error(s) as a percentage.
    
    Parameters:
        - x_obs : float or array-like, observed value(s)
        - x_exp : float or array-like, expected value(s)
    Returns:
        - str or list : Formatted string(s) "xx.xx %"
    '''
    if isiterable(x_obs) and isiterable(x_exp):
        return [ relative_error(xi, xei) for xi, xei in zip(x_obs, x_exp) ]
    else:
        return f"{ abs( (x_obs - x_exp) / x_exp )*100 :.2f} %"

def relative_uncertainty_from_string(rounded_str):
    '''
    Calculate relative uncertainty from a formatted "value ± uncertainty" string.
    
    Parameters:
        - rounded_str : str
    Returns:
        - str : Relative uncertainty as a percentage
    '''
    x, δx = ( float(i) for i in rounded_str.split(' ± ') )
    return relative_uncertainty(x, δx)

def calculate_statistics(names, x, δx, x_exp = None):
    '''
    Calculate statistics for a given set of values:
    Mean(s), standard deviation(s), relative uncertainty(ies),
    and relative error(s) (if expected value(s) provided).

    Parameters:
        - names : str or list, name(s) or symbol(s) of the variable(s)
        - x : array-like or matrix-like, value(s)
        - δx : array-like or matrix-like, uncertainty(ies)
        - x_exp : float or array-like, expected value(s) (default: None)
    Returns:
        - dict :
            - Name : str or list, name(s) or symbol(s)
            - (Standard, Weighted) : dicts, statistics:
                - Mean : str or list, formatted mean(s)
                - Std : float or list, standard deviation(s)
                - Rel Uncert : str or list, relative uncertainty(ies)
                - Rel Error : str or list, relative error(s) (if x_exp provided)
    '''
    if not isiterable(names):
        m = mean(x)
        δm = δmean(δx)
    else:
        m = [ mean(xi) for xi in x ]
        δm = [ δmean(δxi) for δxi in δx ]
    stats_std = {
        'Mean': round_with_uncertainty(m, δm),
        'Std' : std(x),
        'Rel Uncert': relative_uncertainty(m, δm)
    }
    if x_exp:
        stats_std['Rel Error'] = relative_error(m, x_exp)
    
    m_w = mean_weighted(x, δx)
    δm_w = δmean_weighted(δx)
    stats_w = {
        'Mean': round_with_uncertainty(m_w, δm_w),
        'Std' : std_weighted(x, δx),
        'Rel Uncert': relative_uncertainty(m_w, δm_w)
    }
    if x_exp:
        stats_w['Rel Error'] = relative_error(m_w, x_exp)

    return {
        'Name': names,
        'Standard': stats_std,
        'Weighted': stats_w
        }