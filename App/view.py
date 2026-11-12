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


import sys
import threading
from App import logic
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
stopsfile = 'bus_stops.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def print_menu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información de buses de singapur") # Clase 1: Implementar digraph básico
    print("2- Encontrar las paradas más concurridas") # Casa 1: Implementar digraph completo
    print("3- Encontrar una ruta entre dos paradas (DFS)") # Casa 1: Implementar funcionalidad dfs
    print("4- Encontrar una ruta entre dos paradas (BFS)") # Clase 2: Implementar funcionalidad bfs
    print("5- Encontrar la ruta mínima entre dos paradas") # Casa 2: Implementar dijkstra
    print("6- Mostrar en un mapa la ruta mínima entre dos paradas") # Trabajo Complementario: Mostrar ruta con folium
    print("0- Salir")
    print("*******************************************")


def option_one(cont):
    print("\nCargando información de transporte de singapur ....")
    logic.load_services(cont, servicefile, stopsfile)
    numedges = logic.total_connections(cont)
    numvertex = logic.total_stops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

def option_two(cont):
    most_concurrent = logic.get_most_concurrent_stops(cont)

    if al.is_empty(most_concurrent):
        print("\nNo hay paradas para mostrar.")
        return

    print("\nLas paradas más concurridas son:")
    for index in range(al.size(most_concurrent)):
        vertex, total_connections = al.get_element(most_concurrent, index)
        print(
            f"{index + 1}. {vertex}: "
            f"{total_connections} conexiones"
        )

def option_three(cont):
    origin = input(
        "Ingrese el BusStopCode o la llave origen (BusStopCode-ServiceNo): "
    ).strip()
    destination = input(
        "Ingrese el BusStopCode o la llave destino (BusStopCode-ServiceNo): "
    ).strip()
    path = logic.get_route_between_stops_dfs(cont, origin, destination)

    if path is None:
        print("\nNo se encontró una ruta entre las paradas indicadas.")
        return

    route = []
    while not st.is_empty(path):
        route.append(st.pop(path))

    print("\nRuta encontrada:")
    print(" -> ".join(route))

def option_four(cont):
    # TODO: Imprimir los resultados de la opción 4
    ...

def option_five(cont):
    # TODO: Imprimir los resultados de la opción 5
    ...

def option_six(cont):
    # (Opcional) TODO: Imprimir los resultados de la opción 6
    ...


"""
Menu principal
"""


def main():
    cont = logic.new_analyzer()
    working = True
    while working:
        print_menu()
        option = input('Seleccione una opción para continuar\n>').strip()

        if option == "1":
            print("\nInicializando....")
            cont = logic.new_analyzer()
            option_one(cont)
        elif option == "2":
            option_two(cont)
        elif option == "3":
            option_three(cont)
        elif option == "4":
            option_four(cont)
        elif option == "5":
            option_five(cont)
        elif option == "6":
            option_six(cont)
        elif option == "0":
            working = False
            print("Saliendo...")
        else:
            print("Opción no válida. Seleccione una opción del menú.")


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()
