# -*- coding: utf-8 -*-
class solucion:
    def __init__(self, camino = [], valoracion = 0.0):
        
        self.camino = camino
        self.valoracion = valoracion
        
    def getCamino(self):
        return self.camino
 
    def getvaloracion(self):
        return self.valoracion
    
    def setCamino(self, camino):
        self.camino = camino
        
    def setValoracion(self, valoracion):
        self.valoracion = valoracion
    