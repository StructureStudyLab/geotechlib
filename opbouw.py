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
        '''
        Deze optimalisatie zorgt ervoor dat opbouwen waarbij 2 of meer lagen
        dezelfde id hebben samengevoegd worden tot 1 laag.
        '''
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
        '''
        Geeft een string terug in de vorm van
        van;tot;grondsoort_id met een regeleinde na elke entry
        '''
        result = "van;tot;grondsoort_id\n"
        for gl in self.grondlagen:
            result += "%.2f;%.2f;%d\n" % (gl[0], gl[1], gl[2])
        return result

    def blobToData(self, data):
        '''
        Leest een grondopbouw uit de sqllite database en stopt de entries
        in de grondlagen lijst
        '''
        lines = data.split('\n')
        self.grondlagen = []

        for i in range(1, len(lines)):
            line = lines[i]
            if len(line.strip())>0:
                van, tot, id = line.split(';')
                self.grondlagen.append([float(van),float(tot),int(id)])