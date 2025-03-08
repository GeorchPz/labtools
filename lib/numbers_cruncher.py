# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 00:45:38 2023

@author: Jorge Pottiez López-Jurado
"""

import sigfig

def isNaN(num):
    # https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
    return num != num

def rounder(value, uncert):
    '''
    Rounds single values: 3.39 ± 0.44 → 3.4 ± 0.5
        - Normal rounding cut-off, add: cutoff = 29
        - Possible change in notation, add: notation = 'sci'
    '''
    # print('val:',type(value), '\t unc:',uncert)
    
    if not isNaN(value):
        r = sigfig.round(value, uncert, cutoff=29)
    else:
        r = 'nan ± nan'
    
    return r

def arr_rounder(value_arr, uncert_arr): 
    'Rounds arrays'
    return list(map(rounder, value_arr, uncert_arr))


'Basic formulas for mean & its uncertainty'
sqrt = lambda x : x**(1/2)
# Standard mean & its error
m  = lambda x  : sum(x) / len(x)
δm = lambda δx : sqrt(sum(δx**2)) / len(δx)
# Weighted mean formulas
w   = lambda δx   : 1/(δx**2)
wm  = lambda x,δx : sum(x*w(δx)) / sum(w(δx))
δwm = lambda δx   : 1 / sqrt(sum(w(δx)))


def rel_un(rounded_str):
    'Return relative uncertainty from string "0.39 ± 0.44"'
    x, δx = ( float(i) for i in rounded_str.split(' ± ') )
    return str(round(δx/x*100, 2)) + '%'

def mean_n_relat_uncert(name, f, δf):
    '''Calculates various types of means'''
    # Rounded values of means
    str_m  = rounder(m(f), δm(δf))
    str_wm = rounder(wm(f, δf), δwm(δf))
    # Relative uncerts
    ι_m  = rel_un(str_m)
    ι_wm = rel_un(str_wm)
    
    return {
        '':                 (name,''),
        'Type':             (' Standard ', ' Weighted '),
        'Mean (m)':         (str_m, str_wm),
        'Rel. Uncert. (ι)': (ι_m, ι_wm),
    }