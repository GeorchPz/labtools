# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:13:45 2020

@author: jorge
"""

import sympy as sp

sp.init_printing() #SHOULD INSTALL LATEX

def f_n_δf_form(vars_str, expr_str, vars_dep):
    '''
    Calculates the uncertainty formula (for dependent OR independent values)
    _sy → Symbolic value of sympy
    '''
    
    # Create variables string list & symbols
    vars_list = vars_str.split(',')
    vars_sy   = sp.symbols(vars_str, real = True)
    
    if len(vars_list) == 1:
        vars_sy = [vars_sy]
    
    vars_dict = {k: v for k, v in zip(vars_list, vars_sy)}
    
    # Convert formula to sympy
    f_sy = sp.sympify(expr_str, locals = vars_dict)
    
    # Create gradient vector & uncertainties list (as str & symbol lists)
    grad_f, uncerts = [], []
    
    for x in vars_sy:
        grad_f.append( sp.diff(f_sy,x) )
        uncerts.append( sp.Symbol('δ' + str(x), positive = True) )
    
    if vars_dep == 'Dependent':
        δf_sy = sum([ abs(diffx)*δx for (diffx, δx) in zip(grad_f, uncerts) ])
    
    elif vars_dep == 'Independent':
        δf2 = sum([ (diffx*δx)**2 for (diffx, δx) in zip(grad_f, uncerts) ])
        δf_sy = sp.sqrt(δf2)
    else:
        raise ValueError('Are values dependent or independent?')
    
    return f_sy, δf_sy

def f_n_δf_lambdif(vars_str, f_sy, δf_sy):
    '''
    Lambdifies formulas
    That is: converts a SymPy expression into a function for numeric evaluation.
    '''
    # Variables
    uncerts_str = ','.join( 'δ' + x for x in vars_str.split(',') )
    all_vars_str = vars_str + ',' + uncerts_str
    
    # Lambdas
    f_lamb = sp.lambdify(vars_str, f_sy)
    δf_lamb = sp.lambdify(all_vars_str, δf_sy)
    
    return f_lamb, δf_lamb

def forms_exporter(form_names, formulas):
    '''Exports the formulas by: pretty-printing & returning them in their latex form'''
    latex_form = []

    for name, expr in zip(form_names, formulas):
        # Equation f = f(x,y,...) in sympy
        eq_sy = sp.Eq( sp.Symbol(name), expr )
        # Pretty printing
        sp.pprint(eq_sy)
        # Latex Formula
        latex_form.append( sp.latex(eq_sy) )
    
    # Since LaTeX usually gives problems with greek letters,
    # we change those to their LaTeX counterparts (e.g: α --> \alpha)
    
    def replace_greek_to_LaTeX(text):
        for i, j in greek_to_LaTeX_dict.items():
            text = text.replace(i, j)
        return text

    greek_to_LaTeX_dict = {
        'α': '\\alpha ', 'β': '\\beta ',    'γ': '\\gamma ',
        'δ': '\\delta ', 'ε': '\\epsilon ', 'ζ': '\\zeta ',
        'η': '\\eta ',   'θ': '\\theta ',   'ι': '\\iota ',
        'κ': '\\kappa ', 'λ': '\\lambda ',  'μ': '\\mu ',
        'ν': '\\nu ',    'ξ': '\\xi ',      'ο': '\\omikron ',
        'π': '\\pi ',    'ρ': '\\rho ',     'σ': '\\sigma ',
        'τ': '\\tau ',   'υ': '\\upsilon ', 'φ': '\\phi ',
        'χ': '\\chi ',   'ψ': '\\psi ',     'ω': '\\omega ',
        # Capital letters
        'Α': '\\Alpha ', 'Β': '\\Beta ',    'Γ': '\\Gamma ',
        'Δ': '\\Delta ', 'Ε': '\\Epsilon ', 'Ζ': '\\Zeta ',
        'Η': '\\Eta ',   'Θ': '\\Theta ',   'Ι': '\\Iota ',
        'Κ': '\\Kappa ', 'Λ': '\\Lambda ',  'Μ': '\\Mu ',
        'Ν': '\\Nu ',    'Ξ': '\\Xi ',      'Ο': '\\Omikron ',
        'Π': '\\Pi ',    'Ρ': '\\Rho ',     'Σ': '\\Sigma ',
        'Τ': '\\Tau ',   'Υ': '\\Upsilon ', 'Φ': '\\Phi ',
        'Χ': '\\Chi ',   'Ψ': '\\Psi ',     'Ω': '\\Omega ',
        # Other stuff
        '⁻¹': '^{-1}',   '⁻²': '^{-2}',     '⁻³': '^{-3}'}
    
    latex_form = list(map(replace_greek_to_LaTeX, latex_form))

    return latex_form