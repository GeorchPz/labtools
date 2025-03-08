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
from lib.files_manager import name2path, get_data_n_uncert

rounder = lambda value, uncert : sigfig.round(float(value), float(uncert), cutoff = 29)

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


def Reg(x, y, δx, δy, function, fit_type):
    '''
    fit_type{0, 1, 2} int
        0 -> explicit ODR (Orthogonal distance regression )
        (1 -> implicit ODR)
        2 -> ordinary least-squares
    
    Correct fitting with scipy curve_fit including errors in x?
    https://stackoverflow.com/questions/26058792/correct-fitting-with-scipy-curve-fit-including-errors-in-x
    '''
    from scipy.odr import ODR, Model, RealData
    
    data = RealData(x, y, δx, δy)
    model = Model(function)

    odr = ODR(data, model, beta0 = [1,1])
    odr.set_job(fit_type = fit_type)
    output = odr.run()
    
    beta, err_beta = output.beta, output.sd_beta
    
    return beta, err_beta

def plotter(x, y, σx, σy, func, coefs, err, str_form, str_func_w_vals, title, x_label, y_label, filename):
    '''Plots linear regression's results'''
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(9,6))
    # Main slope
    # Errorbars of points
    plt.errorbar(
        x, y, xerr= σx, yerr= σy, fmt='k.',
        ecolor='dimgrey', capsize=4, elinewidth=2
        )
    
    n = 100
    xn = np.linspace(min(x), max(x), n)
    yn = func(coefs, xn)
    yn_p = func(coefs + err, xn)
    yn_m = func(coefs - err, xn)
    
    # print(format(poly_model))
    
    # Regression
    plt.plot(
        xn, yn, linewidth=2, color='midnightblue', alpha=0.9, 
        label= 'Regresión:' + f'\n${str_func_w_vals}$'
        )
    # Uncertainty of the regression
    ax.fill_between(
        xn, yn_m, yn_p, alpha=0.2, label='Incertidumbre asociada'
        )
    # Ticks, grid & plot's text
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    ax.yaxis.set_minor_locator( AutoMinorLocator() )
    plt.grid(which='major', linestyle='--', alpha=0.6)
    # plt.grid(which='minor', linestyle='-', alpha=0.3)
    # Texts
    plt.title(title, fontdict= font, fontsize= 16)
    plt.xlabel(x_label, fontdict= font)
    plt.ylabel(y_label, fontdict= font)
    plt.legend(loc='best', labelspacing= 1)
    
    # Export
    plot_name = name2path(filename + '__PolyReg'.replace(' ', '_'), ext = '.png')
    plt.savefig(plot_name, dpi = 500, transparent = False)



def central(title, x_label, y_label, str_coefs, str_func, function, fit_type, filename):
    '''PROGRAM STARTER'''
    x, y, δx, δy = get_exp_vals(x_label, y_label, filename)
    
    coefs, err = Reg(x, y, δx, δy, function, fit_type)
    round_coefs = [ rounder(p,e) for p,e in zip(coefs, err) ]
    
    
    # mapping : [ ('A', 1.01), ('B', 2.001), ('C', 3.1) ...]
    mapping = zip(str_coefs.split(','), round_coefs)
    
    str_func_w_vals = str_func
    for sym, val in mapping:
        print(sym, val)
        str_func_w_vals = str_func_w_vals.replace(sym, '('+ val +')')
    
    print(str_func_w_vals)
    
    plotter(x, y, δx, δy, function, coefs, err, str_func, str_func_w_vals, title, x_label, y_label, filename)
    # do an exceler()


def main():
    '''TOGGLEABLE DATA'''
    # title = '$n$ vs $λ^{-2}$'
    # x_label = '$λ^{-2}$ \; ($nm^{-2}$)'
    # y_label = 'n'
    # filename = 'espectro_Hg_©'
    
    title = 'Diferencia de tensión superficial\n vs \nconcentración en volumen de etanol'
    x_lab = 'C (%)'
    y_lab = '$σ_0-σ$ (N/m)'
    fname = 'Flu1_©'
    
    str_coefs = 'α,β'
    str_func  = 'σ_0-σ = α·ln(1 + β·C)'
    
    def func(beta, x):
        a, b = beta
        y = a * np.log(1 + b*x)
        return y
    
    fit_type = 0
    central(title, x_lab, y_lab, str_coefs, str_func, func, fit_type, fname)


if __name__ == '__main__':
	main()