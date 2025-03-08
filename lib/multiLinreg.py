# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

from numpy import linspace

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.ticker import AutoMinorLocator

from lib.Linreg import rounder, short, get_vals_Lr
from lib.xl_manager import name2path


def exceler(vals_list, x_name, y_name, filename, subtitles):
    'Exports data to excel'
    from pandas import DataFrame, ExcelWriter  
    from lib.xl_editor import xl_enhancer
    
    # vals1, vals2, vals 3 = vals_list
    # x, y, σx, σy, r, A, B, σA, σB = vals
    *_, r_list, As, Bs, σAs, σBs = zip(*vals_list)
    
    As_round = [ rounder(p,e) for p,e in zip(As, σAs) ]
    Bs_round = [ rounder(p,e) for p,e in zip(Bs, σBs) ]
    
    # String of the type: y(x) = (B ± σB)·x + (A ± σA)
    poly_type = f'{y_name}({x_name}) = B·{ x_name } + A'
    
    # we change the index so that we dont transpose the usual 0,1,2 column
    df = DataFrame({
        'r'         : r_list,
        'B±'        : Bs_round,
        'A±'        : As_round,
        'B (UNITS)' : Bs,
        'σB'        : σBs,
        'A (UNITS)' : As,
        'σA'        : σAs
                        }, index= subtitles)
    df.index.name = poly_type
    
    path  = name2path('LinRegs_Data - ' + filename)
    writer = ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer)
    writer.save()

    # Make it pretty ;)
    xl_enhancer(path)


def texter(vals_list, fname, subtitles):
    'Exports data to text file'
    
    texts = []
    for vals, subttl in zip(vals_list, subtitles):
        x, y, σx, σy, r, A, B, σA, σB = vals
        #LinReg label
        label_txt = (
            f'{subttl}:\nr = { round(r,3) }' + '\n'
            f'${ y.name } = ({ rounder(A,σA) }) + ({ rounder(B,σB) })·{ x.name }$')
        
        #Linear reg. text
        texts += (
            label_txt, '\n' + 'r  = ' + short(r),
            'B  = ' + short(B), 'σB = ' + short(σB),
            'A  = ' + short(A), 'σA = ' + short(σA),
            '')
    
    txt_fname = name2path('LinRegs Data - ' + fname, ext = '.txt')
    
    print(txt_fname)
    with open(txt_fname, 'w', encoding='utf-8') as txt_file:
        # 'w' opens file in (over)writing mode
        # 'utf-8' encodes greek letters
        for line in texts:
            txt_file.write(line + '\n')
            print(line)


