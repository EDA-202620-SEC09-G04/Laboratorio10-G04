from DataStructures.List import array_list as lt

def new_stack():
    return lt.new_list()

def push(stack, element):
    lt.add_first(stack, element)
    return stack


def pop(stack):
    if lt.is_empty(stack):
        raise Exception('EmptyStructureError: stack is empty')

    element = lt.first_element(stack)
    lt.remove_first(stack)
    return element


def is_empty(stack):
    return lt.is_empty(stack)


def top(stack):
    if lt.is_empty(stack):
        raise Exception('EmptyStructureError: stack is empty')
    return lt.first_element(stack)


def size(stack):
    return lt.size(stack)