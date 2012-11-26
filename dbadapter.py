'''
Created on 8 nov. 2012

The adapter that stands between the sqlite database and the applications using
the database. Contains methods for data retrieval and storage.

@author: breinbaas
'''

import sqlite3, cpt, vsoil, datetime

class DBAdapter:
    '''
    The adapter between the sqlite3 database with geotechnical information.
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

    def deleteAllCPTs(self):
        '''
        Delete all CPT files.
        '''
        pass #TODO: implement

    def getMaxIDFromCPT(self):
        '''
        Return the highest id (int) in the cpt table.
        '''
        self.cursor.execute('SELECT max(id) FROM cpt')
        args = self.cursor.fetchone()
        if args[0] != None:
            return int(args[0])
        else:
            return -1

    def getMaxIDFromVSoil(self):
        '''
        Return the highest id (int) in the vsoil table.
        '''
        self.cursor.execute('SELECT max(id) FROM vsoil')
        args = self.cursor.fetchone()
        if args[0] != None:
            return int(args[0])
        else:
            return -1

    def getCPTAt(self, x, y):
        self.cursor.execute("SELECT * FROM cpt where x=%s AND y=%s" % (x,y))
        return self.cursor.fetchone()

    def addCPT(self, theCPT, theVSoilId):
        self.cursor.execute('INSERT INTO cpt VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (theCPT.id, theCPT.date, theCPT.x, theCPT.y,
                             theCPT.zmax, theCPT.zmin, sqlite3.Binary(theCPT.dataAsText()),
                             theVSoilId, theCPT.getLatitude(), theCPT.getLongitude(), theCPT.name))

    def addVSoil(self, theVSoil):
        self.cursor.execute('INSERT INTO vsoil VALUES(?, ?, ?)', (theVSoil.id, theVSoil.source, sqlite3.Binary(theVSoil.asText())))

    def getCPTById(self, id):
        '''
        Return a CPT class with the corresponding id or None.
        '''
        result = None
        self.cursor.execute('SELECT * FROM cpt WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            c = cpt.CPT()
            c.id = int(row[0])
            c.date = row[1] #TODO: inlezen datetime
            c.x = float(row[2])
            c.y = float(row[3])
            c.zmax = float(row[4])
            c.zmin = float(row[5])
            c.blobToData(str(row[6]))
            c.name=str(row[10])
            return c

    def getAllCTPs(self):
        '''
        Return a list with all CPT's found in the database.
        Careful with large collections!
        '''
        result = []
        self.cursor.execute('SELECT * FROM cpt')
        rows = self.cursor.fetchall()
        for r in rows:
            c = cpt.CPT()
            c.id = int(r[0])
            c.date = r[1] #TODO: inlezen datetime
            c.x = float(r[2])
            c.y = float(r[3])
            c.mv = float(r[4])
            c.zmin = float(r[5])
            c.blobToData(str(r[6]))
            c.naam=str(row[10])
            result.append(c)

        return result

    def getVSoilById(self, id):
        '''
        Returns a VSoil object with the corresponding id or None.
        '''
        result = None
        self.cursor.execute('SELECT * FROM vsoil WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            result = vsoil.VSoil()
            result.id = int(row[0])
            result.source = str(row[1])
            result.blobToData(str(row[2]))
            return result

    def getColors(self):
        '''
        Returns a list of all colors [id, color] found in the vsoil table.
        '''
        result = []
        self.cursor.execute('SELECT id, color FROM soiltypes')
        rows = self.cursor.fetchall()
        for r in rows:
            result.append([r[0], r[1]])
        return result


    def getSoiltypeById(self, id):
        '''
        Returns a soiltype with the corresponding id or None.
        '''
        result = None
        self.cursor.execute('SELECT * FROM soiltypes WHERE id=%d' % (id))
        row = self.cursor.fetchone()
        if row[0] == None:
            return None
        else:
            import soiltype
            result = soiltype.SoilType()

            def setUnknownIfNone(value):
                if value == None:
                    return -1.0 #all parameters should be >=0 so -1 is used if a value is unknown (and thus empty in the database)
                else:
                    return float(value)

            result.id = int(row[0])
            result.name = str(row[1])
            result.description = str(row[2])
            result.source = str(row[3])
            result.ydry = setUnknownIfNone(row[4])
            result.ysat = setUnknownIfNone(row[5])
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
            result.color = str(row[24])
            return result

    def close(self):
        self.connection.commit()
        self.cursor.close()


if __name__=="__main__":
    db = DBAdapter("c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite")
    db.open()
    cpt = db.getCPTById(2)
    vs = db.getVSoilById(2)
    g = db.getSoiltypeById(2)
    c = db.getColors()
    print cpt, vs, g, c
    db.close()



