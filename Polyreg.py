  # -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

'''Same as in Linreg'''
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from pandas import read_excel

import sigfig
from lib.xl_manager import name2path, get_data_n_uncert

rounder = lambda value, uncert : sigfig.round(float(value), float(uncert), cutoff = 29)
short = lambda x: str(round(x,5))

font = {
        'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14
        }
'''-- Until here'''

import numpy as np
import pandas as pd
from lib.xl_editor import xl_enhancer

def get_exp_vals(x_label, y_label, filename):
    # Find magnitudes
    x_magn = x_label.split(' ')[0].replace('$','')
    y_magn = y_label.split(' ')[0].replace('$','')
    
    # Import data
    data = read_excel( name2path(filename) )
    (x,y), (δx,δy) = get_data_n_uncert(x_magn +','+ y_magn, data)
    
    return x, y, δx, δy

def poly_reg(x, y, degree):
    '''Gives two lists: the coefficient and its uncertainty from higher exponent to lower'''
    coefs, cov = np.polyfit(x, y, degree, cov=True)
    # Error (determinated by the diagonal of the covarience matrix)
    err = np.sqrt(np.diag(cov))
    
    # print(coefs, err)
    return coefs, err

def plotter(x, y, σx, σy, coefs, err, form, title, x_label, y_label, filename):
    '''Plots linear regression's results'''
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(9,6))
    # Main slope
    # Errorbars of points
    plt.errorbar(
        x, y, xerr= σx, yerr= σy, fmt='k.',
        ecolor='dimgrey', capsize=4, elinewidth=2
        )
    
    x_line = np.linspace(min(x), max(x), 100)
    
    poly_model = np.poly1d(coefs)
    poly_model_p = np.poly1d(coefs + err)
    poly_model_m = np.poly1d(coefs - err)
    
    print(format(poly_model))
    # Regression
    plt.plot(
        x_line, poly_model(x_line), linewidth=2, color='midnightblue', alpha=0.9, 
        label= 'Regresión polinómica:' + f'\n${form}$'
        )
    # Uncertainty of the regression
    ax.fill_between(
        x_line, poly_model_m(x_line), poly_model_p(x_line), alpha=0.2,
        label='Incertidumbre asociada'
        )
    
    # Ticks, grid & plot's text
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    ax.yaxis.set_minor_locator( AutoMinorLocator() )
    plt.grid(which='major', linestyle='--', alpha=0.6)
    # plt.grid(which='minor', linestyle='-', alpha=0.3)
    
    plt.title(title, fontdict= font, fontsize= 16)
    plt.xlabel(x_label, fontdict= font)
    plt.ylabel(y_label, fontdict= font)
    plt.legend(loc='best', labelspacing= 1)
    
    # Export
    plot_name = name2path(filename + '_PolyReg', ext = '.png')
    plt.savefig(plot_name, dpi = 500, transparent = False)


def exceler(x, y, coefs, err, roundlist, form, filename):
    'Transfers data to excel'
    
    abc = ['A','B','C','D','E','F','G']
    n = len(coefs)
    
    # Cutting abc list and inverting it : if n=2 -> [B,A]
    cba = abc[:n][::-1]
    
    # List of monomials
    monos = [f'{ cba[i] }·{x.name}^{ i }' for i in range(len(coefs))]
    # String of the type: y(x) = (A ± σA) + (B ± σB)·x ...
    poly_type = f'{y.name}({x.name}) = ' + ' + '.join( monos[::-1] )
    poly_type = poly_type.replace(f'·{x.name}^0','').replace('^1','')
    
    # we change the index so that we dont transpose the usual 0,1,2 column
    df = pd.DataFrame({
            'Round'    : roundlist,
            'Monomial' : monos[::-1],
            'Values'   : coefs,
            'Errors'   : err
                        }, index= abc[:n])
    
    df = df.transpose()
    df.index.name = poly_type
    
    path  = name2path(filename + '_PolyReg_Data')
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer)
    writer.save()

    # Make it pretty ;)
    xl_enhancer(path)


def central(title, x_label, y_label, filename, degree):
    '''PROGRAM STARTER'''
    x, y, δx, δy = get_exp_vals(x_label, y_label, filename)
    
    coefs, err = poly_reg(x, y, degree)
    
    roundlist = [ rounder(p,e) for p,e in zip(coefs, err) ]
    monomials = [ f'({ s })·{x.name}^{ i }' for i, s in enumerate(roundlist[::-1])] [::-1]
    
    # Formula
    form = f'{y.name}({x.name}) = ' + ' + '.join( monomials )
    form = form.replace(f'·{x.name}^0','').replace('^1','')
    
    
    plotter(x, y, δx, δy, coefs, err, form, title, x_label, y_label, filename)
    exceler(x, y, coefs, err, roundlist, form, filename)


def main():
    '''TOGGLEABLE DATA'''
    # title = '$n$ vs $λ^{-2}$'
    # x_label = '$λ^{-2}$ \; ($nm^{-2}$)'
    # y_label = 'n'
    # filename = 'espectro_Hg_©'
    
    titles = ['Amarillo', 'Azul', 'Verde', 'Violeta 1', 'Violeta 2']
    x_lab = '$I$ (%)'
    y_lab = '$V$ (V)'
    files = ['Amarillo', 'Azul', 'Verde', 'Violeta 1', 'Violeta 2']
    degree = 3
    
    if type(titles) == str:
        central(titles, x_lab, y_lab, files, degree)
    else:
        for title, file in zip(titles, files):
            central(title, x_lab, y_lab, file, degree)

if __name__ == '__main__':
	main()