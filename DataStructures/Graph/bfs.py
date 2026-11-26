from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import digraph as DG
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Queue import queue as qu
from DataStructures.Stack import stack as st

def bfs(my_graph,source):
    """
        Inicia un recorrido Breadth-First Search (BFS) desde source.
        El mapa resultante guarda cada vertice alcanzable y su predecesor.
    
    """
    visited_map = mp.new_map(num_elements=max(1, DG.order(my_graph)),load_factor=0.5)
    vertex_start = DG.get_vertex(my_graph, source)

    if vertex_start is None:
        raise ValueError("El vertice de inicio no existe en el grafo")

    mp.put(
        visited_map,
        source,
        {"marked": True, "dist_to": 0, "edge_from": None},
    )
    return bfs_vertex(my_graph,vertex_start,visited_map)

def bfs_vertex(my_graph,vertex,visited_map):
    """
        Recorre los vertices alcanzables en orden BFS y registra su predecesor.
    """
    if vertex is None:
        raise ValueError("No se puede recorrer un vertice inexistente")

    queue = qu.new_queue()
    qu.enqueue(queue, vertex)

    while not qu.is_empty(queue):
        current_vertex = qu.dequeue(queue)
        current_key = vtx.get_key(current_vertex)
        current_info = mp.get(visited_map, current_key)
        neighbors = mp.key_set(vtx.get_adjacents(current_vertex))
        for index in range(al.size(neighbors)):
            neighbor_key = al.get_element(neighbors, index)
            if not mp.contains(visited_map, neighbor_key):
                neighbor_vertex = DG.get_vertex(
                    my_graph, neighbor_key)
                if neighbor_vertex is None:
                    raise ValueError(
                        "Una adyacencia apunta a un vertice inexistente")

                info = {
                    "marked": True,
                    "edge_from": current_key,
                    "dist_to": current_info["dist_to"] + 1,
                }
                mp.put(visited_map, neighbor_key, info)
                qu.enqueue(queue, neighbor_vertex)
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