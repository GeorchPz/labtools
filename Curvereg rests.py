# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

import numpy as np
from pandas import read_excel

from analysis.linear_regression import rounder

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