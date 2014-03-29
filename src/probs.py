# -*- coding: utf-8 -*-
from algoritmos import algoritmos
a = algoritmos()
g = a.genGraph()
sol, t = a.templeSimulado(g, '50013', '10505')
print sol.camino
print sol.valoracion
print t