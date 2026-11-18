import pytest

from DataStructures.Graph import bfs as BFS
from DataStructures.Graph import digraph as DG
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st


def build_graph():
    graph = DG.new_graph(6)
    for key in range(6):
        DG.insert_vertex(graph, key, key)

    for source, destination in (
        (0, 1),
        (0, 2),
        (1, 3),
        (3, 4),
        (2, 4),
    ):
        DG.add_edge(graph, source, destination)
    return graph


def test_bfs_records_shortest_path_and_reachability():
    graph = build_graph()
    visited = BFS.bfs(graph, 0)

    assert BFS.has_path_to(4, visited)
    assert not BFS.has_path_to(5, visited)
    assert mp.get(visited, 0)["dist_to"] == 0
    assert mp.get(visited, 1)["dist_to"] == 1
    assert mp.get(visited, 2)["dist_to"] == 1
    assert mp.get(visited, 3)["dist_to"] == 2
    assert mp.get(visited, 4)["dist_to"] == 2

    path = BFS.path_to(4, visited)
    route = []
    while not st.is_empty(path):
        route.append(st.pop(path))

    assert route[0] == 0
    assert route[-1] == 4
    assert len(route) == 3
    for source, destination in zip(route, route[1:]):
        source_vertex = DG.get_vertex(graph["vertices"], source)
        assert mp.contains(V.get_adjacents(source_vertex), destination)
    assert BFS.path_to(5, visited) is None


def test_bfs_source_has_a_path_to_itself():
    visited = BFS.bfs(build_graph(), 0)

    assert BFS.has_path_to(0, visited)
    path = BFS.path_to(0, visited)
    assert st.size(path) == 1
    assert st.pop(path) == 0


def test_bfs_rejects_missing_source():
    with pytest.raises(ValueError):
        BFS.bfs(build_graph(), 6)
