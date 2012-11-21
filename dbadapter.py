'''
Created on 8 nov. 2012

De adapterklasse tussen de sqlite3 database en eventuele logica die met de data aan de slag wil.

@author: breinbaas
'''

import sqlite3, sondering, opbouw, datetime

class DBAdapter:
    '''
    Dit is de database adapter tussen de dijkwachter sqlite database
    en alle aanroepende programma's
    '''
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename

    def open(self):
        try:
            self.connection = sqlite3.connect(self.filename)
            self.cursor = self.connection.cursor()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def deleteAllSonderingen(self):
        pass #TODO: implement

    def getMaxIDFromSonderingen(self):
        '''
        Zoekt de hoogste id op in de lijst met sonderingen.
        returns: int
        '''
        self.cursor.execute('SELECT max(id) FROM sondering')
        args = self.cursor.fetchone()
        if args[0] != None:
            return int(args[0])
        else:
            return -1

    def getMaxIDFromOpbouw(self):
        '''
        Zoekt de hoogste id op in de lijst met sonderingen.
        returns: int
        '''
        self.cursor.execute('SELECT max(id) FROM sondering')
        args = self.cursor.fetchone()
        if args[0] != None:
            return int(args[0])
        else:
            return -1

    def getSonderingAt(self, x, y):
        self.cursor.execute("SELECT * FROM sondering where x=%s AND y=%s" % (x,y))
        return self.cursor.fetchone()

    def addSondering(self, deSondering, deOpbouwId):
        self.cursor.execute('INSERT INTO sondering VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (deSondering.id, deSondering.date, deSondering.x, deSondering.y,
                             deSondering.mv, deSondering.zmin, sqlite3.Binary(deSondering.dataAsText()),
                             deOpbouwId, deSondering.getLatitude(), deSondering.getLongitude(), deSondering.naam))

    def addOpbouw(self, deOpbouw):
        self.cursor.execute('INSERT INTO opbouw VALUES(?, ?, ?)', (deOpbouw.id, sqlite3.Binary(deOpbouw.asText()), deOpbouw.bron))

    def getSonderingById(self, id):
        '''
        Geeft een sondering terug met de bijbehorende id en None als er niks gevonden is.
        '''
        result = None
        self.cursor.execute('SELECT * FROM sondering WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            s = sondering.Sondering()
            s.id = int(row[0])
            s.date = row[1] #TODO: inlezen datetime
            s.x = float(row[2])
            s.y = float(row[3])
            s.mv = float(row[4])
            s.zmin = float(row[5])
            s.blobToData(str(row[6]))
            s.naam=str(row[10])
            return s

    def getAllSonderingen(self):
        '''
        Geeft een lijst met alle Sondering classes terug die in de database
        gevonden zijn.
        returns: lijst met Sondering classes
        '''
        result = []
        self.cursor.execute('SELECT * FROM sondering')
        rows = self.cursor.fetchall()
        for r in rows:
            s = sondering.Sondering()
            s.id = int(r[0])
            s.date = r[1] #TODO: inlezen datetime
            s.x = float(r[2])
            s.y = float(r[3])
            s.mv = float(r[4])
            s.zmin = float(r[5])
            s.blobToData(str(r[6]))

            result.append(s)

        return result

    def getOpbouwById(self, id):
        '''
        Geeft een opbouw terug met de bijbehorende id en None als er niks gevonden is.
        '''
        result = None
        self.cursor.execute('SELECT * FROM opbouw WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            result = opbouw.Opbouw()
            result.id = int(row[0])
            result.blobToData(str(row[1]))
            return result

    def getGrondsoortById(self, id):
        '''
        Geeft en grondlaag terug.
        '''
        result = None
        self.cursor.execute('SELECT * FROM grondsoort WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            import grondsoort
            result = grondsoort.Grondsoort()

            def setUnknownIfNone(value):
                if value == None:
                    return -1.0 #all parameters should be >=0 so -1 is used if a value is unknown (and thus empty in the database)
                else:
                    return float(value)

            result.id = int(row[0])
            result.naam = str(row[1])
            result.omschrijving = str(row[2])
            result.bron = str(row[3])
            result.yd = setUnknownIfNone(row[4])
            result.yn = setUnknownIfNone(row[5])
            result.c = setUnknownIfNone(row[6])
            result.phi = setUnknownIfNone(row[7])
            result.upsilon = setUnknownIfNone(row[8])
            result.k = setUnknownIfNone(row[9])
            result.MC_upsilon = setUnknownIfNone(row[10])
            result.MC_E50 = setUnknownIfNone(row[11])
            result.HS_E50 = setUnknownIfNone(row[12])
            result.HS_Eoed = setUnknownIfNone(row[13])
            result.HS_Eur = setUnknownIfNone(row[14])
            result.HS_m = setUnknownIfNone(row[15])
            result.SSC_lambda = setUnknownIfNone(row[16])
            result.SSC_kappa = setUnknownIfNone(row[17])
            result.SSC_mu = setUnknownIfNone(row[18])
            result.Cp = setUnknownIfNone(row[19])
            result.Cs = setUnknownIfNone(row[20])
            result.Cap = setUnknownIfNone(row[21])
            result.Cas = setUnknownIfNone(row[22])
            result.cv = setUnknownIfNone(row[23])
            result.kleur = str(row[24])
            return result

    def close(self):
        self.connection.commit()
        self.cursor.close()


if __name__=="__main__":
    db = DBAdapter("c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite")
    db.open()
    s = db.getSonderingById(1220)
    opb = db.getOpbouwById(1220)
    g = db.getGrondsoortById(2)
    db.close()



