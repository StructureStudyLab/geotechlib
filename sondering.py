'''
Created on 2 nov. 2012

Reads a gef file and stores the interesting stuff in this class

note:
only accepts cpt files
only accepts if they have qc, pw, z
only reads files where columninfo comes BEFORE columnvoid (which is default)

@author: breinbaas
'''
import sys, datetime, latlon

class Sondering:
    '''
    De Sondering class bevat informatie over een sondering. De volgende waarden zijn hier opgeslagen
    id:        ID van de sondering 
    mv:        Het maaiveld van de sondering
    x:         De x-coordinaat in RD stelsel
    y:         De y=coordinaat in RD stelsel
    zmin:      De maximale diepte van de sondering in m tov ref
    date:      De uitvoeringsdatum
    values:    Een lijst met rijen in de vorm van [z, qc, pw, wg]
    '''
    def __init__(self):
        '''
        Initialisatie van de class.
        '''
        self.id = -1
        self.mv = 0.0
        self.x = 0.0
        self.y = 0.0        
        self.zmin = 0.0
        self.date = datetime.datetime(1900,1,1)
        self.values = [] #z, qc, pw, wg  
    
    def dataAsText(self):
        '''
        Maakt een tekstlijn van de data voor uitvoer van de meetgegevens naar bv csv.
        returns: lijst met strings
        '''
        result = "z [m tov ref];qc [MPa];fs [MPa];wg [%]\n"
        for z, qc, pw, wg in self.values:
            result += "%.2f;%.3f;%.3f;%.3f\n" % (z, qc, pw, wg)
        return result  

    def blobToData(self, data):
        lines = data.split('\n')
        self.values = []

        for i in range(1, len(lines)):
            line = lines[i]
            if len(line.strip())>0:
                z, qc, pw, wg = line.split(';')
                self.values.append([float(z),float(qc),float(pw),float(wg)])
    
    def getLatitude(self): 
        '''
        Geeft de latitude van de sondering in WGS84 coordinaten.
        returns: double
        '''   
        lat, lon = latlon.RDToLatLon(self.x, self.y)
        return lat
    
    def getLongitude(self):
        '''
        Geeft de longitude van de sondering in WGS84 coordinaten.
        returns: double
        ''' 
        lat, lon = latlon.RDToLatLon(self.x, self.y)
        return lon    
        
    def readFromFile(self, filename):
        '''
        Leest een sondering in vanuit een GEF bestand. 
        returns: string met eventuele foutmelding of `none` als er geen fout is gevonden.
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
                    self.mv = float(args[1].strip()) 
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
                                  
                        self.values.append([(self.mv-abs(dz)), qc, pw, wg])
                else:
                    return "ERROR: Found gef file %s of type %s" % (filename, typegef)
        
        self.zmin = self.values[len(self.values)-1][0]
        return "none"
