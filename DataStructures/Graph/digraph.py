from DataStructures.Graph import dfo_structure as dfo
from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import edge as edg
from DataStructures.Graph import prim_structure as prim
from DataStructures.Graph import dijsktra_structure as dick
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al

def new_graph(order):
    """
        Crea un grafo dirigido vacío.
    """
    return {
        "vertices": mp.new_map(order, 0.5),
        "num_edges": 0,
    }

def get_vertex(my_graph,key_u):
    """
        Retorna la información completa del vértice con llave key_u
    """

    vertex = mp.get(my_graph,key_u)
    if vertex is None:
        return None
    return vertex

def insert_vertex(my_graph,key_u,info_u):
    """
        Inserta un vertice en el grafo dirigido ``my_graph`` con clave ``key_u`` y valor ``info_u``.
    """
    vertex = vtx.new_vertex(key_u,info_u)
    mp.put(my_graph["vertices"], key_u, vertex)
    return my_graph

def add_edge(my_graph,key_u,key_v,weight=1.0):

    vertex_u = mp.get(my_graph["vertices"],key_u)
    vertex_v = mp.get(my_graph["vertices"],key_v)
    
    if vertex_u is None or vertex_v is None:
        raise Exception("El vertice u no existe")

    arco = mp.get(vtx.get_adjacents(vertex_u),key_v)
    if arco is not None:
        edg.set_weight(arco,weight)
    else:
        vtx.add_adjacent(vertex_u,key_v,weight)
        my_graph["num_edges"] += 1

    return my_graph

def contains_vertex(my_graph,key_u):
    """
        Retorna True si hay un vertice "key_u" en el grafo, o False de lo contrario
    """
    vertex = mp.get(my_graph["vertices"],key_u)
    return vertex is not None

def order(my_graph):
    """
        Retorna la cantidad de vertices del grafo.
    """
    return mp.size(my_graph["vertices"])

def size(my_graph):
    """
        Retorna la cantidad de arcos del grafo.
    """
    return my_graph["num_edges"]

def vertices(my_graph):
    """
        Retorna una lista de llaves de todos los vértices del grafo.
    """
    return mp.key_set(my_graph["vertices"])

def update_vertex_info(my_graph,key_u,new_info_u):
    """
        Actualiza la información de un vértice llave key_u con la nueva info
    """
    vertex = mp.get(my_graph["vertices"],key_u)
    if vertex is not None:

        vtx.set_value(vertex,new_info_u)
    return my_graph

def degree(my_graph,key_u):
    """
        Retorna el grado de un vértice llave "key_u"
    """
    vertex = get_vertex(my_graph["vertices"],key_u)
    if vertex is None:
        raise Exception("El vertice no existe")

    return mp.size(vtx.get_adjacents(vertex))

def adjacents(my_graph,key_u):
    """
        Returna una lista con las llaves de los vertices adyacentes al
        vértice vertex con llave "key_u"
    """
    vertex = get_vertex(my_graph,key_u)
    if vertex is None:
        raise Exception("El vertice no existe")
    
    return mp.key_set(vtx.get_adjacents(vertex))

def edges_vertex(my_graph,key_u):

    """
        Retorna una lista con las llaves 
    """
    vertex = get_vertex(my_graph,key_u)
    if vertex is None:
        raise Exception("El vertice no existe")
    
    return mp.value_set(vtx.get_adjacents(vertex))

def get_vertex_information(my_graph,key_u):
    """
        Retorna la información (value) asociade al vértice con llave key_u
    """

    vertex = get_vertex(my_graph,key_u)
    if vertex is None:
        raise Exception("El vertice no existe")
    return vtx.get_value(vertex)