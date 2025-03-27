# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 23:44:02 2021

@author: Jorge Pottiez López-Jurado
"""

def manager(title, legend_ttl, subtitles, x_label, y_label, files_name, Mode):
    '''Centralizes al necessary progs'''
    files_name = [files_name] if type(files_name) == str else files_name
    n = len(files_name)
    
    if Mode == 'Linreg' and n == 1:
        from analysis.linear_regression import get_vals_Lr, plotter
        
        vals = get_vals_Lr(x_label, y_label, files_name[0])
        return plotter(*vals, title, x_label, y_label)
    
    elif Mode == 'Linreg' and n > 1:
        from lib.multiLinreg import get_vals_Lr, multi_plotter
        
        vals_list = [get_vals_Lr(x_label, y_label, f_name) for f_name in files_name]
        return multi_plotter(vals_list, title, legend_ttl, subtitles, x_label, y_label)    
    
    elif Mode == 'Plot':
        from lib.multiGrapher import get_vals, plotter
        
        vals = get_vals(x_label, y_label, files_name)
        plotter(vals, title, legend_ttl, subtitles, x_label, y_label,
                log_xscale= False, log_yscale= False)
    
    else:
        raise NameError(f'{Mode} is not a supported mode yet')
    
    # plt.show()

    
def main():
    '''TOGGLEABLE DATA'''
    # Num:     0         1
    Mode = ['Linreg', 'Plot'][1]
    
    # title = '$ρ_{rel}$ vs $T$'#' - rango [-1ºC, 4ºC]'
    # legend_ttl = None
    # subtitles = None
    # x_label = 'T (ºC)'
    # y_label = '$ρ_{rel}$' #r'$ρ_{rel}$ = $\frac{ρ(T)}{ρ_{0ºC}$'
    # f_names = 'p6_densidad_©'#'_small_range'
    
    title = 'v(r⁻¹)'
    legend_ttl = None
    subtitles = 'Sin Tapón', 'Sumidero Grande', 'Sumidero Mediano'
    y_label = 'v (cm/s)'
    x_label = 'r⁻¹ (cm⁻¹)'
    f_names = 'p3_v_sin_tap_©', 'p3_v_sum_g_©', 'p3_v_sum_m_©'
    
    '''Pract'''
    title = 'EM_3__cond'
    legend_ttl = None
    subtitles = None
    y_label = 'ρ ($\Omega m$)'
    x_label = '$T-T_0$ (K)'
    f_names = 'EM_3__cond'
    
        
    '''PROGRAM STARTER'''
    manager(title, legend_ttl, subtitles, x_label, y_label, f_names, Mode)

if __name__ == '__main__':
	main()