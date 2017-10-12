#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A tentative collection of functions for writing the charge in different formats (to be integrated into the charge class).
"""
################################################################################

import numpy as np
from .xsf_format import xsf_struct, xsf_datagrid_2d

def write_1Dcharge_file(X, Y, nx=1, plot_file = 'chargeplot1D.out'):
    """
    Writes a text file for a 1D plot of the charge.

    :param X: variable x along the path chosen for the plot
    :param Y: charge along the path
    :param nx: number of points of the path
    :param plot_file: output charge plot file
    :return:
    """
    # Determine max and min of the (real) charge and the sum of imaginary (absolute) charge
    charge_min = np.min(Y.real)
    charge_max = np.max(Y.real)
    charge_im = np.sum(np.abs(Y.imag)) / nx

    f = open(plot_file, 'w')
    f.write('# Minimun, maximun, imaginary charge: '+"{:.9E}  ".format(charge_min) + "{:.9E}  ".format(charge_max)+
             "{:.9E}\n".format(charge_im))
    f.write('# 1D plot, nx =  '+ str(nx) +'\n')
    f.write('# X' + 16 * ' ' + 'Y\n')
    for i in range(0, nx):
        f.write("{:.9E}  ".format(X[i]) + "{:.9E}\n".format(Y[i].real))


def write_2Dcharge_file(X, Y, Z, struct_info, x0, e1, e2, nx=1, ny=1, plot_file = 'chargeplot2D.out', format='gnuplot'):
    """
    Writes a file for a 2D plot of the charge in different formats.

    :param X: variable x along the 1st direction chosen for the plot
    :param Y: variable y along the 2nd direction chosen for the plot
    :param Z: charge on the grid
    :param nx: number of points along the 1st direction
    :param ny: number of points along the 2nd direction
    :param plot_file: output charge plot file
    :param format:  'gnuplot' -> 3 columns with x, y coordinates and charge data (suitable for gnuplot or similar)
                    'plotrho.x' -> format for plotrho.x
                    'xsf' -> xsf format for XCrySDen
    :return:
    """

    a = struct_info['a']
    # normalize e1
    m1 = np.linalg.norm(e1)
    if (abs(m1) < 1.0E-6):  # if the module is less than 1.0E-6
        e1 = a[1]
        m1 = np.linalg.norm(e1)
    e1 = e1 / m1

    # normalize e2
    m2 = np.linalg.norm(e2)
    if abs(m2) < 1.0E-6:  # if the module is less than 1.0E-6
        e2 = a[2]
        m2 = np.linalg.norm(e2)
    e2 = e2 / m2

    # Steps along the e1 and e2 directions...
    deltax = m1 / (nx - 1)
    deltay = m2 / (ny - 1)

    # Determine max and min of the (real) charge and the sum of imaginary (absolute) charge
    charge_min = np.min(Z.real)
    charge_max = np.max(Z.real)
    charge_im = np.sum(np.abs(Z.imag)) / nx / ny

    f = open(plot_file,'w')

    if format == 'gnuplot':
        f.write(
            '# Minimun, maximun, imaginary charge: ' + "{:.9E}  ".format(charge_min) + "{:.9E}  ".format(charge_max) +
            "{:.9E}\n".format(charge_im))
        f.write('# 2D plot, nx =  ' + str(nx) + ' ny = ' + str(ny) + '\n')
        f.write('# X' + 16 * ' ' + 'Y' + 16 * ' ' + 'Z\n')
        for i in range(0,nx):
            for j in range(0,ny):
                f.write("{:.9E}  ".format(X[i, j]) + "{:.9E}  ".format(Y[i, j]) + "{:.9E}\n".format(Z[i, j].real))
            f.write("\n")
    elif format == 'contour.x':
        pass
    elif format == 'plotrho.x':
        f.write("{:4d} {:4d}\n".format( (nx-1), (ny-1) ))
        for i in range(0, nx):
            f.write(("{:8.4f}").format((deltax * i)))
            if ((i+1) % 8) == 0 or i==nx-1:
                f.write("\n")
        for i in range(0, ny):
            f.write("{:8.4f}".format((deltay * i)))
            if ((i+1) % 8) == 0 or i==ny-1:
                f.write("\n")
        for i in range(0, nx):
            for j in range(0,ny):
                f.write("{:12.4E}".format(Z[i, j].real))
                if ((i*ny + j +1) % 6) == 0:
                    f.write("\n")
        f.write("\n")
        f.write("{:8.4f} {:8.4f} {:8.4f}\n".format(x0[0],x0[1],x0[2]))
        f.write("{:8.4f} {:8.4f} {:8.4f}\n".format(m1 * e1[0], m1 * e1[1], m1 * e1[2]))
        f.write("{:8.4f} {:8.4f} {:8.4f}\n".format(m2 * e2[0], m2 * e2[1], m2 * e2[2]))
        #TODO: add structural info (not clear if it should be done)
    elif format == 'xsf':
        one = xsf_struct(struct_info)
        two = xsf_datagrid_2d(Z, nx, ny, m1, m2, x0, e1, e2, struct_info)
        f.write(one+two)
    else:
        print('Format not implemented')
        raise NotImplementedError
