# -*- coding: utf-8 -*-
"""
Created on Thu May 25 13:48:32 2023

@author: Jorge Pottiez López-Jurado
"""

import numpy as np
import pandas as pd
import sigfig
from lib.xl_manager import get_data_n_uncert
from lib.xl_editor  import xl_enhancer


def isNaN(num):
    # https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
    return num != num


def rounder(value, uncert):
    '''
    Rounds sigle values: 3.39 ± 0.44 → 3.4 ± 0.5
        - Normal rounding cut-off, add: cutoff = 29
        - Possible change in notation, add: notation = 'sci'
    '''
    # print('val:',type(value), '\t unc:',uncert)
    
    if not isNaN(value):
        r = sigfig.round(value, uncert, cutoff=29)
    else:
        print(
            "There's probably a problem with a column, since:",
            f"{value} ± {uncert}"
            )
        r = 'nan ± nan'
    
    return r


def arr_rounder(value_arr, uncert_arr): 
    'Rounds arrays'
    return list(map(rounder, value_arr, uncert_arr))


'Defs'
sqrt = lambda x : x**(1/2)
# Standard mean & its error
m  = lambda x  : sum(x) / len(x)
δm = lambda δx : sqrt(sum(np.array(δx)**2)) / len(δx)
# Weighted mean formulas
w   = lambda δx   : 1/(np.array(δx)**2)
wm  = lambda x,δx : sum(x*w(δx)) / sum(w(δx))
δwm = lambda δx   : 1 / sqrt(sum(w(δx)))



fold = r"C:\Users\jorge\OneDrive\Programas_py\Lab_programs\Lab_data"
path = fold + '\\' + "LinRegs_Data_©.xlsx"

vars_str = 'τ_1, τ_2'

df = pd.read_excel(path)

x1 = abs(df['τ_1 (s)'])
x2 = df['τ_2 (s)']
e1 = df['δτ_1']
e2 = df['δτ_2']

# Tuples
x_t = list(zip(x1,x2))
e_t = list(zip(e1,e2))

mean  = [ m(l) for l in x_t]
err_m = [ δm(l) for l in e_t]

wmean  = [ wm(l,m) for l,m in zip(x_t, e_t)]
err_wm = [ δwm(l) for l in e_t]


df['τ_m']   = arr_rounder(mean, err_m)
df['τ_wm']  = arr_rounder(wmean, err_wm)

# print( df.iloc[:,-2:] )

new_path = fold + '\\' + "LinRegs_Data_©_means.xlsx"

df.to_excel(new_path, index = False)

xl_enhancer(new_path)

