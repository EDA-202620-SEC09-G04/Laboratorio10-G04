from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import pq_entry as pqe

def default_compare_lower_value(father_node, child_node):
    return pqe.get_priority(father_node) < pqe.get_priority(child_node)


def default_compare_higher_value(father_node, child_node):
    return pqe.get_priority(father_node) > pqe.get_priority(child_node)


def new_heap(is_min_pq=True):
    
    if is_min_pq:
        cmp_fn = default_compare_lower_value
    else:
        cmp_fn = default_compare_higher_value
        
    elements = lt.new_list()
    heap = {
        "size": 0,
        "elements": elements,
        "cmp_function": cmp_fn
    }
    return heap


def priority(my_heap, index1, index2):
    
    elements = my_heap["elements"]
    pos1 = index1 - 1
    pos2 = index2 - 1
    entry1 = lt.get_element(elements, pos1)
    entry2 = lt.get_element(elements, pos2)
    cmp_fn = my_heap["cmp_function"]
    result = cmp_fn(entry1, entry2)
    return result


def exchange(my_heap, index1, index2):
    
    elements = my_heap["elements"]
    pos1 = index1 - 1
    pos2 = index2 - 1
    lt.exchange(elements, pos1, pos2)
    return my_heap


def swim(my_heap, index):
    
    pos = index
    swim = True
    while pos > 1 and swim:
        parent_pos = pos // 2
        is_parent_higher = priority(my_heap, parent_pos, pos)
        if not is_parent_higher:
            exchange(my_heap, pos, parent_pos)
            pos = parent_pos
        else:
            swim = False
    return my_heap


def insert(my_heap, priority, value):
    
    elements = my_heap["elements"]
    entry = pqe.new_pq_entry(priority, value)
    lt.add_last(elements, entry)
    my_heap["size"] += 1
    size = my_heap["size"]
    swim(my_heap, size)
    return my_heap


def size(my_heap):
    
    size = my_heap["size"]
    return size


def is_empty(my_heap):
    
    current_size = size(my_heap)
    res = False
    if current_size == 0:
        res = True
    return res


def sink(my_heap, pos):
    
    sink = True
    heap_size = size(my_heap)
    max_parent_pos = heap_size // 2
    while pos <= max_parent_pos and sink:
        child_izq = 2 * pos
        child_der = child_izq + 1
        if child_der <= heap_size:
            is_right_higher = priority(my_heap, child_der, child_izq)
            if is_right_higher:
                child_izq = child_der
        is_child_higher = priority(my_heap, child_izq, pos)
        if is_child_higher:
            exchange(my_heap, pos, child_izq)
            pos = child_izq
        else:
            sink = False
    return my_heap


def remove(my_heap):

    res = None
    if not is_empty(my_heap):
        elements = my_heap["elements"]
        first_element = lt.get_element(elements, 0)
        res = pqe.get_value(first_element)
        last_pos = size(my_heap)
        exchange(my_heap, 1, last_pos)
        lt.remove_last(elements)
        my_heap["size"] -= 1
        if not is_empty(my_heap):
            sink(my_heap, 1)
    return res


def get_first_priority(my_heap):
    
    res = None
    if not is_empty(my_heap):
        elements = my_heap["elements"]
        first_element = lt.get_element(elements, 0)
        res = pqe.get_priority(first_element)
    return res


def is_present_value(my_heap, value):
    
    found = -1
    curr_pos = 1
    elements = my_heap["elements"]
    while curr_pos <= size(my_heap) and found == -1:
        pos = curr_pos - 1
        element = lt.get_element(elements, pos)
        element_value = pqe.get_value(element)
        if element_value == value:
            found = curr_pos
        curr_pos += 1
    return found


def contains(my_heap, value):
    
    pos = is_present_value(my_heap, value)
    res  = False
    if pos != -1:
        res = True
    return res


def improve_priority(my_heap, priority, value):
    
    pos = is_present_value(my_heap, value)
    if pos != -1:
        elements = my_heap["elements"]
        element = lt.get_element(elements, pos - 1)
        pqe.set_priority(element, priority)
        swim(my_heap, pos)
    return my_heap