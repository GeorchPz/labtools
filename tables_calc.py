# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:07:42 2020

@author: Jorge Pottiez López-Jurado
"""

import pandas as pd

# import lib.symb_manager as sy_man

from lib.xl_editor        import xl_enhancer
from lib.symb_manager     import f_n_δf_form, f_n_δf_lambdif, forms_exporter
from lib.xl_manager       import name2path, get_data_n_uncert
from lib.numbers_cruncher import arr_rounder, mean_n_relat_uncert


def data_framer(vars_str, eq_str_list, data, vars_dep):
    '''Calculates the output values of a formula for given arrays'''
    
    data_to_concat = []
    
    f_data, δf_data = get_data_n_uncert(vars_str, data)
    
    print(δf_data)
    
    for eq_str in eq_str_list:
        
        f_str, expr_str = eq_str.split('=')
        δf_str          = 'δ' + f_str
        
        # Calculates: f_sy, δf_sy
        formulas_sy = f_n_δf_form(vars_str, expr_str, vars_dep) 
        f_lamb, δf_lamb = f_n_δf_lambdif(vars_str, *formulas_sy)
        # (*args : allows the array to be unpacked)
        
        # print(f_data)
        f_arr  =  f_lamb(*f_data)
        δf_arr = δf_lamb(*f_data, *δf_data)
        
        ### 1st dataframe
        data[f_str + ' (UNITS)'] = f_arr
        data[δf_str]             = δf_arr
        data[f_str + ' ± ' + δf_str] = arr_rounder(f_arr, δf_arr)
        
        ### 2nd dataframe
        formulas_str = (f_str, δf_str)
        # Pretty-printing & returns the latex form of the formulas f & δf
        formulas_ltx = forms_exporter(formulas_str, formulas_sy)
        # Mean & relative uncertainty of f ± δf
        mean_n_ι_data = pd.DataFrame(
                            mean_n_relat_uncert(f_str, f_arr, δf_arr)
                                    )
        
        latex_formulas = pd.DataFrame( {'LaTeX Formulas': formulas_ltx} )
        
        f_misc_data = pd.concat([mean_n_ι_data, latex_formulas], axis='columns')
        
        data_to_concat.append(f_misc_data)
        
    misc_data = pd.concat(data_to_concat, axis='index')
    print('\n', misc_data.drop(columns=['LaTeX Formulas']))
    
    return data, misc_data


def save_df(filename, computed_data, misc_data):
    '''Exports dataframes to excel'''
    final_path = name2path(filename + '_©')
    writer = pd.ExcelWriter(final_path, engine='xlsxwriter')

    computed_data.to_excel(writer, index=False, sheet_name='Calc table')

    misc_data.to_excel(writer, index=False, sheet_name='Misc')
    writer.save()

    # Make it pretty ;)
    xl_enhancer(final_path)


def texter(vars_str, eq_str_list, vars_dep):
    '''
    Gives us the needed formulas (& pretty prints them)
    when we are not interested in aplying them to an excel
    '''
    # Lists of all: names & LaTeX formulas
    vars_calc, formulas_ltx  = [], []
    
    for eq_str in eq_str_list:
        f_str, expr_str = eq_str.split('=')
        
        formulas_str = (f_str, 'δ' + f_str)
        
        # Calculates: f_sy, δf_sy
        formulas_sy = f_n_δf_form(vars_str, expr_str, vars_dep) 
    
        # Pretty-printing & returns the latex form of the formulas
        f_n_δf_ltx = forms_exporter(formulas_str, formulas_sy)
        print('\n')
        
        vars_calc.append(f_str)
        formulas_ltx.extend(f_n_δf_ltx)
    
    
    ##### A partir de aqui es exclusivo de filename == ''
    
    name = f'LaTeX___{ vars_calc[-1] }({vars_str})'
    path = name2path(name , ext= '.txt')
        
    txt_file = open(path, 'w', encoding='utf-8')
    # 'w' opens file in writing mode
    # 'utf-8' encodes greek letters
    
    for i in formulas_ltx:
        print(i)
        txt_file.write(i + '\n')
    txt_file.close()
    


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


if __name__ == '__main__':
	main()

# Vals Aire

# ν = 1.3·E-5 m²/s
# ρ = 1.29 Kg/m³.
