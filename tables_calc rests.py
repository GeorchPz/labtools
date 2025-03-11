# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:07:42 2020

@author: Jorge Pottiez López-Jurado
"""

import pandas as pd

# import lib.symb_manager as sy_man

from data.extract_data       import name2path


def central(variables, equations, filenames, vars_dep):
    '''Pretty prints formulas & calculations + '''
    vars_str    = variables.replace(' ', '')
    file_list   = filenames.replace(' ', '').split(',')
    eq_list     = equations.replace(' ', '').split(',')
    
    if file_list != ['']:
        for filename in file_list:
            print('','-'*50, ' '*20 + filename, '-'*50,'', sep='\n')
            raw_data = pd.read_excel(name2path(filename), sheet_name= 0)
            # Computing thing
            computed_data, misc_data = data_framer(vars_str, eq_list, raw_data, vars_dep)
            # Save xl
            save_df(filename, computed_data, misc_data)
    
    else: # if file_list == [''] (empty list)
        texter(vars_str, eq_list, vars_dep)
        pass

def main():
    '''Toggleable data'''
    '''
    Notes:  - files : list of filenames (without the .xlsx extention)
            - _©    : watermark added to final .xlsx filename
            - eq    : given an Equation f = f(x,y,...)
            - vars  : variables {x,y,...}, in general they're measured values
                    if there are n>1 eqs, vars is the union set of all vars
            - DEP   : Variables dependency between x & y ...
            
            - files == True : gives file of equation
    '''
    
    # Num:      0             1
    DEP = ['Dependent', 'Independent'][0]
    
    # var     = 'r, v' # tb funciona con 'r,a,v'
    # eqs     = 'r⁻¹ = 1/r, v⁻¹ = 1/v'
    # files   = 'p3_v_sin_tap, p3_v_sum_g' #, 'p3_v_sum_m'

    var     = 'A, B, ΔΩ'
    eqs     = 'τ_1 = - exp(A)/(ΔΩ*2*pi), τ_2 = -1/B'
    files   = 'LinRegs_Data'

    var     = 'h,e,B'
    eqs     = 'phi_0 = h/e*B'
    files   = ''    
    
    central(var, eqs, files, DEP)