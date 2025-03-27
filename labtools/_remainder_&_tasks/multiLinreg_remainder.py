# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

from analysis.linear_regression import rounder, short, get_vals_Lr
from data.extract_data import name2path


def exceler(vals_list, x_name, y_name, filename, subtitles):
    'Exports data to excel'
    from pandas import DataFrame, ExcelWriter  
    from data.exports import xl_enhancer
    
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


if __name__ == '__main__':
	main()