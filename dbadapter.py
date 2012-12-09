#-------------------------------------------------------------------------------
# Name:        dbadapter
# Purpose:
#
# Author:      breinbaas
#
# Created:     29-11-2012
# Copyright:   (c) breinbaas 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
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
    def __init__(self, filename=""):
        '''
        Constructor
        '''
        #TODO: switch to the right database depending on the platform
        if filename == "":
            filename = "c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite"
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

    def getNumCPTs(self):
        self.cursor.execute('SELECT COUNT(*) FROM cpt')
        args = self.cursor.fetchone()
        if args[0] != None:
            return int(args[0])
        else:
            return -1

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

    def getCPTandVSoil(self, index):
        '''Returns the cpt and the connected vsoil (if any) at the given index
        or None if the index is invalid.'''
        cpt = None
        vsoil= None
        self.cursor.execute("SELECT id, vsoil_id FROM cpt LIMIT 1 OFFSET %d" % index)
        args = self.cursor.fetchone()
        if args[0] != None:
            cpt = self.getCPTById(int(args[0]))
            vsoil = self.getVSoilById(int(args[1]))
            return cpt, vsoil
        else:
            return None, None

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

    def getAllSoiltypes(self):
        '''
        Return a list with all Soiltypes found in the database.
        '''
        result = []
        self.cursor.execute('SELECT id FROM soiltypes')
        rows = self.cursor.fetchall()
        for r in rows:
            st = self.getSoiltypeById(int(r[0]))
            result.append(st)

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

    def updateVSoil(self, vsoil):
        self.cursor.execute('UPDATE vsoil SET source=?, data=? WHERE id=?', (vsoil.source, sqlite3.Binary(vsoil.asText()), vsoil.id))
        self.connection.commit()

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
            def setUnknownIfNone(value):
                if value == None:
                    return -1.0 #all parameters should be >=0 so -1 is used if a value is unknown (and thus empty in the database)
                else:
                    return float(value)
            result = soiltype.SoilType()
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

    def getAllOedmeterTests(self):
        '''
        Returns oedemetertest with an optional filter.
        '''
        results = []
        self.cursor.execute('SELECT * FROM oedometer_tests')
        rows = self.cursor.fetchall()

        def setUnknownIfNone(value):
            if value == None:
                return -1.0 #all parameters should be >=0 so -1 is used if a value is unknown (and thus empty in the database)
            else:
                return float(value)

        import oedometertest
        for r in rows:
            oed = oedometertest.OedometerTest()
            oed.id = int(r[0])
            oed.soiltype = str(r[1])
            oed.ysat = float(r[2])
            oed.p0 = setUnknownIfNone(r[3])
            oed.pg = setUnknownIfNone(r[4])
            oed.cp = float(r[5])
            oed.cs = float(r[6])
            oed.cap = float(r[7])
            oed.cas = float(r[8])
            oed.cv = float(r[9])
            oed.a = setUnknownIfNone(r[10])
            oed.b = setUnknownIfNone(r[11])
            oed.c = setUnknownIfNone(r[12])
            oed.depth = float(r[13])
            oed.borhole = str(r[14])
            results.append(oed)

        return results

    def close(self):
        self.connection.commit()
        self.cursor.close()


if __name__=="__main__":
    db = DBAdapter()
    db.open()
    cpt = db.getCPTById(2)
    vs = db.getVSoilById(2)
    #vs.source = "Testing"
    #db.updateVSoil(vs)
    g = db.getSoiltypeById(2)
    c = db.getColors()
    sts = db.getAllSoiltypes()
    oeds = db.getAllOedmeterTests()

    print cpt, vs, g, c, sts, oeds
    db.close()



