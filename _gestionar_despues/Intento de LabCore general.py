# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:44:02 2021

@author: Jorge Pottiez López-Jurado
"""

    
def manager(variables, equation, file_name, title, subtitles, x_label, y_label, files_name, comp_vals, Mode):
    '''Centralizes al necessary progs'''
    files_name = [files_name] if type(files_name) == str else files_name
    n = len(files_name)
    
    
    if Mode == 'Tables':
        from tables_calc import central
        
        return central(variables, equation, file_name)
    
    elif Mode == 'Linreg' and n == 1:
        from Linreg import get_vals_Lr, plotter
        
        vals = get_vals_Lr(x_label, y_label, files_name[0])
        return plotter(*vals, title, x_label, y_label)
    
    
    elif Mode == 'Linreg' and n > 1:
        from multiLinreg import get_vals_Lr, multi_plotter
        
        vals_list = [get_vals_Lr(x_label, y_label, f_name) for f_name in files_name]
        return multi_plotter(vals_list, title, subtitles, x_label, y_label)
    
    
    elif Mode == 'Simple Plot':
        from multiGrapher import get_vals, plotter
        
        vals = get_vals(x_label, y_label, files_name)
        plotter(vals, title, subtitles, x_label, y_label,
                log_xscale= False, log_yscale= False)
    
    
    elif Mode == 'Comparator':
        from comparator import results_comparator
        
        labels_str = ','.join(str(sbttl) for sbttl in subtitles)
        results_comparator(comp_vals, title, x_label, labels_str,
                           shared_x_axis = True)
    
    
    else:
        raise NameError(f'{Mode} is not a supported mode yet')
    
    # plt.show()

    
def main():
    '''TOGGLEABLE DATA'''
    # Num:     0         1            2             3
    Mode = ['Tables', 'Linreg', 'Simple Plot', 'Comparator'][0]
    
    '''0º Mode'''
    var = 'η,r,R'
    eq = 'η_{Faxen} = η*(1 -2.104*r/R +2.09*(r/R)**3 -0.95*(r/R)**5)'
    f_name = 'new_visc_S_-_ΔΤ_4ºmedida'
    
    
    '''1º & 2º Mode'''
    title = 'Viscosidad dinamica en función de la Temperatura'
    subtitles = '1º estimación','Ladenburg', 'Faxen'
    
    x_label = 'T \; (ºC)'
    y_label = 'η \; (g·cm^{-1}·s^{-1})'
    f_names = 'ΔT_1º_estim', 'ΔT_Ladenburg', 'ΔT_Faxen'
    
    '''3º Mode'''
    comp_vals = [
        '12.4 ± 0.4, 14.9',
        '11.7 ± 0.4, 14.9',
        '11.7 ± 0.4, 14.9'
        ]
        
    '''PROGRAM STARTER'''
    manager(var, eq, f_name,
            title, subtitles, x_label, y_label, f_names,
            comp_vals, Mode)

if __name__ == '__main__':
	main()