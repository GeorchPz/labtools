# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 21:00:02 2023

@author: Jorge Pottiez López-Jurado
"""

import os

path = "C:\\Users\\jorge\\OneDrive\\Programas_py\\Lab_programs\\Lab_data"

l = os.listdir(path)

ext = '.xlsx'
label = ''

m = []
for i in l:
    if ext in i and label in i:
        i = i.replace(ext,'')
        m.append(i)
print(m)

'Modificar lista'
# n = []
# for i in m:
#     i = i.replace('','')
#     n.append(i)
# print(n)