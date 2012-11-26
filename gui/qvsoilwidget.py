#-------------------------------------------------------------------------------
# Name:         qvsoilwidget
# Purpose:      displays a cpt file and if the cpt is linked to a soilstructure
#               the structure is drawn as well
#
# Author:       breinbaas
#
# Created:      23-11-2012
# Copyright:    (c) breinbaas 2012
# Licence:      GPL
#-------------------------------------------------------------------------------

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

qcmax = 30.
qcmin = 0.
pwmax = 0.2
pwmin = 0.0
wgmax = 10.
wgmin = 10.

class QVSoilWidget(QWidget):
    def __init__(self, cpt=None, vsoil=None, parent=None):
        """
        Initializer, sets up members.
        """
        super(QVSoilWidget, self).__init__(parent)
        #define some labels to show information on the widget
        self.lblZ =  QLabel(self)
        self.lblQc = QLabel(self)
        self.lblPw = QLabel(self)
        self.lblWg = QLabel(self)

        #use fontmetrics to assign the minimum width of the labels
        fm = QFontMetricsF(self.font())
        self.lblZ.setMinimumWidth(fm.width("z=-99.99m"))
        self.lblQc.setMinimumWidth(fm.width("99.9MPa"))
        self.lblPw.setMinimumWidth(fm.width("9.99MPa"))
        self.lblWg.setMinimumWidth(fm.width("99.9%"))

        #there are three graphics, each has a start and end point
        #these are (re)calculated at the resize event
        self.xstartqc = 0
        self.xendqc = 0
        self.xstartpw = 0
        self.xendpw = 0
        self.xstartwg = 0
        self.xendwg = 0

        #references to the cpt, colorlist and the vsoil object
        self.cpt = cpt
        self.colors = []
        self.vsoil = None

        #flags to display or hide the cpt and / or opbouw
        self.showVSoil = True
        self.showCPT = True

        #only expand and don't get to small
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setMinimumSize(self.minimumSizeHint())

        #information for the graphics
        self.margin = [20, 20, 30, 30] #top, bottom, left, right
        self.share = [0.6,0.2,0.2] #part of screen for qc, pw and wg (0.5 being 50%, total = max 100% = 1)
        self.border = 10 #distance between two graphs

        #activate mouse tracking or else the mousemove event is not tracked
        self.setMouseTracking(True)

    def resizeEvent(self, event=None):
        """
        Overridden resize event, recalculates all positions of the labels and
        the location where the graphs are drawn.
        """
        fm = QFontMetricsF(self.font())
        dx = self.width() - self.margin[2] - self.margin[3] - self.border * 2
        self.xstartqc = self.margin[2]
        self.xendqc = self.margin[2] + dx * self.share[0]
        self.xstartpw = self.xendqc + self.border
        self.xendpw = self.xstartpw + dx * self.share[1]
        self.xstartwg = self.xendpw + self.border
        self.xendwg = self.xstartwg + dx * self.share[2]
        self.lblQc.move(self.margin[2], self.height()-self.margin[1])
        self.lblPw.move(self.xstartpw, self.height()-self.margin[1])
        self.lblWg.move(self.xstartwg, self.height()-self.margin[1])
        self.lblZ.move(self.margin[2], self.margin[1] - fm.height())

    def getInfoFromPosition(self, ypos):
        """
        Returns the z, qc, pw and wg value at the given point (in px).
        Returns None, None, None, None if ypos is invalid
        """
        z = 0.
        qc = 0.
        wg = 0.
        pw = 0.

        z = self.cpt.zmax - (ypos - self.margin[0]) * \
            (self.cpt.zmax - self.cpt.zmin) / (self.height() - self.margin[0] - self.margin[1])

        qc, pw, wg = self.cpt.getValuesAt(z)
        return z, qc, pw, wg

    def mouseMoveEvent(self, event):
        """
        If the mouse is moving in the graph area information is shown of the
        values at the depth that the mouse is at.
        """
        x = event.pos().x()
        y = event.pos().y()

        if self.margin[2] <= x <= self.width() - self.margin[3] and \
            self.margin[0] <= y <= self.height() - self.margin[1]:
                z, qc, pw, wg = self.getInfoFromPosition(y)
                if qc != None:
                    self.lblQc.setText("%.1fMPa" % qc)
                    self.lblPw.setText("%.2fMPa" % pw)
                    self.lblWg.setText("%.1f%s" % (wg,"%"))
                    self.lblZ.setText("%.2fm" % z)
                else:
                    self.lblQc.setText("")
                    self.lblPw.setText("")
                    self.lblWg.setText("")
                    self.lblZ.setText("")

    def paintEvent(self, event=None):
        """
        Overridden paint event that displays the graphs.
        """
        if self.cpt==None or self.vsoil==None:
            return

        painter = QPainter(self)
        painter.setPen(Qt.black)

        if self.showVSoil:
            ymax = self.vsoil.soillayers[0][0]
            ymin = self.vsoil.soillayers[-1][1]
            dy = ymax - ymin
            sy = dy / (self.height() - self.margin[0] - self.margin[1]) #m / px

            y1 = self.margin[0]
            for g in self.vsoil.soillayers:
                x1 = self.margin[2]
                x2 = self.width() - self.margin[3]
                y2 = int(self.margin[0] + (ymax - g[1]) / sy)
                k = QColor()
                k.setNamedColor(self.colors[g[2]][1])
                painter.fillRect(x1,y1,x2-x1,y2-y1,QBrush(k))
                y1 = y2

        if self.showCPT:
            ymax = self.cpt.zmax
            ymin = self.cpt.zmin
            dy = ymax - ymin
            dx = self.width() - self.margin[2] - self.margin[3] - self.border * 2
            sy = dy / (self.height() - self.margin[0] - self.margin[1]) #m / px

            painter.setPen(Qt.black)

            #rectangles
            painter.drawRect(self.xstartqc, self.margin[0], (self.xendqc-self.xstartqc), self.height() - self.margin[0] - self.margin[1])
            painter.drawRect(self.xstartpw, self.margin[0], (self.xendpw-self.xstartpw), self.height() - self.margin[0] - self.margin[1])
            painter.drawRect(self.xstartwg, self.margin[0], (self.xendwg-self.xstartwg), self.height() - self.margin[0] - self.margin[1])

            #axis qc
            for i in range(1, 3):
                qc = i * 10
                x = self.xstartqc + qc / qcmax * (self.xendqc - self.xstartqc)
                painter.drawLine(x, self.margin[0], x, self.height()-self.margin[1])

            for i in range(0, len(self.cpt.values)):
                z, qc, pw, wg = self.cpt.values[i]

                if qc > qcmax:
                    qc = qcmax
                elif qc < 0.:
                    qc = 0.0

                if pw > pwmax:
                    pw = pwmax
                elif pw < 0.0:
                    pw = 0.0

                if wg > wgmax:
                    wg = wgmax
                elif wg < 0.0:
                    wg = 0.0

                y2 = int(self.margin[0] + (ymax - z) / sy)
                qcx2 = self.xstartqc + qc / qcmax * (self.xendqc - self.xstartqc)
                pwx2 = self.xstartpw + pw / pwmax * (self.xendpw - self.xstartpw)
                wgx2 = self.xstartwg + wg / wgmax * (self.xendwg - self.xstartwg)

                if i!=0:
                    painter.drawLine(qcx1,y1,qcx2,y2)
                    painter.drawLine(pwx1,y1,pwx2,y2)
                    painter.drawLine(wgx1,y1,wgx2,y2)

                y1 = y2
                qcx1 = qcx2
                pwx1 = pwx2
                wgx1 = wgx2

if __name__ == '__main__':
    import sys

    db = None
    #check of het windows pad in de omgevingsvariabele PYTHONPATH zit
    if sys.platform == "win32":
        if "C:\\GitHub\\geotechlib" not in sys.path: #toevoegen indien niet gevonden
            sys.path.append("C:\\GitHub\\geotechlib")
        import dbadapter
        db = dbadapter.DBAdapter("c:\\Users\\breinbaas\\Documents\\Databases\\dijkwachter.sqlite")
    else:
        print "Set up the path to the database on linux"
        sys.exit(1)

    db.open()
    cpt = db.getCPTById(0)
    vs = db.getVSoilById(0)
    colors = db.getColors()
    db.close()

    app = QApplication(sys.argv)
    form = QVSoilWidget()
    form.cpt = cpt
    form.vsoil = vs
    form.colors = colors
    form.setWindowTitle("QVSoilWidget")
    form.move(0, 0)
    form.show()
    form.resize(400, 400)
    app.exec_()

