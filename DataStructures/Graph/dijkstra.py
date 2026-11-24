from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import digraph as DG
from DataStructures.Graph import edge as edg
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st
from DataStructures.Graph import dijsktra_structure as structure
from DataStructures.Priority_queue import priority_queue as pq


def dijkstra(my_graph, source):
    """
    Ejecuta el algoritmo de Dijkstra desde el vertice source.
    La estructura resultante contiene las distancias y predecesores de los
    vertices alcanzables.
    """
    if not DG.contains_vertex(my_graph, source):
        raise ValueError("El vertice de inicio no existe en el grafo")

    keys = DG.vertices(my_graph)
    for key_index in range(al.size(keys)):
        key = al.get_element(keys, key_index)
        vertex = DG.get_vertex(my_graph["vertices"], key)
        edges = mp.value_set(vtx.get_adjacents(vertex))
        for edge_index in range(al.size(edges)):
            edge = al.get_element(edges, edge_index)
            if edg.weight(edge) < 0:
                raise ValueError(
                    "Dijkstra no admite arcos con peso negativo")

    new_dick = structure.new_dijsktra_structure(
        source, DG.order(my_graph))
    mp.put(
        new_dick["visited"],
        source,
        {"marked": True, "dist_to": 0, "edge_from": None},
    )
    pq.insert(new_dick["pq"], 0, source)

    return dijkstra_vertex(my_graph, new_dick)


def dijkstra_vertex(my_graph, aux_structure):
    """
    Recorre el grafo relajando los arcos desde el origen.
    """
    priority_queue = aux_structure["pq"]
    visited = aux_structure["visited"]

    while not pq.is_empty(priority_queue):
        current_key = pq.remove(priority_queue)
        current_vertex = DG.get_vertex(
            my_graph["vertices"], current_key)
        if current_vertex is None:
            continue

        current_info = mp.get(visited, current_key)
        current_distance = current_info["dist_to"]
        edges = mp.value_set(vtx.get_adjacents(current_vertex))

        for index in range(al.size(edges)):
            edge = al.get_element(edges, index)
            neighbor_key = edg.to(edge)
            neighbor_vertex = DG.get_vertex(
                my_graph["vertices"], neighbor_key)
            if neighbor_vertex is None:
                raise ValueError(
                    "Una adyacencia apunta a un vertice inexistente")

            candidate_distance = (
                current_distance + edg.weight(edge))
            neighbor_info = mp.get(visited, neighbor_key)

            if neighbor_info is None:
                mp.put(
                    visited,
                    neighbor_key,
                    {
                        "marked": True,
                        "dist_to": candidate_distance,
                        "edge_from": current_key,
                    },
                )
                pq.insert(
                    priority_queue,
                    candidate_distance,
                    neighbor_key,
                )
            elif candidate_distance < neighbor_info["dist_to"]:
                neighbor_info["dist_to"] = candidate_distance
                neighbor_info["edge_from"] = current_key
                pq.improve_priority(
                    priority_queue,
                    candidate_distance,
                    neighbor_key,
                )

    return aux_structure


def dist_to(key_v, aux_structure):
    """
    Retorna el costo del camino para llegar del vertice source al vertice key_v.
    Retorna infinito si no existe camino.
    """
    if not mp.contains(aux_structure["visited"], key_v):
        return float("inf")
    return mp.get(aux_structure["visited"], key_v)["dist_to"]


def has_path_to(key_v, aux_structure):
    """
    Indica si existe un camino entre el vertice source y key_v.
    """
    return mp.contains(aux_structure["visited"], key_v)


def path_to(key_v, aux_structure):
    """
    Retorna un stack con el camino desde source hasta key_v.
    Retorna None si no existe camino.
    """
    if not has_path_to(key_v, aux_structure):
        return None

    path = st.new_stack()
    current = key_v

    while current is not None:
        st.push(path, current)
        vertex_info = mp.get(aux_structure["visited"], current)
        current = vertex_info["edge_from"]

    return path
