#!/usr/bin/python
# Copyright 2009, Di, Wei.
""" Python module pwlm that implements piecewise linear interpolation
for given data with a given triangulation. The module defines two functions:

(i) The function pwl new(x, y, z, triang) returns a representation of a piecewise linear
function of 2 variables given scattered points whose coordinates are in the 1D (NumPy)
arrays x and y with corresponding function values in the 1D array z. The triangles are
defined by a 2D array of integers, each row consisting of three indices i; j; k such that
the points (xi; yi), (xj ; yj ), (xk; yk) give the corners of the triangle in a counterclockwise
order.
(ii) The function plw eval(pwl, x, y) returns the value of the piecewise linear function
represetend by pwl at an arbitrary point (x, y). If the point is out of range (outside of
every triangle), the None value is returned.

	Author:: Di, Wei (vanessa.wdi@gmail.com)
	Date: 2009-9-14
	Python Version: 2.6
"""

def pwl_new(x, y, z, triang):
    from pylab import zeros
    from numpy.linalg import solve
    from numpy import transpose
    
    no_triang = len(triang)
    pwl = zeros((no_triang*3 + no_triang, 3), float)
    for i in range(no_triang):
        tria_ix = triang[i]
        x1 = x[tria_ix[0]]
        y1 = y[tria_ix[0]]
        z1 = z[tria_ix[0]]
        x2 = x[tria_ix[1]]
        y2 = y[tria_ix[1]]
        z2 = z[tria_ix[1]]
        x3 = x[tria_ix[2]]
        y3 = y[tria_ix[2]]
        z3 = z[tria_ix[2]]

        d = x1*y2 - x1*y3 - x2*y1 + x2*y3 + x3*y1 - x3*y2
        a0 = (y2-y3)
        b0 = (x3-x2)
        c0 = (x2*y3-x3*y2)
        a1 = (y3-y1)
        b1 = (x1-x3)
        c1 = (x3*y1-x1*y3)
        a2 = (y1-y2)
        b2 = (x2-x1)
        c2 = (x1*y2-x2*y1)


        pwl[i*3+0] = [a0, b0, c0]
        pwl[i*3+1] = [a1, b1, c1]
        pwl[i*3+2] = [a2, b2, c2]

        A = zeros((3,3),float)
        A[0] = [x1, y1, 1]
        A[1] = [x2, y2, 1]
        A[2] = [x3, y3, 1]
        B = zeros((3,1),float)
        B[0] = z1
        B[1] = z2
        B[2] = z3
        inv_ab = transpose(solve(A, B))
        pwl[no_triang*3+i] =inv_ab  

    return pwl

def pwl_eval(pwl, x, y):
    from numpy import zeros, dot, logical_and, where
    # http://www.scipy.org/Numpy_Example_List
    
    no_triang = len(pwl)/4
    r = zeros((3,1),float)
    r[0] = x
    r[1] = y
    r[2] = 1
    judge_vec = dot(pwl[range(no_triang * 3)],r)
    
    index1 = range(0, no_triang*3,3)
    j1 = judge_vec[index1] >= 0

    index2 = range(0+1, no_triang*3+1,3)
    j2 = judge_vec[index2] >= 0

    index3 = range(0+2, no_triang*3+2,3)
    j3 = judge_vec[index3] >= 0
  
    log_judge1 = logical_and(j1,j2)
    log_judge2 = logical_and(j1,j3)
    log_judge3 = logical_and(log_judge1,log_judge2)
    k = where(log_judge3)
    if len(k[0])==0:
       z = None
       return z
    elif len(k[0])>1:
         temp = k[0]
         k_select = temp[0]
    elif len(k[0])==1:
         k_select = k[0]

    coef = pwl[no_triang*3+k_select]
    z = dot(coef, r)  

    return z



def mycontour(f, xmin, xmax, ymin, ymax, nx=101, ny=101):
    from pylab import arange, zeros, vectorize, contourf
    x = xmin + (xmax - xmin)*arange(float(nx))/float(nx-1)
    y = ymin + (ymax - ymin)*arange(float(ny))/float(ny-1)
    z = zeros((ny, nx))
    vf = vectorize(f)
    print type(vf)
    print vf
    ion()
    for i in xrange(nx):
        z[:, i] = vf(x[i], y)
    contourf(x, y, z, 96)
    return z

if __name__ == '__main__':
   from pylab import array, ion, figure, ones, arange, outer, reshape, show, savefig
   from matplotlib.delaunay import delaunay
   
   ###  Example 1
   x = array([0., 0., 1., 1., 2., 2.])
   y = array([0., 1., 0., 1., 0., 1.])
   z = array([1., 0., 0., 0., 0., 1.])

   triang = delaunay(x, y)[2]
   pwl = pwl_new(x, y, z, triang)
   def f(x, y): return pwl_eval(pwl, x, y)

   
   print abs(f(0.2, 0.7) - 0.3) <= 1.e-6
   print abs(f(1.7, 0.2) - 0.2) <= 1.e-6
   print f(0.3, 1.3) == None
   
   ion()
   figure()
   zc1 = mycontour(f, 0., 2., 0., 1.)
   savefig('wdi_fig_1.eps')

  
   ### Example 2
   x = array([0.0, 0.0, 0.0, 0.7, 1.2, 0.9, 2.0, 2.0, 2.0])
   y = array([0.0, 0.6, 1.0, 0.0, 0.8, 1.0, 0.0, 0.5, 1.0])
   z = array([1.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.0])
   
   triang = delaunay(x, y)[2]
   pwl = pwl_new(x, y, z, triang)
     
   print abs(f(0.2, 0.7)- 5.0/36.0) <= 1.e-6
     
   ion()
   figure()
   zc2 = mycontour(f, 0., 2., 0., 1.)
   savefig('wdi_fig_2.eps')

   ### Example 3
   x = reshape(outer(ones(5), arange(-1.5, 1.75, 0.25)), -1)
   y = reshape(outer(arange(-0.5, 0.75, 0.25), ones(13)), -1)

   def g(x, y): return ((x-1.0)**2+y*y)*((x+1.0)**2+y*y)+0.2*x+0.1*y

   figure()
   zc3 = mycontour(g, -1.5, 1.5, -0.5, 0.5)
   savefig('wdi_fig_3.eps')

   triang = delaunay(x, y)[2]
   pwl = pwl_new(x, y, g(x,y), triang)
   print abs(f(-1.2, 0.2) - 0.2784375) <= 1.e-6
   print abs(f(0.7, -0.2) - 0.5371875) <= 1.e-6

   figure()
   zc4 = mycontour(f, -1.5, 1.5, -0.5, 0.5)
   savefig('wdi_fig_4.eps')
 
