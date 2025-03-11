# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:31:29 2020

@author: Jorge Pottiez López-Jurado
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from pandas import read_excel
from mpl_toolkits.mplot3d import Axes3D
# GManaging windows
from IPython import get_ipython

from lib.files_manager import name2path, newpath, get_data_n_uncert


def plotter(x_y_z_δx_δy_δz, title, x_label, y_label, z_label, save_mode):
    '''Plots results'''

    # Font type
    font = {
        'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14,
    }
    # Colour sequences
    colormaps = cm.coolwarm, cm.plasma, cm.brg, cm.Reds
    used_cmap = colormaps[0]

    # Plot the data
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')

    x_y_z, _ = x_y_z_δx_δy_δz
    x, y, z = x_y_z

    # Plot points
    ax.scatter(
        x, y, z, c=z, cmap=used_cmap, linewidth=1, antialiased=False
        )

    ax.plot_trisurf(x, y, z, cmap=used_cmap, alpha=0.5)

    # Ticks, grid, labels and legend
    ax.set_xlabel(x_label, fontdict=font)
    ax.set_ylabel(y_label, fontdict=font)
    ax.set_zlabel(z_label, fontdict=font)

    ax.grid(which='major', linestyle='-', alpha=0.6)
    # ax.grid(which='minor', linestyle='-', alpha=0.3)

    plt.title(title, fontdict=font, fontsize=16)
    # plt.legend(loc='best', fontsize=12)

    # Export plot
    if save_mode:
        num_of_pics = 6
        ranger = range(0, 360, int(360/num_of_pics))

        folder_path = newpath('3D_Plot - ' + title)
        print('wait!')
        for count, θ in enumerate(ranger):
            ax.view_init(elev=30., azim=θ)
            plot_name = name2path(
                f'azimuth {θ}º', extension='.png', filedir=folder_path)
            plt.savefig(plot_name, dpi=500,
                        bbox_inches='tight', transparent=False)
            print(num_of_pics - count, '..')
        print(f'done for all azimuths in {tuple(ranger)}.')


def get_vals(x_label, y_label, z_label, f_name):
    '''Gets all necessary values from our file'''
    # Find magnitudes
    x_magn = x_label.split(' ')[0]
    y_magn = y_label.split(' ')[0]
    z_magn = z_label.split(' ')[0]

    if '$' in x_magn + y_magn + z_magn:
        x_magn = x_magn.replace('$', '')
        y_magn = y_magn.replace('$', '')
        z_magn = z_magn.replace('$', '')

    # Import data
    data = read_excel(name2path(f_name))
    x_y_z_δx_δy_δz = get_data_n_uncert(
        x_magn + ',' + y_magn + ',' + z_magn, data)

    return x_y_z_δx_δy_δz


def main():
    '''TOGGLEABLE DATA'''
    title = 'Diagramas P-T-V'
    x_label = 'V (L)'
    y_label = 'P (atm)'
    z_label = 'T (ºC)'
    f_name = 'Diag_3D'

    save_mode = False
    # Getting matplotlib in console (0th) or in separate window (1st)
    windows_mode = ['inline', 'qt'][1]
    '''PROGRAM STARTER'''
    get_ipython().run_line_magic('matplotlib', windows_mode)

    vals = get_vals(x_label, y_label, z_label, f_name)
    plotter(vals, title, x_label, y_label, z_label, save_mode)
    plt.show()


if __name__ == '__main__':
    main()
