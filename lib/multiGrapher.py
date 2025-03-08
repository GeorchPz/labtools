    # -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

from numpy import linspace
from pandas import read_excel

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator

from lib.xl_manager import name2path, get_data_n_uncert


def plotter(
        x_y_δx_δy_list, title, legend_title, subtitles,
        x_label, y_label, log_xscale= False, log_yscale= False
        ):
    '''Plots results'''
    
    # Font type
    font = {
            'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 14,
            }
    
    
    subtitles = subtitles if type(subtitles) == list or type(subtitles) == tuple else [subtitles]
    n = len(subtitles)
    # Plots' colours
    if n<8:
        colours = ['blue', 'orange', 'green','red','purple','cyan','pink']
        # colours = ['darkblue', 'blue', 'orange', 'red', 'darkred']
        # colours = plt.cm.seismic(linspace(0.1,0.9,n))
        markers = ['o', '^', 's', 'v', '<', '*', '>', 'x', 'd']
    else:
        colours = cm.rainbow(linspace(0, 1, n))
        markers = ['.']*n
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(9,6))
    
    # here we plot each and every points 
    for i in range(n):
        x_y, δx_δy = x_y_δx_δy_list[i]
        x, y, δx, δy = *x_y, *δx_δy        
        
        'Plotear CON errores'
        ax.errorbar(x, y, xerr= δx, yerr= δy,
                      marker= markers[i], linestyle= '', #markersize = 4, 
                      color= colours[i], ecolor= colours[i],# color si no solapan: 'dimgrey', # markerfacecolor='black',
                      capsize= 4, elinewidth= 2, label= subtitles[i])
        'Plotear sin errores'
        # ax.plot(x, y, linestyle= '-', #markersize = 4, 
        #              color= colours[i], label= subtitles[i])
    # Scale
    if log_xscale == True:
        ax.set_xscale('log')
    if log_yscale == True:
        ax.set_yscale('log')
    
    # Ticks, grid, labels and legend
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    ax.yaxis.set_minor_locator( AutoMinorLocator() )
    
    ax.grid(which='major', linestyle='-', alpha=0.6)
    # ax.grid(which='minor', linestyle='-', alpha=0.3)
    
    plt.title(title, fontdict= font, fontsize=16)
    plt.xlabel(x_label, fontdict= font)
    plt.ylabel(y_label, fontdict= font)
    plt.legend(title = legend_title, loc='best', fontsize=12)
    
    # Export plot
    fname = title.replace('$','').replace('\n','')
    plt_fname = name2path('Plot - ' + fname, ext = '.png')
    plt.savefig(plt_fname, dpi = 500, bbox_inches='tight', transparent = False)


def get_vals(x_label, y_label, files_name):
    '''Gets all necessary values from our file'''
    # Find magnitudes
    x_magn = x_label.split(' ')[0]
    y_magn = y_label.split(' ')[0]
    
    if '$' in x_magn + y_magn:
        x_magn = x_magn.replace('$','')
        y_magn = y_magn.replace('$','')
    
    # Our goal here is to export these lists of list
    x_y_δx_δy_list = []
    
    # Import data
    files_name = [files_name] if type(files_name) == str else files_name
    for fname in files_name:
        data = read_excel( name2path(fname) )
        
        # from pandas import read_csv
        # data = read_csv( name2path(fname, extension = '.csv') )
        x_y_δx_δy = get_data_n_uncert(x_magn +','+ y_magn, data)
        x_y_δx_δy_list.append(x_y_δx_δy)
    
    return x_y_δx_δy_list


def main():
    '''TOGGLEABLE DATA'''

    title = '$V_{out} (t)$ - 10Hz'
    legend_ttl = r'$\bf{Condición \; del \; termistor:}$'
    subtitles = 'más quieto possible', 'movimiento continuo', 'sobre superficie metalica'
    
    x_label = '$t$ (s)'
    y_label = '$V_{out}$ (V)'
    
    f_names = '+quiet', 'metal', 'moviment'
    f_names = [i+'_10Hz' for i in f_names]
    
    '''PROGRAM STARTER'''
    vals = get_vals(x_label, y_label, f_names)
    plotter(
        vals, title, legend_ttl, subtitles, x_label, y_label,
        log_xscale= False, log_yscale= False
        )
    plt.show()

if __name__ == '__main__':
	main()