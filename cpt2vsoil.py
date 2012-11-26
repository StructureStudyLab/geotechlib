'''
Created on 31 okt. 2012

@author: breinbaas
'''
import sys, vsoil

def getSoiltypeByWgAndCUR162(wg):
    '''
    Returns a soiltype according to the table in CUR162
    TODO: refer to right table
    TODO: make solitypes that correspond to the CUR162 values
    TODO: edit list below to correct values
    '''
    if wg <= 1.0: return 0
    elif wg > 1.0 and wg <= 2.0:
        return 1
    elif wg > 2.0 and wg <= 2.5:
        return 2
    elif wg > 2.5 and wg <= 3.0:
        return 3
    elif wg > 3.0 and wg <= 4.0:
        return 4
    elif wg > 4.0:
        return 5

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











