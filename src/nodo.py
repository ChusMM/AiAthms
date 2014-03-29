# -*- coding: utf-8 -*-
import sys
from estado import estado
class nodo:
    def __init__(self, criterio = 0, father = None, IDVertex = '', profundidad = 0, costo = 0.0, euclidea = 0.0):
        if criterio == 0:                                     # anchura
            self.valor = float(profundidad)
        elif criterio == 1 or criterio == 2 or criterio == 3: # profundidades
            self.valor = -1.0 * float(profundidad)
        elif criterio == 4:                                   # costo uniforme
            self.valor = costo
        elif criterio == -4:                                  # costo(Maximizar) 
            self.valor = -1.0 * costo                         
        elif criterio == 5:                                   # A*
            self.valor = costo + euclidea
        elif criterio == -5:                                  # A*(Maximizar)
            self.valor = -1.0 * costo
        elif criterio == 6:                                   # Temple simulado
            self.valor = costo
        else:
            print "Criterio no válido"
            sys.exit(-1)
            
        self.father = father
        self.state = estado(IDVertex, profundidad, costo, euclidea)
        
    def getValor(self):
        return self.valor
  
    def getFather(self):
        return self.father
  
    def getState(self):
        return self.state
  
    def setValor(self, valor):
        self.valor = valor
    
    def setFather(self, father = None):
        self.father = father
  
    def setState(self, state = None):
        self.state = state