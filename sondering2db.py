'''
Created on 30 okt. 2012

Dit script importeert gef bestanden vanuit een directory in een sqlite database.
Het script importeert enkel sonderingen en slaat ze op in een vooraf gedefinieerde database
waarin 2 tabellen staan genaamd

sondering met opmaak
id, datum, x, y, zmax, zmin, data, opbouw_id, latitude, longitude

opbouw met opmaak
id, data

De data van de sonderingen bestaat uit een tekstuele lijst met de opbouw;
z [m tov ref];qc [MPa];fs [MPa];wg [%]
0.25;0.010;-9999.000;-9999.000
0.14;0.166;0.021;12.832
0.12;0.961;0.012;1.240
...

De data van de opbouw bestaat uit een tekstuele lijst met de opbouw;
van;tot;grondsoort_id
0.25;-1.66;0
-1.66;-1.78;1
-1.78;-1.88;5
...

Waarbij de grondsoort_id weer verwijst naar een grondsoorten tabel


@author: BreinBaas
'''

import sys, os, sondering, sondering2opbouw, dbadapter

#check if a path is given
searchpath = ""
if len(sys.argv)!=2:
    print "[WARNING] No path given to find the GEF files, using default."
    searchpath = "c:\\Users\\breinbaas\\Documents\\Breinbaas\\GEF\\"
else:
    searchpath = sys.argv[1]

#open a log file
logFile = open("log.txt", 'w')

#open the database
db = db_adapter.DBAdapter("c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite")
db.open()

#assign the id+1 to the first new entry
currentSonderingId = db.getMaxIDFromSonderingen() + 1
currentOpbouwId = db.getMaxIDFromOpbouw() + 1

#get the files from the path which is given as the first argument
os.chdir(searchpath)
onlyfiles = [ f for f in os.listdir(searchpath) if os.path.isfile(os.path.join(searchpath,f)) ]

def uniqueEntry(x,y):
    '''
    returns true if this entry has unique x,y coordinates
    '''
    return db.getSonderingAt(x, y) == None

def addEntry(gef, opbouw):
    db.addSondering(gef, opbouw.id)
    db.addOpbouw(opbouw)

#some progress values
i = 1
imax = len(onlyfiles)

#open all files and add if necessary
for filename in onlyfiles:
    print "Parsing (%d/%d (%s))" % (i, imax, filename)
    i+=1

    son = sondering.Sondering()
    son.id = currentSonderingId
    error = son.readFromFile(filename)

    if error != "none":
        logFile.write("[SKIPPED] file %s with error: %s\n" % (filename, error))
    elif son.x < 0 or son.x > 300000 or son.y < 270000 or son.y > 630000:
        logFile.write("[SKIPPED] file %s with x=%s, y=%s (strange coordinates)\n" % (filename, son.x, son.y))
    else:
        opbouw = sondering2opbouw.convertToInterval(son, 0.1)
        opbouw.id = currentOpbouwId
        opbouw.optimize()
        if uniqueEntry(son.x, son.y):
            addEntry(son, opbouw)
            currentOpbouwId+=1
            currentSonderingId+=1
            logFile.write("[ADDED] file %s with x=%s, y=%s.\n" % (filename, son.x, son.y))
        else:
            logFile.write("[SKIPPED] file %s with x=%s, y=%s because its not unique.\n" % (filename, son.x, son.y))

db.close()
logFile.close()

