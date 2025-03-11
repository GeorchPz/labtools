# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""


from analysis.linear_regression import rounder, short
from data.extract_data import name2path

import pandas as pd
from data.exports import xl_enhancer

def exceler(x, y, coefs, err, roundlist, form, filename):
    'Transfers data to excel'
    
    abc = ['A','B','C','D','E','F','G']
    n = len(coefs)
    
    # Cutting abc list and inverting it : if n=2 -> [B,A]
    cba = abc[:n][::-1]
    
    # List of monomials
    monos = [f'{ cba[i] }·{x.name}^{ i }' for i in range(len(coefs))]
    # String of the type: y(x) = (A ± σA) + (B ± σB)·x ...
    poly_type = f'{y.name}({x.name}) = ' + ' + '.join( monos[::-1] )
    poly_type = poly_type.replace(f'·{x.name}^0','').replace('^1','')
    
    # we change the index so that we dont transpose the usual 0,1,2 column
    df = pd.DataFrame({
            'Round'    : roundlist,
            'Monomial' : monos[::-1],
            'Values'   : coefs,
            'Errors'   : err
                        }, index= abc[:n])
    
    df = df.transpose()
    df.index.name = poly_type
    
    path  = name2path(filename + '_PolyReg_Data')
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer)
    writer.save()

    # Make it pretty ;)
    xl_enhancer(path)


def central(title, x_label, y_label, filename, degree):
    '''PROGRAM STARTER'''
    x, y, δx, δy = get_exp_vals(x_label, y_label, filename)
    
    coefs, err = poly_reg(x, y, degree)
    
    # roundlist = [ rounder(p,e) for p,e in zip(coefs, err) ]
    # monomials = [ f'({ s })·{x.name}^{ i }' for i, s in enumerate(roundlist[::-1])] [::-1]
    
    # # Formula
    # form = f'{y.name}({x.name}) = ' + ' + '.join( monomials )
    # form = form.replace(f'·{x.name}^0','').replace('^1','')
    
    plotter(x, y, δx, δy, coefs, err, form, title, x_label, y_label, filename)
    exceler(x, y, coefs, err, roundlist, form, filename)


def main():
    '''TOGGLEABLE DATA'''
    # title = '$n$ vs $λ^{-2}$'
    # x_label = '$λ^{-2}$ \; ($nm^{-2}$)'
    # y_label = 'n'
    # filename = 'espectro_Hg_©'
    
    titles = ['Amarillo', 'Azul', 'Verde', 'Violeta 1', 'Violeta 2']
    x_lab = '$I$ (%)'
    y_lab = '$V$ (V)'
    files = ['Amarillo', 'Azul', 'Verde', 'Violeta 1', 'Violeta 2']
    degree = 3
    
    if type(titles) == str:
        central(titles, x_lab, y_lab, files, degree)
    else:
        for title, file in zip(titles, files):
            central(title, x_lab, y_lab, file, degree)

if __name__ == '__main__':
	main()