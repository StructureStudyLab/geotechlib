'''
Created on 18 nov. 2012

@author: breinbaas
'''

class Grondsoort:
    '''
    Een grondsoort bevat de basisinformatie van een grondsoort
    id:             id van de grondsoort
    naam:           korte naam van de grondsoort (zand / klei / leem / veen etc.)
    omschrijving:   nadere beschrijving
    bron:           waar de informatie vandaan komt
    ydroog:         droog vol. gewicht in kN/m3
    ynat:           verzadigd vol. gewicht in kN/m3
    c:              cohesie kN/m2
    phi:            hoek van inwendige wrijving in graden
    upsilon:        #TODO opzoeken
    k:              doorlatendheid in [m/dag]
    MC_upsilon:     PLAXIS MC model upsilon
    MC_E50:         PLAXIS MC model E50 [MPa]
    HS_E50:         PLAXIS HS model E50 [MPa]
    HS_Eoed:        PLAXIS HS model Eoedometer [MPa]
    HS_Eur:         PLAXIS HS model Eunload-reload [MPa]
    SSC_lambda:     PLAXIS SSC model lambda [-]
    SSC_kappa:      PLAXIS SSC model kappa [-]
    SSC_mu:         PLAXIS SSC model mu [-]
    Cp:             Samendrukking parameter Cp [-]
    Cs:             Samendrukking parameter Cs [-]
    Cap:            Samendrukking parameter C'p [-]
    Cas:            Samendrukking parameter C's [-]
    cv:             Cv waarde [#TODO opzoeken]
    kleur           kleur van de grondsoort in HTML kleurcode #RRGGBB
    '''
    def __init__(self):
        '''
        Initialisatie van de class.
        '''
        self.id = -1
        self.naam = ""
        self.omschrijving = ""
        self.bron = ""
        self.ydroog = 0.0
        self.ynat = 0.0
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
        self.kleur = "#ffffff"
