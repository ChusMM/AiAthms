# -*- coding: utf-8 -*-
class estado:
    
    def __init__(self, IDVertex = '', profundidad = 0, costo = 0.0, euclidea = 0.0):
        self.IDVertex = IDVertex
        self.profundidad = profundidad
        self.costo = costo
        self.euclidea = euclidea
    
    def IDvertex(self):
        return self.IDVertex
    
    def getProfundidad(self):
        return self.profundidad
    
    def getCosto(self):
        return self.costo
    
    def getEuclidea(self):
        return self.euclidea
    
    def setIDvertex(self, IDVertex):
        self.IDVertex = IDVertex
        
    def setProfundidad(self, profundidad):
        self.profundidad = profundidad
        
    def setCosto(self, costo):
        self.costo = costo
    
    def setEuclidea(self, euclidea):
        self.euclidea = euclidea
    