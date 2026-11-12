import random as rdm
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mlp

def new_map(num_elements=17, load_factor=0.5, prime=109345121):
    total_capacity = mlp.next_prime(num_elements / load_factor)
    tabla = {
        "prime": prime,
        "capacity": total_capacity,
        "scale": rdm.randint(1, prime - 1),
        "shift": rdm.randint(0, prime - 1),
        "table": lt.new_list(),
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
        "type": "PROBE_HASH_MAP",
    }

    for _ in range(total_capacity):
        lt.add_last(tabla["table"], me.new_map_entry(None, None))

    return tabla


def is_available(table, pos):
    entry = lt.get_element(table, pos)
    return entry is None or me.get_key(entry) is None


def default_compare(key, entry):
    if entry is None:
        return -1
    entry_key = me.get_key(entry)
    if key == entry_key:
        return 0
    elif entry_key is not None and key > entry_key:
        return 1
    return -1


def find_slot(my_map, key, hash_val=None):
    first_avail = None
    m = my_map["capacity"]
    if hash_val is None:
        hash_val = mlp.hash_value(my_map, key)

    for i in range(m):
        curr_i = (hash_val + i) % m
        entry = lt.get_element(my_map["table"], curr_i)

        if is_available(my_map["table"], curr_i):
            if first_avail is None:
                first_avail = curr_i
            if entry is None or me.get_key(entry) is None:
                return False, first_avail
        elif me.get_key(entry) == key:
            return True, curr_i

    return False, first_avail


def rehash(my_map):

    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mlp.next_prime(old_capacity * 2)
    new_table = lt.new_list()
    for _ in range(new_capacity):
        lt.add_last(new_table, me.new_map_entry(None, None))

    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    for i in range(old_capacity):
        entry = lt.get_element(old_table, i)
        if entry is not None:
            k = me.get_key(entry)
            if k is not None:
                put(my_map, k, me.get_value(entry))

    return my_map


def put(my_map, key, value):

    occupied, i = find_slot(my_map, key, mlp.hash_value(my_map, key))

    if i is None:
        rehash(my_map)
        occupied, i = find_slot(my_map, key, mlp.hash_value(my_map, key))
        if i is None:
            raise RuntimeError("Unable to find an available slot in the map")

    if occupied:
        entry = lt.get_element(my_map["table"], i)
        me.set_value(entry, value)
    else:
        new_entry = me.new_map_entry(key, value)
        lt.change_info(my_map["table"], i, new_entry)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)

    return my_map


def contains(my_map, key):

    occupied, _ = find_slot(my_map, key, mlp.hash_value(my_map, key))
    return occupied


def get(my_map, key):
    occupied, i = find_slot(my_map, key, mlp.hash_value(my_map, key))
    if not occupied:
        return None
    entry = lt.get_element(my_map["table"], i)
    return me.get_value(entry)


def remove(my_map, key):
    """
    Elimina la pareja asociada a la llave.
    """
    occupied, i = find_slot(my_map, key, mlp.hash_value(my_map, key))
    if not occupied:
        return None

    entry = lt.get_element(my_map["table"], i)
    val = me.get_value(entry)

    dead = me.new_map_entry(None, None)
    lt.change_info(my_map["table"], i, dead)

    my_map["size"] -= 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return val


def is_empty(my_map):
    """
    Retorna True si la tabla está vacía, False en caso contrario.
    """
    return my_map["size"] == 0 or my_map["table"] is None or my_map["capacity"] == 0

def key_set(my_map):
    """
    Retorna un conjunto con todas las llaves de la tabla.
    """
    keys = lt.new_list()
    for i in range(my_map["capacity"]):
        entry = lt.get_element(my_map["table"], i)
        if entry is not None:
            k = me.get_key(entry)
            if k is not None:
                lt.add_last(keys, k)
    return keys

def value_set(my_map):
    """
    Retorna un conjunto con todos los valores de la tabla.
    """
    values = lt.new_list()
    for i in range(my_map["capacity"]):
        entry = lt.get_element(my_map["table"], i)
        if entry is not None:
            k = me.get_key(entry)
            if k is not None:
                v = me.get_value(entry)
                lt.add_last(values, v)
    return values

def size(my_map):
    """
    Retorna el número de elementos guardados en la tabla.
    """
    return my_map["size"]