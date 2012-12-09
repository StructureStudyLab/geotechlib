#-------------------------------------------------------------------------------
# Name:        vsoil
# Purpose:
#
# Author:      breinbaas
#
# Created:     29-11-2012
# Copyright:   (c) breinbaas 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
'''
Created on 2 nov. 2012

@author: breinbaas
'''

class VSoil(object):
    '''
    A VSoil object contains information of soil layers that are stacked
    on top of each other (like in a borehole). VSoil stands for vertical soil
    The main information is in soillayers which looks like
                  0     1         2
    Soil layer = zmax, zmin, soillayer_id

    The source shows where the information came from (for example `auto-generated'
    if a correlation is done)
    '''
    def __init__(self):
        self.id = -1
        self.soillayers = []
        self.source = ""

    def optimize(self):
        '''
        Optimization makes sure that two (or more) layers that are next to each
        other are rebuild into one layer.
        '''
        new_soillayers = []
        z1 = 0.
        id = -1
        for i in range(0, len(self.soillayers)):
            if i==0:
                z1 = self.soillayers[i][0]
                id = self.soillayers[i][2]
            elif i==len(self.soillayers)-1:
                new_soillayers.append([z1, self.soillayers[i][1], id])
            elif id != self.soillayers[i][2]:
                new_soillayers.append([z1, self.soillayers[i][0], id])
                z1 = self.soillayers[i][0]
                id = self.soillayers[i][2]
        self.soillayers = new_soillayers[:]

    def asText(self):
        '''
        Returns a string like;
        top;bottom;soillayer_id
        '''
        result = "top;bottom;soillayer_id\n"
        for gl in self.soillayers:
            result += "%.2f;%.2f;%d\n" % (gl[0], gl[1], gl[2])
        return result

    def blobToData(self, data):
        '''
        Reads a VSoil class from the sqllite database.
        '''
        lines = data.split('\n')
        self.soillayers = []

        for i in range(1, len(lines)):
            line = lines[i]
            if len(line.strip())>0:
                top, bottom, id = line.split(';')
                self.soillayers.append([float(top),float(bottom),int(id)])