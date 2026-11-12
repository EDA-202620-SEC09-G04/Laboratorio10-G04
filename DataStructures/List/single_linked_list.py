from DataStructures.List import list_node as nd

def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0, 
    }
    return newlist

def is_empty(my_list):
    return not my_list["first"] 

def size(my_list):
    return my_list["size"]

def get_element(my_list, pos):
    if is_empty(my_list) or pos < 0 or pos >= size(my_list):
        return None

    node = my_list["first"]
    for _ in range(pos):
        node = node["next"]
    return node

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0 
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True 
        else:
            temp = temp["next"]
            count += 1
            
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):
    nodo = nd.new_single_node(element)
    nodo["next"] = my_list["first"]
    my_list["first"] = nodo

    if my_list["size"] == 0:
        my_list["last"] = nodo
        
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    nodo = nd.new_single_node(element)
    
    if size(my_list) == 0:
        my_list["first"] = nodo
    else: 
        my_list["last"]["next"] = nodo    
    
    my_list["last"] = nodo        
    my_list["size"] += 1
    return my_list

def first_element(my_list):
    if my_list["first"]:
        return my_list["first"]
    return None

def last_element(my_list):
    if my_list["last"]:
        return my_list["last"]
    return get_element(my_list,size(my_list)-1)

def delete_element(my_list,index):
    if index < 0 or index >= size(my_list):
        return
    removed = None
    if index == 0:
        removed = first_element(my_list)
        my_list["first"] = removed["next"]
    else:
        previous = get_element(my_list,index-1)
        removed = previous["next"]
        previous["next"] = removed["next"]

    my_list["size"] -= 1
    removed["next"] = None
    if my_list["size"] == 0:
        my_list["last"] = None
    elif removed == my_list["last"]:
        my_list["last"] = previous

    return removed

def remove_first(my_list):
    if is_empty(my_list):
            return
    delete_element(my_list,0)

    return 0

def remove_last(my_list):
    if is_empty(my_list):
        return
    last_pos = size(my_list) - 1
    delete_element(my_list,last_pos)
    
    return last_pos

def insert_element(my_list,element,index):
    if index < 0 or index > size(my_list):
        return None

    nodo = nd.new_single_node(element)

    if index == 0:
        nodo["next"] = my_list["first"]
        my_list["first"] = nodo
        if my_list["size"] == 0:
            my_list["last"] = nodo
    elif index >= size(my_list):
        my_list["last"]["next"] = nodo
        my_list["last"] = nodo
    else:
        previous = get_element(my_list,index-1)
        nodo["next"] = previous["next"]
        previous["next"] = nodo

    my_list["size"] += 1

    return my_list

def change_info(my_list,index,new_info):
    if is_empty(my_list) or index < 0 or index >= size(my_list):
        return None
    
    node = get_element(my_list,index)
    node["info"] = new_info
    return my_list 

def exchange(my_list, index1, index2):
    if (is_empty(my_list) or index1 < 0 or index1 >= size(my_list)
            or index2 < 0 or index2 >= size(my_list)):
        return None

    if index1 == index2:
        return my_list
    if index1 > index2:
        index1, index2 = index2, index1
    previous1 = None
    if index1 > 0:
        previous1 = get_element(my_list, index1 - 1)
    previous2 = get_element(my_list, index2 - 1)
    node1 = get_element(my_list, index1)
    node2 = get_element(my_list, index2)

    if node1["next"] == node2:
        node1["next"] = node2["next"]
        node2["next"] = node1
    else:
        temp = node2["next"]
        node2["next"] = node1["next"]
        node1["next"] = temp
        previous2["next"] = node1

    if previous1 is None:
        my_list["first"] = node2
    else:
        previous1["next"] = node2

    if node1["next"] is None:
        my_list["last"] = node1
    elif node2["next"] is None:
        my_list["last"] = node2
    
    return my_list

def sub_list(my_list,index,num_elements):
    if index < 0 or num_elements < 0 or index > size(my_list):
        return None

    nl = new_list()

    node = None
    if index < size(my_list):
        node = get_element(my_list, index)
    for _ in range(num_elements):
        if node is None:
            break
        add_last(nl, node["info"])
        node = node["next"]

    return nl
    
