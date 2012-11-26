'''
Created on 18 nov. 2012

@author: breinbaas
'''

class SoilType:
    '''
    A soiltype contains the following information:

    id:             id of the soiltype
    name:           short name of the soiltype (sand / clay / loam / peat etc.)
    description :   a longer descriptive name
    source:         source of the information
    ydry:           dry weight in kN/m3
    ysat:           saturated weight in kN/m3
    c:              cohesion kN/m2
    phi:            #TODO opzoeken angle of ... [degrees]
    upsilon:        #TODO opzoeken
    k:              permeability in [m/day]
    MC_upsilon:     PLAXIS MC model upsilon
    MC_E50:         PLAXIS MC model E50 [MPa]
    HS_E50:         PLAXIS HS model E50 [MPa]
    HS_Eoed:        PLAXIS HS model Eoedometer [MPa]
    HS_Eur:         PLAXIS HS model Eunload-reload [MPa]
    SSC_lambda:     PLAXIS SSC model lambda [-]
    SSC_kappa:      PLAXIS SSC model kappa [-]
    SSC_mu:         PLAXIS SSC model mu [-]
    Cp:             Compression index Cp [-]
    Cs:             Compression index Cs [-]
    Cap:            Compression index C'p [-]
    Cas:            Compression index C's [-]
    cv:             Cv value [#TODO opzoeken]
    color:          Color in HTML code, ie. #RRGGBB
    '''
    def __init__(self):
        '''
        Initialisation.
        '''
        self.id = -1
        self.name = ""
        self.description = ""
        self.source = ""
        self.ydry = 0.0
        self.ysat = 0.0
        self.c = 0.0
        self.phi = 0.0
        self.upsilon = 0.0
        self.k = 0.0
        self.MC_upsilon = 0.0
        self.MC_E50 = 0.0
        self.HS_E50 = 0.0
        self.HS_Eoed = 0.0
        self.HS_Eur = 0.0
        self.HS_m = 0.0
        self.SSC_lambda = 0.0
        self.SSC_kappa = 0.0
        self.SSC_mu = 0.0
        self.Cp = 0.0
        self.Cs = 0.0
        self.Cap = 0.0
        self.Cas = 0.0
        self.cv = 0.0
        self.color = "#ffffff"
