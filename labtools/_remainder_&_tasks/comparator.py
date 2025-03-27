# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 20:44:31 2021

@author: jorge
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from data.extract_data import name2path

# Font type
font = {
        'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 12
        }

def old_results_comparator(val_labels, vals, vals_uncert, expected_vals, title, x_label):
    '''Allows you to see if a defined value is wwithin a certain range'''

    length = 5/4*(len(val_labels) + 1)
    
    fig, ax = plt.subplots(figsize=(4/3*length, length))
    # fig, ax = plt.subplots()
    
    plt.errorbar(
        vals, val_labels, xerr= vals_uncert,
        marker= 'o', linestyle= '', color= 'blue', ecolor= 'dimgray',
        capsize= 6, elinewidth= 2.5, label= 'Valores experimentales'
        )
    
    plt.plot(
        expected_vals, val_labels,
        marker= '|', linestyle= '', color= 'red',
        markersize = 20, label= 'Valores tabulados'
        )
    
    # Ticks, grid and legend
    ax.set_yticklabels(val_labels, fontdict= font)
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    plt.grid(which='major', axis='x', linestyle='-', alpha=0.6)
    
    plt.title(title, fontdict= font, fontsize=16)
    plt.xlabel(x_label, fontdict= font)
    plt.legend(loc='best', fancybox=True, framealpha=1, shadow=True)
    
    # Export plot
    plot_name = name2path('Comparator - ' + title, extension = '.png')
    plt.savefig(plot_name, dpi = 500, transparent = False)


def results_comparator(vals, title, x_label, labels_str, shared_x_axis):
    '''Allows you to see if a defined value is wwithin a certain range'''
    
    labels = labels_str.replace(' ','').split(',')
    
    def get_vals(vals_str):
        '''Separates string in a 3 array va'''
        vals_list = vals_str.replace(' ','').replace('±',',').split(',')
        exp_val, uncert, expected_val = [float(i) for i in vals_list]
        return exp_val, uncert, expected_val
    
    n = len(vals)
    
    if n > 1:
        fig, axs = plt.subplots(n, sharex= shared_x_axis, figsize=(2*n- 2, n ))
        
        for i in range( n ):
            observ_val, uncert, expected_val = get_vals(vals[i])
            '''Text'''
            textstr = '\n'.join((
                'ε = ' + rel_err(observ_val, expected_val),
                'ι = ' + rel_un(observ_val, uncert)
                ))
            '''Plot'''
            axs[i].set_yticks( [1] )
            axs[i].set_yticklabels([labels[i]], fontdict= font)
            axs[i].errorbar(observ_val, 1, xerr= uncert,
                            marker= 'o', linestyle= '', color= 'blue',
                            ecolor= 'gray',
                            capsize= 6, elinewidth= 2)
            axs[i].plot(expected_val, 1, markersize = 20,
                        marker= '|', linestyle= '', color= 'red')
            
            # Ticks and grid
            axs[i].xaxis.set_minor_locator( AutoMinorLocator() )
            axs[i].grid(which='major', axis='x', linestyle='-', alpha=0.6)
            axs[i].text(1.02, 0.95, textstr,
                        transform=axs[i].transAxes, fontdict= font,
                        verticalalignment='top')
            # (bbox_to_anchor= (0, -0.12,1,0), loc= 'upper left',
            #         ncol= 2, mode= "expand", labelspacing= 1, borderaxespad= 0.,
            #         fontsize= 12)

        ttl_ycoord = 1.02
        txt = plt.text(
            1.03, -1.25, 'ε: Error relativo \nι: Incertidumbre \n relativa',
            fontdict= font, transform=axs[-1].transAxes
            )
    
    else:
        fig, ax = plt.subplots(sharex= shared_x_axis, figsize=(10, 1 ))
        
        observ_val, uncert, expected_val = get_vals(vals[0])
        
        '''Text'''
        textstr = '\n'.join((
            'Error relativo: \nε = ' + rel_err(observ_val, expected_val),
            'Incertidumbre relativa: \nι = ' + rel_un(observ_val, uncert)
            ))
        '''Plot'''
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.errorbar(
            observ_val, 1, xerr= uncert,
            marker= 'o', linestyle= '', color= 'blue',
            ecolor= 'gray', capsize= 6, elinewidth= 2
            )
        ax.plot(
            expected_val, 1, markersize= 20,
            marker= '|', linestyle= '', color= 'red'
            )
                    
        # Ticks and grid
        ax.xaxis.set_minor_locator( AutoMinorLocator() )
        ax.grid(which= 'major', axis= 'x', linestyle= '-', alpha= 0.6)
        ax.text(1.03, 0.95, textstr,
                    transform=ax.transAxes, fontdict= font,
                    verticalalignment='top')
        
        ttl_ycoord = 1.2
        # A fix to be able to save ε & ι in the png image
        txt = plt.text(
            1.02, -1, '     '*8, fontdict= font, transform=ax.transAxes
            )
    
    # Label, Title and legend
    plt.xlabel('$' + x_label + '$', fontdict= font, fontsize= 14)
    # ttl = plt.suptitle('Contraste de Resultados - ' + title,
    #                    fontdict= font, fontsize= 16, y= ttl_ycoord)
    lgd = plt.legend(
        ['Valor tabulado', 'Valor experimental'], framealpha= 0,
        bbox_to_anchor=(0, -0.45,1,0), loc='upper left',
        ncol=2, mode="expand", borderaxespad=0.
        )
    
    # Export plot
    plot_name = name2path('Comparator - ' + title, ext = '.png')
    plt.savefig(
        plot_name, bbox_extra_artists= (lgd, txt), #(ttl, lgd, txt),
        bbox_inches='tight', dpi = 500, transparent = False
        )


def main():
    '''TOGGLEABLE DATA'''
    # title = 'Densidad de las esferas'
    # x_label = '$ρ \; (g·cm^{3})$'
    # shared_x_axis = True
    
    # # Results
    # val_labels = ''
    # vals = 7.9
    # vals_uncert = 1.1
    # # Tabulated results
    # expected_vals = 7.86
    
    title = ''
    x_label = 'S \; (mm²)'
    labels_str = ', '.join(['$S_{'+ str(i+1) + '}$' for i in range(6) ])
    shared_x_axis = True
    
    """
    set vals as:
        - [ 'observ_val, uncert, expected_val, ...]
        or
        - [observ_val ± uncert, expected_val, ...]
    """

    
    vals = [
            '71 ± 6, 78.5',
            '79 ± 6, 88.2',
            '97 ± 8, 98.5',
            '128 ± 12, 122.7',
            '210 ± 30, 174.4',
            '280 ± 60, 490.9'
        ]
    '''PROGRAM STARTER'''
    results_comparator(vals, title, x_label, labels_str, shared_x_axis)
    plt.show()



if __name__ == '__main__':
	main()