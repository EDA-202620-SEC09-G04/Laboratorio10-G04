from DataStructures.Graph import dfo_structure as dfo
from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import edge as edg
from DataStructures.Graph import digraph as DG
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al

"""def dfs(my_graph, source):
    vertices = al.new_list()
    inicio = DG.get_vertex(my_graph,source)
    if inicio is None:
        raise Exception("El vertice no existe")


    def recorrer_dfs(my_graph,vertice,vertices_visitados):
        vertice_key = vtx.get_key(vertice)
        al.add_last(vertices_visitados,vertice)
        vecinos = DG.adjacents(vertice_key)
        for i in range(al.size(vecinos)):
            if al.get_element(vertices_visitados,i) is not None:
                vecino = DG.get_vertex(my_graph,al.get_element(vertices_visitados,i))
                recorrer_dfs(my_graph,vecino,vertices_visitados)


def dfs_vertex(my_graph,vertex,visited_map):

"""