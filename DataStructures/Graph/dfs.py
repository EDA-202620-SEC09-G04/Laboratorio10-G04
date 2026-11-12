from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import digraph as DG
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st

def dfs(my_graph,source):
    """
        Inicia un recorrido Depth First Search (DFS) sobre el grafo my_graph a partir de un vertice inicial con llave source.
        Esta es la función máscara para iniciar el recorrido recursivo usando la funcion auxiliar dfs_vertex(…). 
        Cada vertice alcanzable se agrega a un mapa con su llave y 
        como valor un diccionarion con la informacion {“marked”, “edge_from”}.
    """
    visited_map = mp.new_map(num_elements=17,load_factor=.5)
    vertex_start = DG.get_vertex(my_graph["vertices"], source)
    if vertex_start is None:
        raise ValueError("El vertice de inicio no existe en el grafo")

    mp.put(visited_map, source, {"marked": True, "edge_from": None})
    return dfs_vertex(my_graph,vertex_start,visited_map)

def dfs_vertex(my_graph,vertex,visited_map):
    """
        Funcion recursiva que permite obtener un recorrido DFS desde un vertice inicial. 
        La funcion aplica a los vertices adyacentes del vertice inicial. 
        Esta función es usada por la funcion depth_first_search. 
        Cada vertice alcanzable se agrega a un mapa con su llave y 
        como valor un diccionarion con la informacion {“marked”, “edge_from”}.
    """
    if vertex is None:
        raise ValueError("No se puede recorrer un vertice inexistente")

    neighbors = mp.key_set(vtx.get_adjacents(vertex))
    for index in range(al.size(neighbors)):
        neighbor_key = al.get_element(neighbors, index)
        if not mp.contains(visited_map,neighbor_key):
            neighbor_vertex = DG.get_vertex(
                my_graph["vertices"], neighbor_key)
            if neighbor_vertex is None:
                raise ValueError("Una adyacencia apunta a un vertice inexistente")

            info = {"marked": True, "edge_from": vtx.get_key(vertex)}
            mp.put(visited_map, neighbor_key, info)
            dfs_vertex(my_graph, neighbor_vertex,visited_map)
    return visited_map

def has_path_to(key_v,visited_map):
    """
        Indica si existe un camino entre el vertice source y 
        el vertice vertex a partir del mapa de recorrido.
    """
    return mp.contains(visited_map,key_v)

def path_to(key_v, visited_map):
    """
        Retorna el camino entre los vertices con llaves source y 
        key_v a partir del mapa de recorrido. 
        Retorna None si No hay camino.
    
    """
    if not has_path_to(key_v,visited_map):
        return None

    path = st.new_stack()
    current = key_v

    while current is not None:
        st.push(path, current)
        vertex_info = mp.get(visited_map, current)
        current = vertex_info["edge_from"]

    return path

