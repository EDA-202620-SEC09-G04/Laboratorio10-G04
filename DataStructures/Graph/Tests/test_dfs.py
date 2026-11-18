import pytest

from DataStructures.Graph import dfs as DFS
from DataStructures.Graph import digraph as DG
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st


def build_graph(vertex_count, edges):
    graph = DG.new_graph(vertex_count)
    for key in range(vertex_count):
        DG.insert_vertex(graph, key, key)
    for source, destination in edges:
        DG.add_edge(graph, source, destination)
    return graph


def test_dfs_tracks_reachable_vertices_and_predecessor_path():
    graph = build_graph(
        5,
        ((0, 1), (0, 2), (1, 2), (2, 0), (2, 3)),
    )
    visited = DFS.dfs(graph, 0)

    assert DFS.has_path_to(0, visited)
    assert DFS.has_path_to(3, visited)
    assert not DFS.has_path_to(4, visited)
    assert DFS.path_to(4, visited) is None

    path = DFS.path_to(3, visited)
    route = []
    while not st.is_empty(path):
        route.append(st.pop(path))

    assert route[0] == 0
    assert route[-1] == 3
    for source, destination in zip(route, route[1:]):
        source_vertex = DG.get_vertex(graph["vertices"], source)
        assert mp.contains(V.get_adjacents(source_vertex), destination)


def test_dfs_rejects_missing_source():
    graph = build_graph(1, ())

    with pytest.raises(ValueError):
        DFS.dfs(graph, 1)
