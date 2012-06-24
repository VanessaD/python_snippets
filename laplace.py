#!/usr/bin/python
# Copyright 2009, Di, Wei.
"""
Old Python Codes which using the module relaxm_wdi.py for solving a discrete Laplace equation
	Author:: Di, Wei (vanessa.wdi@gmail.com)
	Date: 2009-9-14
	Python Version: 2.6
"""


from mpi4py import MPI
from relaxm import relax, relaxB, relaxU
rank = MPI.COMM_WORLD.Get_rank()
n = 50
u = [None]*n
nsweeps = 100
from numpy import arange, ones, outer
def uc(z): return (-1./(z+2.) + 1./(z-2.+1.j)).real
dx = 2./float(n-1)
x = -1. + arange(float(n))*dx
z = outer(x, ones(n)) + outer(ones(n), 1.j*x)
u = uc(z).copy()

if rank == 0:
    verbose = True
    if verbose:
        from pylab import contourf, savefig
        from numpy import transpose, max
        contourf(x, x, transpose(u))
        # Not the exact solution but visually indistinguishable from it.
        savefig('accurate_wdi.pdf')
        def residual():
            return max(4*u[1:n-1,1:n-1] - u[0:n-2,1:n-1] - u[2:n,1:n-1] \
                - u[1:n-1,0:n-2] - u[1:n-1,2:n])/(dx*dx)
        print 'Residual of accurate solution is', residual()
    u[1:-1, 1:-1] = 0
    time1 = MPI.Wtime()
    relax(u, nsweeps)
    time2 = MPI.Wtime()
    print 'Serial relax took', time2 - time1, 'seconds.'
    print u[n/2-1:n/2+1, n/2-1:n/2+1]
    if verbose:
        contourf(x, x, transpose(u))
        savefig('inaccurate_wdi.pdf')
        print 'Residual of inaccurate solution is', residual()
    u[1:-1, 1:-1] = 0
    time1 = MPI.Wtime()
    
u[1:-1, 1:-1] = 0
relaxB(u, nsweeps)
if rank == 0:
    time2 = MPI.Wtime()
    print '"Blocked" parallel relax took', time2 - time1, 'seconds.'
    print u[n/2-1:n/2+1, n/2-1:n/2+1]
    u[1:-1, 1:-1] = 0
    time1 = MPI.Wtime()
    
u[1:-1, 1:-1] = 0
relaxU(u, nsweeps)
if rank == 0:
    time2 = MPI.Wtime()
    print '"Unblocked" parallel relax took', time2 - time1, 'seconds.'
    print u[n/2-1:n/2+1, n/2-1:n/2+1]
