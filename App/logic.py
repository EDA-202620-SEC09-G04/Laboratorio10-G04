"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as m
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfs as DFS
from DataStructures.Graph import bfs as BFS
from DataStructures.Graph import dijkstra as DIJKSTRA
import csv
import time
import os

data_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data')


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = new_analyzer()
    return analyzer


def new_analyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar la información de las paradas
   connections: Grafo para representar las rutas entre estaciones
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(
            num_elements=8000, load_factor=0.7, prime=109345121)

        analyzer['connections'] = G.new_graph(order=20000)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_services(analyzer, servicesfile, stopsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    stops_path = os.path.join(data_dir, stopsfile)
    with open(stops_path, encoding="utf-8", newline="") as file:
        for stop in csv.DictReader(file, delimiter=","):
            add_stop(analyzer, stop)

    services_path = os.path.join(data_dir, servicesfile)
    lastservice = None
    with open(services_path, encoding="utf-8", newline="") as file:
        for service in csv.DictReader(file, delimiter=","):
            vertex = format_vertex(service)
            if not G.contains_vertex(analyzer['connections'], vertex):
                add_stop_vertex(analyzer, vertex)
            add_route_stop(analyzer, service)

            if lastservice is not None:
                sameservice = lastservice['ServiceNo'] == service['ServiceNo']
                samedirection = (
                    lastservice['Direction'] == service['Direction'])
                samebusStop = (
                    lastservice['BusStopCode'] == service['BusStopCode'])
                if sameservice and samedirection and not samebusStop:
                    add_stop_connection(analyzer, lastservice, service)

            add_same_stop_connections(analyzer, service)
            lastservice = service

    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def total_stops(analyzer):
    """
    Total de paradas de autobus en el grafo
    """
    return G.order(analyzer['connections'])


def total_connections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return G.size(analyzer['connections'])


# Funciones para la medición de tiempos

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def add_stop_connection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(lastservice)
        destination = format_vertex(service)
        clean_service_distance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        add_connection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        return exp


def add_stop(analyzer, stop):
    """
    Adiciona una parada (BusStopCode) en los stops del sistema de transporte
    """
    stop['services'] = lt.new_list()
    m.put(analyzer['stops'], stop['BusStopCode'], stop)
    return analyzer

def add_stop_vertex(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """

    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])
    stop_services = stop_info['services']
    compare_services = lambda service_1, service_2: (
        0 if service_1 == service_2 else -1)
    if lt.is_present(
            stop_services, service['ServiceNo'], compare_services) == -1:
        lt.add_last(stop_services, service['ServiceNo'])

    return analyzer


def add_connection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """

    G.add_edge(analyzer['connections'], origin, destination, distance)



def add_same_stop_connections(analyzer, service):
    stop_1 = format_vertex(service)
    stop_buses_lt = m.get(analyzer['stops'], service['BusStopCode'])['services']

    if lt.size(stop_buses_lt) > 1:
        pass

    node = stop_buses_lt['first']
    for _ in range(lt.size(stop_buses_lt)):
        stop_2 = format_vertex({'BusStopCode': service['BusStopCode'], 'ServiceNo': node['info']})
        if stop_1 != stop_2:
            add_connection(analyzer, stop_1, stop_2, 0)
        node = node['next']
    return analyzer


# ___________________________________________________
#  Funciones de resolución de requerimientos
# ___________________________________________________

def get_most_concurrent_stops(analyzer):
    """
    Retorna hasta cinco vertices con mas arcos entrantes y salientes.

    Cada elemento contiene el identificador del vertice y su grado total.
    """
    graph = analyzer['connections']
    vertices = G.vertices(graph)
    total_vertices = al.size(vertices)
    
    if total_vertices == 0:
        return al.new_list()
    
    incoming_degrees = m.new_map(
        num_elements=max(1, total_vertices), load_factor=0.5)

    for index in range(total_vertices):
        origin = al.get_element(vertices, index)
        adjacent_vertices = G.adjacents(graph, origin)

        for adjacent_index in range(al.size(adjacent_vertices)):
            destination = al.get_element(adjacent_vertices, adjacent_index)
            incoming_degree = m.get(incoming_degrees, destination)
            if incoming_degree is None:
                incoming_degree = 0
            m.put(incoming_degrees, destination, incoming_degree + 1)

    ranked_stops = al.new_list()

    for index in range(total_vertices):
        vertex = al.get_element(vertices, index)
        total_degree = G.degree(graph, vertex)
        incoming_degree = m.get(incoming_degrees, vertex)
        if incoming_degree is not None:
            total_degree += incoming_degree
        al.add_last(ranked_stops, (vertex, total_degree))

    def sort_by_out_degree(stop1, stop2):
        if stop1[1] != stop2[1]:
            return stop1[1] > stop2[1]
        return str(stop1[0]) < str(stop2[0])

    al.merge_sort(ranked_stops, sort_by_out_degree)

    most_concurrent = al.new_list()
    for index in range(min(5, al.size(ranked_stops))):
        al.add_last(most_concurrent, al.get_element(ranked_stops, index))

    return most_concurrent

def get_vertices_for_stop(analyzer, stop): #Función auxiliar

    graph = analyzer['connections']
    result_list = al.new_list()
    if G.contains_vertex(graph, stop):
        al.add_last(result_list, stop)
    else:
        stop_info = m.get(analyzer['stops'], stop)
        if stop_info is not None:
            services = stop_info['services']
            node = services['first']
            
            for _ in range(lt.size(services)):
                bus = node['info']
                vertex = str(stop) + '-' + str(bus)
                if G.contains_vertex(graph, vertex):
                    al.add_last(result_list, vertex)
                node = node['next']
    return result_list

def get_route_between_stops_dfs(analyzer, stop1, stop2):
    """
    Retorna una ruta DFS entre dos paradas, o None si no existe.

    Cada parada puede ser una llave de vertice o un BusStopCode.
    """
    graph = analyzer['connections']
    origin_vertices = get_vertices_for_stop(analyzer, stop1)
    destination_vertices = get_vertices_for_stop(analyzer, stop2)
    
    if al.is_empty(origin_vertices) or al.is_empty(destination_vertices):
        return None
    
    for i in range(al.size(origin_vertices)):
        origin = al.get_element(origin_vertices, i)
        search = DFS.dfs(graph, origin)
        
        for j in range(al.size(destination_vertices)):
            destination = al.get_element(destination_vertices, j)
            path = DFS.path_to(destination, search)
            if path is not None:
                return path
    return None

def get_route_between_stops_bfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos parada usando bfs
    """
    graph = analyzer['connections']
    origin_vertices = get_vertices_for_stop(analyzer, stop1)
    destination_vertices = get_vertices_for_stop(analyzer, stop2)
    
    if al.is_empty(origin_vertices) or al.is_empty(destination_vertices):
        return None
    
    for i in range(al.size(origin_vertices)):
        origin = al.get_element(origin_vertices, i)
        search = BFS.bfs(graph, origin)
        
        for j in range(al.size(destination_vertices)):
            destination = al.get_element(destination_vertices, j)
            path = BFS.path_to(destination, search)
            if path is not None:
                return path
    return None

def get_shortest_route_between_stops(analyzer, stop1, stop2):
    """
    Obtener la ruta mínima entre dos paradas
    """
    graph = analyzer['connections']
    origin_vertices = get_vertices_for_stop(analyzer, stop1)
    destination_vertices = get_vertices_for_stop(analyzer, stop2)
    
    if al.is_empty(origin_vertices) or al.is_empty(destination_vertices):
        return None
    
    best_path = None
    min_distance = float("inf")
    best_structure = None
    
    for i in range(al.size(origin_vertices)):
        origin = al.get_element(origin_vertices, i)
        search_structure = DIJKSTRA.dijkstra(graph, origin)
        
        for j in range(al.size(destination_vertices)):
            destination = al.get_element(destination_vertices, j)
            distance = DIJKSTRA.dist_to(destination, search_structure)
            if distance < min_distance:
                min_distance = distance
                best_path = DIJKSTRA.path_to(destination, search_structure)
                best_structure = search_structure
                
    analyzer['paths'] = best_structure
    return best_path

def show_calculated_shortest_route(analyzer, destination_stop):
    # (Opcional) TODO: Mostrar en un mapa la ruta mínima entre dos paradas usando folium
    ...




# ___________________________________________________
# Funciones Helper
# ___________________________________________________

def clean_service_distance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def format_vertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name