def default_sort_criteria(element1,element2):
    return element1 < element2

def selection_sort(my_list,sort_crit):
    """
        IN-PLACE: T
        ESTABLE: F
        ADAPTABLE: F
    """
    
    n = size(my_list)
    for pos1 in range(n):
        minimum = pos1
        for pos2 in range(pos1+1,n):
            if sort_crit(nd.get_element(get_element(my_list,pos2)),nd.get_element(get_element(my_list,minimum))):
                minimum = pos2
        if minimum != pos1:
            exchange(my_list,pos1,minimum)

        pos1 += 1
    
    return my_list

def insertion_sort(my_list, sort_crit):
    """
        IN-PLACE: T
        ESTABLE: T
        ADAPTABLE: T
    """

    n = size(my_list)
    for pos1 in range(1,n):
        pos2 = pos1
        while pos2 > 0 and sort_crit(nd.get_element(get_element(my_list,pos2)),nd.get_element(get_element(my_list,pos2-1))):
            exchange(my_list,pos2,pos2-1)
            pos2 -= 1


    return my_list
    
def shell_sort(my_list,sort_crit):
    """
        IN-PLACE: T
        ESTABLE: F
        ADAPTABLE: T
    """
    if size(my_list) > 1:
        n = size(my_list)
        step = n // 2
        while step > 0:
            for pos1 in range (step,n):
                pos2 = pos1
                while pos2 >= step and sort_crit(nd.get_element(get_element(my_list, pos2)) , nd.get_element(get_element(my_list,pos2-step))):
                    exchange(my_list, pos2, pos2-step)
                    pos2 -= step
            step //= 2
    return my_list

def merge_sort(my_list,sort_crit):
    """
        IN-PLACE: F
        ESTABLE: T
        ADAPTABLE: F

    """

    n = size(my_list)
    if n <= 1:
        return my_list

    middle = n // 2
    list_left = sub_list(my_list, 0, middle)
    list_right = sub_list(my_list, middle, n - middle)

    merge_sort(list_left, sort_crit)
    merge_sort(list_right, sort_crit)

    temp = new_list()
    pos_left = 0
    pos_right = 0
 
    while pos_left < size(list_left) and pos_right < size(list_right):
        if sort_crit(nd.get_element(get_element(list_left, pos_left)), nd.get_element(get_element(list_right, pos_right))):
            add_last(temp,nd.get_element(get_element(list_left,pos_left)))

            pos_left += 1
        else:
            add_last(temp,nd.get_element(get_element(list_right,pos_right)))
            pos_right += 1
        
    # Aquellos elementos que no quedaron alterados en el anterior ciclo
    # se van a insertar al final de la lista (tanto en el lado izquierdo como en el derecho)

    while pos_left < size(list_left):
        add_last(temp,nd.get_element(get_element(list_left,pos_left)))
        pos_left += 1

    while pos_right < size(list_right):
        add_last(temp,nd.get_element(get_element(list_right,pos_right)))
        pos_right += 1

    for i in range(size(temp)):
        change_info(my_list,i,nd.get_element(get_element(temp,i)))
    
    return my_list

def quick_sort(my_list,sort_crit):
    """
        IN-PLACE: T
        ESTABLE: F
        ADAPTABLE: F
    """

    low = 1
    high = size(my_list) - 1
    def partition(my_list,low,high,sort_crit):

        leader = low
        following = low

        while leader < high:
            leader_element = get_element(my_list,leader)
            pivot_element = get_element(my_list,high)
            if leader_element != None and pivot_element != None  and sort_crit(nd.get_element(leader_element),nd.get_element(pivot_element)):
                exchange(my_list,following,leader)
                following += 1
            leader += 1
        exchange(my_list,following,high)
        return following
    
    def qs(my_list,low,high,sort_crit):
        if (low >= high):
            return
        pivot = partition(my_list,low,high,sort_crit)
        qs(my_list,low,pivot-1,sort_crit)
        qs(my_list,pivot+1,high,sort_crit)

    return qs(my_list,low,high,sort_crit)
