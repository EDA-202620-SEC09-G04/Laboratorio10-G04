import random as rdm
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements=17, load_factor=0.5, prime=109345121):
    capacity = mf.next_prime(num_elements / load_factor)
    my_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": rdm.randint(1, prime - 1),
        "shift": rdm.randint(0, prime - 1),
        "table": lt.new_list(),
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
        "type": "CHAIN_HASH_MAP",
    }

    for _ in range(capacity):
        lt.add_last(my_map["table"], sll.new_list())

    return my_map


def is_available(table, pos):
    bucket = lt.get_element(table, pos)
    return bucket is None or sll.is_empty(bucket)


def default_compare(key, entry):
    if entry is None:
        return -1
    entry_key = me.get_key(entry)
    if key == entry_key:
        return 0
    if entry_key is not None and key > entry_key:
        return 1
    return -1


def _find_entry(my_map, key):
    bucket_index = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], bucket_index)
    if bucket is None:
        return bucket_index, -1, None

    for entry_index in range(sll.size(bucket)):
        entry = sll.get_element(bucket, entry_index)["info"]
        if me.get_key(entry) == key:
            return bucket_index, entry_index, entry

    return bucket_index, -1, None


def find_slot(my_map, key):
    bucket_index, _, entry = _find_entry(my_map, key)
    return entry is not None, bucket_index


def rehash(my_map):
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = lt.new_list()
    for _ in range(new_capacity):
        lt.add_last(new_table, sll.new_list())

    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    for bucket_index in range(old_capacity):
        bucket = lt.get_element(old_table, bucket_index)
        for entry_index in range(sll.size(bucket)):
            entry = sll.get_element(bucket, entry_index)["info"]
            new_bucket_index = mf.hash_value(my_map, me.get_key(entry))
            new_bucket = lt.get_element(my_map["table"], new_bucket_index)
            sll.add_last(new_bucket, entry)
            my_map["size"] += 1

    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map


def put(my_map, key, value):
    bucket_index, _, entry = _find_entry(my_map, key)
    bucket = lt.get_element(my_map["table"], bucket_index)

    if entry is not None:
        me.set_value(entry, value)
    else:
        sll.add_last(bucket, me.new_map_entry(key, value))
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)

    return my_map


def contains(my_map, key):
    _, _, entry = _find_entry(my_map, key)
    return entry is not None


def get(my_map, key):
    _, _, entry = _find_entry(my_map, key)
    if entry is None:
        return None
    return me.get_value(entry)


def remove(my_map, key):
    bucket_index, entry_index, entry = _find_entry(my_map, key)
    if entry is None:
        return None

    bucket = lt.get_element(my_map["table"], bucket_index)
    removed = sll.delete_element(bucket, entry_index)
    value = me.get_value(removed["info"])
    my_map["size"] -= 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return value


def is_empty(my_map):
    return my_map["size"] == 0


def key_set(my_map):
    keys = lt.new_list()
    for bucket_index in range(my_map["capacity"]):
        bucket = lt.get_element(my_map["table"], bucket_index)
        for entry_index in range(sll.size(bucket)):
            entry = sll.get_element(bucket, entry_index)["info"]
            lt.add_last(keys, me.get_key(entry))
    return keys


def value_set(my_map):
    values = lt.new_list()
    for bucket_index in range(my_map["capacity"]):
        bucket = lt.get_element(my_map["table"], bucket_index)
        for entry_index in range(sll.size(bucket)):
            entry = sll.get_element(bucket, entry_index)["info"]
            lt.add_last(values, me.get_value(entry))
    return values


def size(my_map):
    return my_map["size"]
