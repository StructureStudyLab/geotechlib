'''
Created on 6 nov. 2012

@author: breinbaas
'''

import math, numpy

def RDToLatLon(x, y):
    '''
    Converts (Dutch) RD coordinates into latitude and longitude values.
    '''
    x0 = 155000.
    y0 = 463000.
    phi0 = 52.15517440
    lambda0 = 5.38720621

    K = numpy.array( [( 0., 3235.65389, -.24750, -.06550, 0.),
                      (-.00738, -.00012, 0., 0., 0.),
                      (-32.58297, -.84978, -.01709, -.00039, 0.),
                      (0., 0., 0., 0., 0.),
                      (.00530, 0.00033, 0., 0., 0.),
                      (0., 0., 0., 0., 0.)])

    L = numpy.array( [(0., .01199, 0.00022, 0., 0.),
                      (5260.52916, 105.94684, 2.45656, .05594, .00128),
                      (-.00022, 0., 0., 0., 0.),
                      (-.81885, -.05607, -.00256, 0., 0.),
                      (0., 0., 0., 0., 0.),
                      (.00026, 0., 0., 0., 0.)])

    dx = (x - x0) * .00001
    dy = (y - y0) * .00001

    phi = 0.
    lam = 0.
    for q in range(5):
        for p in range(6):
            phi += K[p][q] * math.pow(dx, float(p)) * math.pow(dy, float(q))
            lam += L[p][q] * math.pow(dx, float(p)) * math.pow(dy, float(q))

    phi = phi0 + phi / 3600.
    lam = lambda0 + lam / 3600.

    return phi, lam

def LatLonToRD(lat, lon):
    '''
    Converts latitude and longitude values into (Dutch) RD coordinates.
    '''
    x0 = 155000.
    y0 = 463000.
    phi0 = 52.15517440
    lambda0 = 5.38720621

    R = numpy.array( [(0., 190094.945, -0.008, -32.391, 0.),
                      (-0.705, -11832.228, 0., -0.608, 0.),
                      (0., -114.211, 0., 0.148, 0.),
                      (0., -2.340, 0., 0., 0.)])

    S = numpy.array( [( 0., 0.433, 3638.893, 0., 0.092),
                      (309056.544, -0.032, -157.984, 0., -0.054),
                      (73.077, 0., -6.439, 0., 0.),
                      (59.788, 0., 0., 0., 0.)])

    dphi = 0.36 * (lat - phi0)
    dlambda = 0.36 * (lon - lambda0)

    x = 0.
    y = 0.
    for q in range(5):
        for p in range(4):
            x += R[p][q] * math.pow(dphi, float(p)) * math.pow(dlambda, float(q))
            y += S[p][q] * math.pow(dphi, float(p)) * math.pow(dlambda, float(q))

    x += x0
    y += y0

    return x, y

if __name__ == '__main__':
    lat, lon = RDToLatLon(120304, 474004)
    #x, y = LatLonToRD(52.37453253, 4.88352559)
    print lat,lon
    #print x,y
