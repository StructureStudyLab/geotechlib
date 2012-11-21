'''
Created on 31 okt. 2012

@author: breinbaas
'''
import sys, opbouw

def getGrondsoortCUR162(wg):
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
    
def convertToInterval(son, min_interval):
    opb = opbouw.Opbouw()
    ztop = son.mv
    n = 0
    sum_wg = 0.
    for i in range(0, len(son.values)):
        z = son.values[i][0]
        wg = son.values[i][3]
        sum_wg += wg
        n += 1                
        
        if i==len(son.values)-1:
            opb.grondlagen.append([ztop, z, getGrondsoortCUR162(sum_wg / n)]) 
        elif (ztop - z) > min_interval or i==len(son.values)-1:
            if n==0:
                print i, len(son.values), ztop, z, wg, "FATAL, een interval zonder waarden gevonden"
                sys.exit(0)
            else:                
                opb.grondlagen.append([ztop, z, getGrondsoortCUR162(sum_wg / n)])                
                ztop = z 
                sum_wg = 0.
                n = 0    
     
    return opb
                                      
        
            
                
            

                    
                
                    
                
                    
