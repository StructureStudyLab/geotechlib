'''
Created on 2 nov. 2012

@author: breinbaas
'''

class Opbouw(object):
    '''
                  0     1         2
    grondlaag = zmax, zmin, grondsoort_id
    '''
    def __init__(self):
        self.id = -1
        self.grondlagen = []
        
    def optimize(self):
        new_grondlagen = []
        z1 = 0.
        id = -1
        for i in range(0, len(self.grondlagen)):
            if i==0:
                z1 = self.grondlagen[i][0]
                id = self.grondlagen[i][2]
            elif i==len(self.grondlagen)-1:
                new_grondlagen.append([z1, self.grondlagen[i][1], id])                
            elif id != self.grondlagen[i][2]:
                new_grondlagen.append([z1, self.grondlagen[i][0], id])
                z1 = self.grondlagen[i][0]
                id = self.grondlagen[i][2]
        self.grondlagen = new_grondlagen[:]       
          
    def asText(self):
        result = "van;tot;grondsoort_id\n"
        for gl in self.grondlagen:
            result += "%.2f;%.2f;%d\n" % (gl[0], gl[1], gl[2])
        return result
            
        
        