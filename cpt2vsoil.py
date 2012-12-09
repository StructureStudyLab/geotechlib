#-------------------------------------------------------------------------------
# Name:        cpt2vsoil
# Purpose:
#
# Author:      breinbaas
#
# Created:     29-11-2012
# Copyright:   (c) breinbaas 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
'''
Created on 31 okt. 2012

@author: breinbaas
'''
import sys, vsoil

def getSoiltypeByWgAndCUR162(wg):
    '''
    Returns a soiltype according to the table in CUR162 (electrical cone)
    TODO: replace hard coded ids to database ids based on the soil name
    '''
    if wg <= 0.6: return 45
    elif wg > 0.6 and wg <= 0.8:
        return 43
    elif wg > 0.8 and wg <= 1.1:
        return 43
    elif wg > 1.1 and wg <= 1.4:
        return 42
    elif wg > 1.4 and wg <= 1.8:
        return 41
    elif wg > 1.8 and wg <= 2.2:
        return 40
    elif wg > 2.2 and wg <= 2.5:
        return 39
    elif wg > 2.5 and wg <= 5.0:
        return 38
    elif wg > 5.0 and wg <= 8.1:
        return 37
    elif wg > 8.1:
        return 36

def convertToInterval(cpt, min_interval):
    '''
    Walks trough a cpt and makes soillayers every interval based on the
    wg TODO: translate wg to something English
    '''
    vs = vsoil.VSoil()
    ztop = cpt.zmax
    n = 0
    sum_wg = 0.
    for i in range(0, len(cpt.values)):
        z = cpt.values[i][0]
        wg = cpt.values[i][3]
        sum_wg += wg
        n += 1

        if i==len(cpt.values)-1:
            vs.soillayers.append([ztop, z, getSoiltypeByWgAndCUR162(sum_wg / n)])
        elif (ztop - z) > min_interval or i==len(cpt.values)-1:
            if n==0:
                print i, len(cpt.values), ztop, z, wg, "FATAL, een interval zonder waarden gevonden"
                sys.exit(0)
            else:
                vs.soillayers.append([ztop, z, getSoiltypeByWgAndCUR162(sum_wg / n)])
                ztop = z
                sum_wg = 0.
                n = 0

    return vs