def multi_plotter(
        x_y_σx_σy_r_A_B_σA_σB_list,
        title, legend_title, subtitles, x_label, y_label
        ):
    '''Plots & prints linear regression's results'''
    
    # Font type
    font = {
            'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 14,
            }
    
    n = len(subtitles)
    # Plots' colours
    if n<8:
        colours = ['blue','orange','green','red','purple','cyan','pink']
        markers = ['o', '^', 's', 'v', '<', '*', '>', 'x', 'd']
    else:
        colours = cm.rainbow(linspace(0, 1, n))
        markers = ['.']*n
    labels = []
    
    '''If we don't want markers'''
    if True:
        markers = ['.']*n
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(9,6))
    
    # Since all names are the same, we take the first ones
    x_0, y_0 = x_y_σx_σy_r_A_B_σA_σB_list[0][:2]
    x_name  = x_0.name
    y_name  = y_0.name
    
    # here we plot each and every linear regresion 
    for i in range(n):
        x, y, σx, σy, r, A, B, σA, σB = x_y_σx_σy_r_A_B_σA_σB_list[i]

        # Errorbars of points
        ax.errorbar(x, y, xerr= σx, yerr= σy,
                    marker= markers[i], linestyle= '', #markersize ='10',
                    color= colours[i], alpha=0.6, ecolor= 'dimgray',
                    capsize= 2, elinewidth= 1.5)        
        # Main slope
        ax.plot(x, A + B*x , linewidth= 2,
                color= colours[i])   
        # Slope's uncertainty
        ax.fill_between(x, (A - σA) + (B - σB)*x, (A + σA) + (B + σB)*x,
                        color= colours[i], alpha=0.2)
        
        #LinReg label
        label_txt = (
            f'{subtitles[i]}:\nr = { round(r,3) }' + '\n'
            f'${ y_name }({x_name}) = ({ rounder(B,σB) })·{ x_name } + ({ rounder(A,σA) })$'
            ) # formated string
        labels += [ mlines.Line2D([], [], color= colours[i], marker= markers[i],
                                markersize=8, label= label_txt) ]
    
    # Ticks, grid and legend
    ax.xaxis.set_minor_locator( AutoMinorLocator() )
    ax.yaxis.set_minor_locator( AutoMinorLocator() )

    plt.grid(which='major', linestyle='-', alpha=0.6)
    # plt.grid(which='minor', linestyle='-', alpha=0.3)
    
    plt.title(title, fontdict= font, fontsize=16)
    plt.xlabel(x_label, fontdict= font)
    plt.ylabel(y_label, fontdict= font)
    
    # Label for the uncertaities
    incert_lbl = mpatches.Patch(color= 'grey', alpha= 0.2,
                                label= 'Incertidumbres de las pendientes')
    
    
    '''Diferent types of legend'''
    '⚠️ if ERROR: cambiar de lgd'
    
    'Leyenda abajo para 2'
    # l1, l2 = labels
    # lgd = ax.legend(
    #     handles= [l1, incert_lbl, l2],
    #     bbox_to_anchor= (0, -0.12,1,0), loc= 'upper left',
    #     ncol= 2, mode= "expand", labelspacing= 1, borderaxespad= 0.
    #     )
    'Leyenda abajo'
    lgd = ax.legend(handles= [*labels, incert_lbl], loc= 'upper left',
        bbox_to_anchor= (0, -0.12,1,0), ncol= 2, #mode= "expand",
        labelspacing= 1, borderaxespad= 0.)
    'Leyenda dentro'
    # lgd = ax.legend(handles= [*labels, incert_lbl], loc='best', fancybox=True)
    'Leyenda derecha'
    # lgd = ax.legend(handles= [*labels, incert_lbl], bbox_to_anchor=(1.01, 0.5), loc='center left', labelspacing=1, borderaxespad=0.)
    
    
    # Export plot & data
    fname = title.replace('$','').replace('\n','').replace('\\','')
    plt_fname = name2path('LinRegs - ' + fname, ext = '.png')
    plt.savefig(plt_fname, bbox_extra_artists= (lgd,),
                bbox_inches='tight', dpi = 500, transparent = False)
    
    
    if True:
        exceler(x_y_σx_σy_r_A_B_σA_σB_list, x_name, y_name, fname, subtitles)
    else:
        texter(x_y_σx_σy_r_A_B_σA_σB_list, fname, subtitles)


def main():
    '''TOGGLEABLE DATA''' # ©
    # title = 'ΔL vs ΔT - Regresiones totales'
    # subtitles = 'Cobre','Aluminio', 'Acero'
    
    # x_label = 'ΔT \; (ºK)'
    # y_label = 'ΔL \; (mm)'
    
    # f_names = 'datos_cobre','datos_aluminio','datos_acero'
    
    title = '$n$ vs $λ^{-2}$'
    x_label = 'λ^{-2} \; (pm^{-2})'
    y_label = 'n'
    legend_ttl = None
    subtitles = 'Espectro del Hg', 'Espectro del Cd'
    f_names = 'espectro_Hg_©', 'espectro_Cd_©'
    
    '''PROGRAM STARTER'''
    vals_list = [get_vals_Lr(x_label, y_label, f_name) for f_name in f_names]
    multi_plotter(vals_list, title, legend_ttl, subtitles, x_label, y_label)
    plt.show()


if __name__ == '__main__':
	main()