#-------------------------------------------------------------------------------
# Name:        cpt
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

Reads a cpt file and stores the interesting stuff in this class

note:
only accepts cpt files
only accepts if they have qc (conusweerstand), pw (plaatselijke wrijving), z (depth)
only reads files where columninfo comes BEFORE columnvoid (which is default)

@author: breinbaas
'''
import sys, datetime, latlon

class CPT:
    '''
    The CPT class contains the following cpt information;
    id:        ID
    name:      filename that was read
    zmax:      Highest point of the CPT
    x:         X-coordinate
    y:         Y-coordinate
    zmin:      Lowest point of the CPT
    date:      Date of test
    values:    Measurements in the order of [z, qc, pw, wg]
    '''
    def __init__(self):
        '''
        Initialisation.
        '''
        self.id = -1
        self.name = ""
        self.x = 0.0
        self.y = 0.0
        self.zmax = 0.0
        self.zmin = 0.0
        self.date = datetime.datetime(1900,1,1)
        self.values = [] #z, qc, pw, wg

    def dataAsText(self):
        '''
        Return a list of strings containing the values like;
        -1.23;1.234;0.013;0.562
        '''
        result = "z [m tov ref];qc [MPa];fs [MPa];wg [%]\n"
        for z, qc, pw, wg in self.values:
            result += "%.2f;%.3f;%.3f;%.3f\n" % (z, qc, pw, wg)
        return result

    def getValuesAt(self, _z):
        "Returns the values at the given depth. Returns None is _z is out of range"
        for z, qc, pw, wg in self.values:
            if (z < _z):
                return qc, pw, wg
        return None, None, None

    def blobToData(self, data):
        "Reads a blob from the database and translates it back to values."
        lines = data.split('\n')
        self.values = []

        for i in range(1, len(lines)):
            line = lines[i]
            if len(line.strip())>0:
                z, qc, pw, wg = line.split(';')
                self.values.append([float(z),float(qc),float(pw),float(wg)])

    def getLatitude(self):
        '''
        Returns the latitude of a cpt file (WGS84 coordinates).
        '''
        lat, lon = latlon.RDToLatLon(self.x, self.y)
        return lat

    def getLongitude(self):
        '''
        Returns the longitude of a cpt file (WGS84 coordinates).
        '''
        lat, lon = latlon.RDToLatLon(self.x, self.y)
        return lon

    def readFromFile(self, filename):
        '''
        Reads a CPT from a GEF file.
        returns: string with error or `none` if there is no error.
        '''
        readHeader = True
        colid = {'dz':-1, 'qc':-1, 'pw':-1, 'wg':-1}
        colvoid = {'dz':None, 'qc':None, 'pw':None, 'wg':None}
        calcWg = True
        typegef = "notset"
        columnseperator = " "

        for line in open(filename, 'r'):
            if readHeader:
                keyword = line.split('=')[0]
                args = line.split('=')[1].split(',')
                if line.find("#EOH")>-1:
                    #als er geen qc en pw is zijn we niet geinteresseerd in de sondering
                    if colid['qc']==None or colid['pw']==None:
                        return "FATAL ERROR: Found gef file without qc or fs, not interested in this file"
                    if colid['dz']==None:
                        return "FATAL ERROR: Found gef file without columninfo for z, useless file"
                    #als er wel qc en pw is gaan we het wrijvingsgetal zelf berekenen
                    calcWg = colid['wg']==None
                    #stop met de header en start het lezen van de data
                    readHeader = False
                elif keyword=="#STARTDATE":
                    year = int(args[0].strip())
                    month = int(args[1].strip())
                    day = int(args[2].strip())
                    self.date = datetime.datetime(year, month, day)
                elif keyword=="#FILEDATE": #some people skip the startdate which is stupid but the filedate will do in this case
                    if self.date.year==1900:
                        year = int(args[0].strip())
                        month = int(args[1].strip())
                        day = int(args[2].strip())
                        self.date = datetime.datetime(year, month, day)
                elif keyword=="#COLUMNSEPARATOR":
                    columnseperator = args[0].strip()
                    if len(columnseperator)<=0:
                        columnseperator = " "
                elif keyword=="#REPORTCODE" or keyword == "#PROCEDURECODE":
                    if line.upper().find("GEF-CPT-Report".upper()) > -1:
                        typegef = "sondering"
                elif line.find("#ZID")>-1:
                    self.zmax = float(args[1].strip())
                elif line.find("#XYID") > -1:
                    #make sure the x and y have 2 digits
                    self.x = float(args[1].strip())
                    self.y = float(args[2].strip())
                elif keyword == "#COLUMNVOID":
                    #ga er van uit dat altijd eerst columninfo wordt ingevuld en daarna columnvoid
                    #zo niet dan is er programmeerwerk nodig!
                    if colid['dz']==None:
                        return "FATAL ERROR: Found gef file with columnvoid defined before columninfo"
                    id = int(args[0].strip())
                    for i, c in colid.iteritems():
                        if c==id:
                            colvoid[i]=args[1].strip()
                elif keyword == "#COLUMNINFO":
                    id = int(args[3].strip())
                    if id == 1 or id == 11: #sondeerlengte of gecorrigeerde sondeerlengte
                        colid['dz'] = int(args[0].strip()) - 1
                    elif id == 2: #conusweerstand
                        colid['qc'] = int(args[0].strip()) - 1
                    elif id == 3: #wrijvingsweerstand
                        colid['pw'] = int(args[0].strip()) - 1
                    elif id == 4: #wrijvingsgetal
                        colid['wg'] = int(args[0].strip()) - 1
            else:
                if typegef=="sondering":
                     #splits de lijn in argumenten en sla lege argumenten over
                    args = []
                    for arg in line.split(columnseperator):
                        if len(arg.strip())>0:
                            args.append(arg.strip())

                    if args[colid['qc']]!= colvoid['qc'] and args[colid['pw']]!=colvoid['pw']:
                        dz = float(args[colid['dz']])
                        qc = float(args[colid['qc']])
                        if qc <= 0.:
                            qc = 0.01
                        pw = float(args[colid['pw']])
                        if calcWg:
                            wg = (pw / qc) * 100.
                        else:
                            wg = float(args[colid['wg']])

                        self.values.append([(self.zmax-abs(dz)), qc, pw, wg])
                else:
                    return "ERROR: Found gef file %s of type %s" % (filename, typegef)

        self.zmin = self.values[len(self.values)-1][0]
        return "none"
