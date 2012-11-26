'''
Created on 30 okt. 2012

This script imports GEF files from a directory into a sqlite database.

Needed tables

CPT with columns
id, date, x, y, zmax, zmin, data, vsoil_id, latitude, longitude, name

VSoil with columns
id, source, data

The data of the cpt is stored as a blob with the following layout;
z [m tov ref];qc [MPa];fs [MPa];wg [%]
0.25;0.010;-9999.000;-9999.000
0.14;0.166;0.021;12.832
0.12;0.961;0.012;1.240
...

The data of a vsoil is stored as a blob in the form of;
top;bottom;soiltype_id
0.25;-1.66;0
-1.66;-1.78;1
-1.78;-1.88;5
...

soiltype_id points to a soiltype in the database

@author: BreinBaas
'''

import sys, os, cpt, cpt2vsoil, dbadapter

#check if a path is given
searchpath = ""
if len(sys.argv)!=2:
    print "[WARNING] No path given to find the GEF files, using default."
    #searchpath = "c:\\Users\\breinbaas\\Documents\\Breinbaas\\GEF\\"
    searchpath = "c:\\Users\\breinbaas\\Documents\\Waternet\\DAM\\117X\\030 Sonderingen\\GEF\\"
else:
    searchpath = sys.argv[1]

#open a log file
logFile = open("log.txt", 'w')

#open the database
db = dbadapter.DBAdapter("c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite")
db.open()

#assign the id+1 to the first new entry
currentCPTId = db.getMaxIDFromCPT() + 1
currentVSoilId = db.getMaxIDFromVSoil() + 1

#get the files from the path which is given as the first argument
os.chdir(searchpath)
onlyfiles = [ f for f in os.listdir(searchpath) if os.path.isfile(os.path.join(searchpath,f)) ]

def uniqueEntry(x,y):
    '''
    returns true if this entry has unique x,y coordinates
    '''
    return db.getCPTAt(x, y) == None

def addEntry(cpt, vs):
    db.addCPT(cpt, vs.id)
    db.addVSoil(vs)

#some progress values
i = 1
imax = len(onlyfiles)

#open all files and add if necessary
for filename in onlyfiles:
    print "Parsing (%d/%d (%s))" % (i, imax, filename)
    i+=1

    c = cpt.CPT()
    c.id = currentCPTId

    import re
    insensitive_gef = re.compile(re.escape('.gef'), re.IGNORECASE)
    c.name = insensitive_gef.sub('', filename)

    #c.naam = filename.
    error = c.readFromFile(filename)

    if error != "none":
        logFile.write("[SKIPPED] file %s with error: %s\n" % (filename, error))
    elif c.x < 0 or c.x > 300000 or c.y < 270000 or c.y > 630000:
        logFile.write("[SKIPPED] file %s with x=%s, y=%s (strange coordinates)\n" % (filename, c.x, c.y))
    else:
        vs = cpt2vsoil.convertToInterval(c, 0.1)
        vs.id = currentVSoilId
        vs.source = "auto_generated"
        vs.optimize()
        if uniqueEntry(c.x, c.y):
            addEntry(c, vs)
            currentVSoilId+=1
            currentCPTId+=1
            logFile.write("[ADDED] file %s with x=%s, y=%s.\n" % (filename, c.x, c.y))
        else:
            logFile.write("[SKIPPED] file %s with x=%s, y=%s because its not unique.\n" % (filename, c.x, c.y))

db.close()
logFile.close()

