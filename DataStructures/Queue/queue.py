from DataStructures.List import single_linked_list as lt
from DataStructures.List import list_node as ln

def new_queue():
    return lt.new_list()

def enqueue(queue, element):
    lt.add_last(queue, element)
    return queue

def dequeue(queue):
    if lt.is_empty(queue):
        raise Exception('EmptyStructureError: queue is empty')
    elem = lt.first_element(queue)
    lt.remove_first(queue)
    return ln.get_element(elem)

def is_empty(queue):
    return lt.is_empty(queue)

def peek(queue):
    if lt.is_empty(queue):
        raise Exception('EmptyStructureError: queue is empty')
    return ln.get_element(lt.first_element(queue))

def size(queue):
    return lt.size(queue)  
