STRUCTURE_CHARACTERS = {
    '&': '\\&',
    '%': '\\%',
    '$': '\\$',
    '#': '\\#',
    '_': '\\_',
    '{': '\\{',
    '}': '\\}',
    '~': '\\textasciitilde{}',
    '^': '\\^{}',
    '\\': '\\textbackslash{}',
}

GREEK_CHARACTERS = {
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
}

MATH_CHARACTERS = {
    '∞': '\\infty ', '≈': '\\approx ', '≠': '\\neq ',
    '≤': '\\leq ',   '≥': '\\geq ',    '≡': '\\equiv',
    '±': '\\pm ',    '×': '\\times ',  '÷': '\\div ',
    '⁻¹': '^{-1}',   '⁻²': '^{-2}',    '⁻³': '^{-3}',
    '⁰': '^{0}',     '¹': '^{1}',      '²': '^{2}',
    '³': '^{3}'
}

def latex_escape_special_characters(text, structure=True, greek=True, math=True):
    """
    Escape special characters in a LaTeX string, by replacing them with their LaTeX equivalent.

    Parameters:
        - text : str, text to escape
        - structure : bool, whether to escape structure characters (e.g. '&', '%', '$')
        - greek : bool, whether to escape greek characters (e.g. 'α', 'β', 'γ')
        - math : bool, whether to escape math characters (e.g. '⁻¹', '≈', '∞')
    Returns:
        str, text with escaped characters
    """
    if not structure:
        FORMAT_CHARACTERS = {}
    if not greek:
        GREEK_CHARACTERS = {}
    if not math:
        MATH_CHARACTERS = {}

    escape_chars = {**STRUCTURE_CHARACTERS, **GREEK_CHARACTERS, **MATH_CHARACTERS}
    for character, replacement in escape_chars.items():
        text = text.replace(character, replacement)
    
    return text