import pytest

from DataStructures.Graph import dijkstra as DIJKSTRA
from DataStructures.Graph import digraph as DG
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st


def build_graph():
    graph = DG.new_graph(6)
    for key in range(6):
        DG.insert_vertex(graph, key, key)

    DG.add_edge(graph, 0, 1, 4)
    DG.add_edge(graph, 0, 2, 1)
    DG.add_edge(graph, 2, 1, 2)
    DG.add_edge(graph, 1, 3, 1)
    DG.add_edge(graph, 2, 3, 5)
    DG.add_edge(graph, 3, 4, 2)
    return graph


def test_dijkstra_records_weighted_distances_and_predecessors():
    graph = build_graph()
    search = DIJKSTRA.dijkstra(graph, 0)

    assert DIJKSTRA.dist_to(0, search) == 0
    assert DIJKSTRA.dist_to(1, search) == 3
    assert DIJKSTRA.dist_to(2, search) == 1
    assert DIJKSTRA.dist_to(3, search) == 4
    assert DIJKSTRA.dist_to(4, search) == 6
    assert DIJKSTRA.dist_to(5, search) == float("inf")

    assert DIJKSTRA.has_path_to(4, search)
    assert not DIJKSTRA.has_path_to(5, search)
    assert mp.get(search["visited"], 1)["edge_from"] == 2


def test_dijkstra_path_to_source_and_unreachable_vertex():
    search = DIJKSTRA.dijkstra(build_graph(), 0)

    source_path = DIJKSTRA.path_to(0, search)
    assert st.size(source_path) == 1
    assert st.pop(source_path) == 0
    assert DIJKSTRA.path_to(5, search) is None


def test_dijkstra_rejects_missing_source():
    with pytest.raises(ValueError):
        DIJKSTRA.dijkstra(build_graph(), 6)


def test_dijkstra_rejects_negative_weights():
    graph = DG.new_graph(2)
    DG.insert_vertex(graph, 0, 0)
    DG.insert_vertex(graph, 1, 1)
    DG.add_edge(graph, 0, 1, -1)

    with pytest.raises(ValueError):
        DIJKSTRA.dijkstra(graph, 0)
