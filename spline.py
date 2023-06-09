import numpy as np
import scipy.interpolate as si
import random
import matplotlib.pyplot as plt
from polyline import polyline_generator

def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array of control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree,1,count-1)

    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree,count+degree+degree-1)
    else:
        kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

    # Calculate query range
    u = np.linspace(periodic,(count-degree),n)

    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T

def spline(width, height):
    cv = list(polyline_generator(7))
    d=2
    p = bspline(cv,n=100,degree=d,periodic=False)
    x,y = p.T
    x*=width/64
    y*=height/64
    return np.array([x,y]).T


if __name__ == '__main__':
    cv = np.array(list(polyline_generator(7)))
    plt.plot(cv.T[0], cv.T[1], 'o-', label='Polyline Points')
    
    d=2
    p = bspline(cv,n=100,degree=d,periodic=False)
    x,y = p.T
    plt.plot(x,y,'r-', label='B-Spline Curve (degree='+str(d)+')')

    plt.minorticks_on()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, 64)
    plt.ylim(0, 64)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

