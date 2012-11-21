'''
Created on 18 nov. 2012

@author: breinbaas
'''

class Grondsoort:
    '''
    Een grondsoort bevat de basisinformatie van een grondsoort
    id:    id van de grondsoort
    yd     droog vol. gewicht in kN/m3
    yn     nat vol. gewicht in kN/m3
    c      cohesie kN/m2
    phi    hoek van inwendige wrijving in graden
    kleur  kleur van de grondsoort in HTML kleurcode #RRGGBB
    '''
    def __init__(self, id, naam, yd, yn, c, phi, kleur):
        '''
        Initialisatie van de class.
        '''
        self.id = id
        self.naam = naam
        self.yd = yd
        self.yn = yn
        self.c = c
        self.phi = phi
        self.kleur = kleur
