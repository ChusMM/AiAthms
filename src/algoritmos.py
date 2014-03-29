# -*- coding: utf-8 -*-
# Métodos de búsqueda no informada, A* y temple simulado 
# Jesús Manuel Muñoz Mazuecos, Ingeniería Informática  (Inteligencia artificial)
import sys
import csv
import time
import random
import math
from nodo import nodo
from coordenada import coordenada
from solucion import solucion
from pygraph.classes.graph import graph
from bisect import bisect_left
from bisect import insort

class algoritmos:
    
    def __init__(self):
        self.l = []        # Lista ordenada
        self.keys = [None] # Lista de claves
        # Atributos para recoger estadísticas
        self.nelementos = 0.0
        self.SumTime = 0.0
        self.Tinicio = 0.0
        self.encontrado = 0
        self.tiempo = 0.0
        self.destino = ''
        self.tMedio = 0.0
        
    def buscar(self, g, src, dst, lim, modo): # Método para buscar
        camino = []  # Lista en donde guardamos los nodos que se eligen
        algoritmos.__inicializarGlobals(self)
        llave = 0
        self.encontrado = 0
        self.destino = dst
        
        # preparativos para nuestra lista ordenada
        elegido = nodo(modo, None, src, 1, 0.0, 0.0)
        self.l.append(elegido)
        self.keys[0] = self.l[0].valor
        
        # inicializo la lista de visitados
        visitados = []
        visitados.append(elegido.state.IDVertex)
        
        while len(self.l) != 0:
            llave = 0
            # Coger el 1º
            elegido = self.l[0]
            camino.append(elegido)
            # Eliminar el 1º
            self.l.remove(elegido)
            self.keys.remove(elegido.valor)
            if elegido.state.IDVertex == dst:
                if modo == 3: # condición para abortar la profundidad iterativa
                    self.encontrado = 1
                sol = solucion([], 0.0)
                sol.camino, sol.valoracion = algoritmos.__trayecto(self, modo, camino, g)
                return sol # Objeto de la clase solucion
            else:
                #   Condiciones necesarias en el caso de que haya límite de profundidad
                if (modo == 2 or modo == 3) and elegido.state.profundidad < lim:
                    llave = 1
                if modo == 0 or modo == 1 or modo == 4 or modo == 5 or modo < 0:
                    llave = 1
                    
                if llave:
                    # Lista de sucesores sin visitados
                    sucesores = algoritmos.__listaVecinos(self, g, elegido.state.IDVertex, visitados)
                    # Insertar sucesores
                    for sucesor in sucesores:
                        algoritmos.__insertar(self, g, elegido, sucesor, modo)
                        visitados.append(sucesor)
                        
        if modo == 3 and self.encontrado == 0:
            sol = algoritmos.buscar(self, g, src, dst, lim + 1, modo)
            return sol

    def templeSimulado(self, g, src, dst):
        T = 100.0
        alpha = 0.6
        it = 2
        solActual = solucion([], 100000.0) # Incial...
        solCandidata = solucion([], 0.0)
        solFinal = solucion([], 0.0)
        # Solución inicial
        nodoActual = nodo(6, None, src, 0, solActual.valoracion, 0.0)
        # Solucion Inicial(Final)
        solFinal.camino = [] 
        solFinal.valoracion = 100000.0
        t0 = time.time();
        # Temple simulado ...
        while T > 0.1:
            for i in range(it):
                # Selecciona un sucesor aleatorio
                cand = algoritmos.__randSucesor(self, g, nodoActual.state.IDVertex)
                # Se devuelve una solución vecina
                solCandidata = algoritmos.buscar(self, algoritmos.genGraph(self), cand, dst, 0, 5)
                # Creamos un tipo nodo que es el sucesor candidato
                nodoCandidato = nodo(6, nodoActual, 
                                        cand, 
                                        nodoActual.state.profundidad + 1, 
                                        solCandidata.valoracion, 
                                        0.0)
                # Devuelve la diferencia de valoraciones entre el nodo actual y el candidato
                # DE = - costeValoracionCandidata - (- costeValoraciónActual)
                DE = algoritmos.__difValor(self, solActual.valoracion, solCandidata.valoracion)
                # Si la valoración es mejor...
                if DE > 0:
                    # Actualizamos los valores de nodo actual y solución actual
                    solActual.camino = algoritmos.__anexionSol(self, solActual.camino, solCandidata.camino, nodoActual.state.IDVertex)
                    solActual.valoracion = algoritmos.__evalSol(self, g, solActual.camino)
                    nodoActual = nodoCandidato   
                else:
                    # Se calcula el fator de probabilidad
                    u = random.randint(0, 1)
                    if u <= math.pow(math.e, DE / T):
                        # Actualizamos los valores de nodo actual y solución actual
                        solActual.camino = algoritmos.__anexionSol(self, solActual.camino, solCandidata.camino, nodoActual.state.IDVertex)
                        solActual.valoracion = algoritmos.__evalSol(self, g, solActual.camino)
                        nodoActual = nodoCandidato
                        
            # Si es una solución más óptima la seleccionamos como final
            if solActual.valoracion < solFinal.valoracion:
                solFinal.camino = solActual.camino
                solFinal.valoracion = solActual.valoracion
            # Decrementar la temperatura por un factor alpha
            T = alpha * T
            # Incrementar el número de iteraciones
            it = it + 2
        tf = time.time() - t0;
        return solFinal, tf
        
    def __insertar(self, g, padre, vertice, modo):
        # factor de maximizar y minimizar
        if modo >= 0:
            factor = 1.0
        else: 
            factor = -1.0
        # calulo del costo
        costoArista = algoritmos.__calcularCosto(self, g, padre.state.IDVertex, vertice, factor)
        costo = padre.state.costo + costoArista
        
        # calculamos la distancia euclidea...
        distancia = algoritmos.__euclidea(self, vertice, self.destino)
        
        # se crea un tipo nodo para insertar en la lista
        nd = nodo(modo, padre, vertice, padre.state.profundidad + 1, costo, distancia)            
        
        # INSERCIÓN EN LA LISTA
        tIniIns = time.time()
        pos = bisect_left(self.keys, nd.valor)
        self.l.insert(pos, nd)
        insort(self.keys, nd.valor)
        self.SumTime = + (time.time() - tIniIns)
        # FIN INSERCIÓN
        
        self.nelementos = self.nelementos + 1
        
    def __anexionSol(self, actual, candidata, vertice):
        l = []
        for elem in actual:
            if elem == vertice:
                break
            l.append(elem)
        l.append(vertice)
        return l + candidata

    def __evalSol(self, g, camino):
        costo = 0.0
        for i in range(len(camino) - 1):
            costo += algoritmos.__calcularCosto(self, g, camino[i], camino[i + 1], 1.0)
        return costo

    def __randSucesor(self, g, nodo):
        sucesores = g.neighbors(nodo)
        n = random.randint(0, len(sucesores) - 1)
        sucesor = sucesores[n]
        return sucesor
        
    def __difValor(self, valorActual, valorCandidato):
        return ((-1.0) * valorCandidato) - ((-1.0) * valorActual)

    def __euclidea(self, origen, destino):
        csvReader = csv.reader(open('nodes.csv', 'rb'))
        for row in csvReader:
            # Aquí se extraen las coordenadas del .csv
            if row[0] == origen:
                src = coordenada(row[0], math.fabs(float(row[1])), math.fabs(float(row[2])))
            if row[0] == destino:
                dst = coordenada(row[0], math.fabs(float(row[1])), math.fabs(float(row[2])))
        # El radio de la tierra... 
        Rt = 6371.0
        # (X2 - X1), (Y2 - Y1) y pasarlos a radianes
        delta = math.fabs(dst.latitud - src.latitud) * math.pi / 180.0
        teta = math.fabs(dst.longitud - src.longitud) * math.pi / 180.0
        # Sustituir en la formula
        distancia = 2.0 * Rt * math.sqrt(math.pow(math.sin(delta / 2.0), 2) + math.pow(math.sin(teta / 2.0), 2))
        return 0.2 * (distancia * 1000) # devolver la distancia en metros
        
    def __listaVecinos(self, g, n, visitados):
        vecinos = g.neighbors(n)
        # eliminar los visitados
        for vertex in vecinos:
            if visitados.count(vertex) != 0:
                vecinos.remove(vertex)
                    
        return vecinos

    def __calcularCosto(self, g, src, dst, factor):
        d = g.edge_weight((src, dst))
        attr = g.edge_attributes((src, dst))
        if factor > 0: # Maximizar o minimizar
            c = 0.8 * (d + 1000.0) # + attr[0] + attr[1])
        else:
            c = (attr[0] + attr[1]) - d * 1000.0
        return c
        
    def __inicializarGlobals(self):
        self.l = []
        self.keys = [None]
        self.nelementos = 0.0
        self.SumTime = 0.0
        self.Tinicio = time.time()
        self.encontrado = 0
        self.tiempo = 0.0
        self.destino = ''
        self.tMedio = 0.0
        
    def __trayecto(self, modo, camino, g):
        algoritmos.__verTipo(self, modo, camino)
        s = []
        camino.reverse()
        
        s.append(camino[0].state.IDVertex)
        n = camino[0].father
        
        while n != None:
            s.insert(0, n.state.IDVertex)
            n = n.father
            
        costo = algoritmos.__evalSol(self, g, s);
        print 'Costo Total: %s' %(costo)
        print s
        
        algoritmos.__stats(self)
        algoritmos.__separador(self)
        
        return s, costo
        
    def __stats(self):
        if self.nelementos == 0: # Evita la división entre cero en el caso que no se genere nada
            self.nelementos = 1
        
        self.tiempo = time.time() - self.Tinicio
        self.tMedio = self.SumTime / self.nelementos
        # Estadísticas en consola
        print 'Estadísticas:'
        print 'Elementos generados: %d' %(self.nelementos)
        print 'Tiempo medio de inserción: %.4e segundos' %(self.tMedio)
        print 'Todo ello en: %.3f segundos' %(self.tiempo)

    def __verTipo(self, modo, camino):
        if modo == 0:   # anchura
            print 'Recorrido en Anchura'
        elif modo == 1: # profundidad
            print 'Recorrido en Profundidad'
        elif modo == 2: # profundidad acotada
            print 'Recorrido en Profundidad Acotada'
        elif modo == 3: # profundidad iterativa
            print 'Recorrido en Profundidad Iterativa'
        elif modo == 4: # costo
            print 'Recorrido en Costo Uniforme'
        elif modo == 5: # A*
            print 'Recorrido mediante A*'
        elif modo == 6: # Temple simulado
            print 'Recorrido mediante temple simulado'
        
    def __separador(self):
        print '--------------------------------------------------------'
        
    def genGraph(self):
        g = graph()
        csvReader = csv.reader(open('arcs.csv', 'rb'))
        for row in csvReader:                      # Cada fila es una arista 
            algoritmos.__addVertex(self, g, row)   # añadir vertice
            algoritmos.__addEdge(self, g, row)     # añadir arista    
        return g
        
    def __addVertex(self, g, row):
        for i in range(2):
            if g.has_node(row[i]) == False:
                g.add_node(row[i])
        
    def __addEdge(self, g, row):
        attr = [0.0, 0.0]       # lista de dos elementos que contiene los bares y comercios 
                                # l[0] -> bares, l[1] -> comercios
        d = float(row[2])       # distancia
        attr[0] = float(row[3]) # bares 
        attr[1] = float(row[4]) # tiendas
        label = row[5]          # nombre de la calle
        g.add_edge((row[0], row[1]), d, label, attr)
    
