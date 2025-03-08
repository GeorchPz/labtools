# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

from pandas import read_excel

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import sigfig

from lib.xl_manager import name2path, get_data_n_uncert

sqrt = lambda x : x**(1/2)


def lin_corr(x, y):
    '''Returns the Pearson's linear correlation coefficient'''
    N_ = x.size - 1
    # Means & stand. desviation & corariance
    xm, ym = x.mean(), y.mean()
    sx = sqrt(sum( (x-xm)**2 ) / N_)
    sy = sqrt(sum( (y-ym)**2 ) / N_)
    # Covariance
    sxy = sum( (x-xm)*(y-ym) ) / N_
    
    return sxy / (sx*sy)


def std_fit(x, y, δx, δy):
    '''Standard least square fitting to y = A + B·x, with δx,δy → const'''
    N = x.size
    Σx, Σy = sum(x), sum(y)
    Σx2 = sum(x**2)
    Σxy = sum(x*y)
    # Slope coefficients
    Δ = N*Σx2 - Σx**2
    A = ( Σx2*Σy - Σx*Σxy )/Δ
    B = ( N*Σxy - Σx*Σy )/Δ
    # Possibles σy
    σy_teo = sqrt( sum((y - A - B*x)**2) / (N-2) )
    σy_equiv = sqrt( δy**2 + (B*δx)**2 )
    σy = max(σy_equiv, σy_teo)
    # Their uncertainty
    σA = σy*sqrt( Σx2/Δ )
    σB = σy*sqrt( N/Δ )
    
    return A, B, σA, σB


def weighted_fit(x, y, δx, δy):
    '''Least square fitting, with δx,δy → not const'''
    N = x.size
    # Calculate σ with a no weighted B
    B_nw = ( N*sum(x*y) - sum(x)*sum(y) )/( N*sum(x**2) - sum(x)**2 )
    σ = sqrt( δy**2 + (B_nw*δx)**2 )
    # Weight
    w = 1 / σ**2
    # Summations
    Σw = sum(w)
    Σwx = sum(w*x)
    Σwx2 = sum(w*x**2)
    Σwy = sum(w*y)
    Σwxy = sum(w*x*y)
    # Slope coefficients
    Δ = Σw*Σwx2-Σwx**2 
    A = (Σwx2*Σwy-Σwx*Σwxy)/Δ
    B = (Σw*Σwxy-Σwx*Σwy)/Δ
    # Their uncertainty
    σA = sqrt(Σwx2/Δ)
    σB = sqrt(Σw/Δ)
    
    return A, B, σA, σB


rounder = lambda value, uncert : sigfig.round(float(value), float(uncert), cutoff = 29)
short = lambda x: str(round(x,5))

# Font type
font = {
        'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14
        }


def plotter(x, y, σx, σy, r, A, B, σA, σB, title, x_label, y_label):
    '''Prints & plots linear regression's results'''
    
    #Linear reg. text
    main_label = (
        f' \n ${y.name} = ({ rounder(B,σB) })·{x.name} + ({ rounder(A,σA) })$' +
        f' \n r = {round(r,3)}'
        ) # formated string
    
    '''TEXT'''        
    text = (
        'Fitting to y = (B ± σB)·x + (A ± σA)',
        main_label,
        '\n' + 'r  = ' + short(r),
        'B  = ' + short(B), 'σB = ' + short(σB),
        'A  = ' + short(A), 'σA = ' + short(σA),
        )

    '''FIGURE'''
    # Plot the data
    fig, ax = plt.subplots(figsize=(9,6))
    # Main slope
    ax.plot(x, A + B*x , linewidth=2, color='midnightblue', alpha=0.9, 
            label= 'Regresión lineal' + main_label)
    # Errorbars of points
    plt.errorbar(
        x, y, xerr= σx, yerr= σy, fmt='k.',
        ecolor='dimgrey', capsize=4, elinewidth=2
    )
    # Uncertainty of the slope
    x_s = x.sort_values()
    ax.fill_between(x_s, (A - σA) + (B - σB)*x_s, (A + σA) + (B + σB)*x_s, alpha=0.2,
                    label='Incertidumbre asociada')
    # Old uncertainty of the slope
    # ax.plot(x, (A + σA) + (B + σB)*x, color='firebrick', linestyle='--')
    # ax.plot(x, (A - σA) + (B - σB)*x, color='firebrick', linestyle='--',
    #          label='Incertidumbre de la pendiente')
    
    # Ticks, grid & plot's text
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    ax.yaxis.set_minor_locator( AutoMinorLocator() )
    plt.grid(which='major', linestyle='--', alpha=0.6)
    # plt.grid(which='minor', linestyle='-', alpha=0.3)
    
    plt.title(title, fontdict= font, fontsize=16)
    plt.xlabel(x_label, fontdict= font)
    plt.ylabel(y_label, fontdict= font)
    plt.legend(loc='best', labelspacing=1)
    
    '''Export'''
    fname = title.replace('$','').replace('\n','').replace('\\','')
    
    # Export plot
    plt_fname = name2path('LinReg - ' + fname.replace('$',''), ext = '.png')
    plt.savefig(plt_fname, dpi = 500, transparent = False)
    
    # Export data
    txt_fname = name2path('LinReg Data - ' + fname, ext = '.txt')
    with open(txt_fname, 'w', encoding='utf-8') as txt_file:
        # 'w' opens file in (over)writing mode
        # 'utf-8' encodes greek letters
        for i in text:
            txt_file.write(i + '\n')
            print(i)


# Check if δx & δy are numbers
isconst = lambda var : isinstance(var, (float,int)) or len ( set(var) ) == 1


def get_vals_Lr(x_label, y_label, file_name):
    '''Gets all necessary values from our file and its linear regression'''
    # Find magnitudes
    x_magn = x_label.split(' ')[0]
    y_magn = y_label.split(' ')[0]
    
    if '$' in x_magn + y_magn:
        x_magn = x_magn.replace('$','')
        y_magn = y_magn.replace('$','')
    
    # Import data
    data = read_excel( name2path(file_name) )
    x_y, δx_δy = get_data_n_uncert(x_magn +','+ y_magn, data)
    x, y, δx, δy = *x_y, *δx_δy
    
    '''Data analysis'''
    r = lin_corr(x, y)
    # Get linear reg values: lr_vals = (A, B, σA, σB)
    if isconst(δx) and isconst(δy):
        lr_vals = std_fit(x, y, δx, δy)
    else:
        lr_vals = weighted_fit(x, y, δx, δy)
    
    return (x, y, δx, δy, r, *lr_vals)

def main():
    '''TOGGLEABLE DATA'''
    # title   = 'ΔL vs ΔT PRUEBAA'
    # x_label = 'ΔT \; (ºK)'
    # y_label = 'ΔL \; (mm)'
    # filename = 'datos_aluminio'
    
    title = '$n$ vs $λ^{-2}$'
    x_label = '$λ^{-2}$ \; ($nm^{-2}$)'
    y_label = 'n'
    filename = 'espectro_Hg_©'
    
    '''PROGRAM STARTER'''
    vals = get_vals_Lr(x_label, y_label, filename)
    plotter(*vals, title, x_label, y_label)
    plt.show()


if __name__ == '__main__':
	main()