def new_list():
    newlist = {
        "elements": [],
        "size": 0, 
    }
    return newlist

def get_element(my_list, index):    
    if index < 0 or index >= my_list["size"] or my_list["size"] == 0 or my_list["elements"] == []:
        return None
    return my_list["elements"][index]


def is_present(my_list, element, cmp_function):
    
    size = my_list["size"]
    if size > 0:
        keyexist = False 
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexist = True 
                break
        if keyexist:
            return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

def size(my_list):
    return my_list["size"]

def first_element(my_list):
    if size(my_list) == 0:
        return None
    return my_list["elements"][0] 

def is_empty(my_list):
    return my_list["size"] == 0 or my_list["elements"] == []

def last_element(my_list):
    if is_empty(my_list):
        return None
    return my_list["elements"][size(my_list) - 1]

def delete_element(my_list, index):
    if is_empty(my_list) or index < 0 or index >= size(my_list):
        return None
    del my_list["elements"][index]
    my_list["size"] -= 1
    return my_list

def remove_first(my_list):
    if is_empty(my_list):
        return None
    element = get_element(my_list,0)
    del my_list["elements"][0]
    my_list["size"] -= 1
    return element


def remove_last(my_list):
    if is_empty(my_list):
        return None
    element = get_element(my_list,size(my_list)-1)
    del my_list["elements"][size(my_list) - 1]
    my_list["size"] -= 1
    return element

def insert_element(my_list,element,index):
    if index < 0:
        return None
    
    my_list["elements"].insert(index, element)
    my_list["size"] += 1
    return my_list

def change_info(my_list,index,new_info):
    if index < 0 or index >= size(my_list) or is_empty(my_list):
        return None

    
    my_list["elements"][index] = new_info
    return my_list

def exchange(my_list,index1,index2):
    if index1 < 0 or index2 < 0 or index1 >= size(my_list) or index2 >= size(my_list):
        return
    my_list["elements"][index1], my_list["elements"][index2] = (
        my_list["elements"][index2],
        my_list["elements"][index1],
    )
    return my_list

def sub_list(my_list,index,num_elements):
    if index < 0 or index >= my_list["size"] or is_empty(my_list):
        raise IndexError("list index out of range")
    sub = new_list()
    sub["elements"] = my_list["elements"][index:index + num_elements]
    sub["size"] = len(sub["elements"])
    return sub        


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
            if sort_crit(get_element(my_list,pos2),get_element(my_list,minimum)):
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
        while pos2 > 0 and not sort_crit(get_element(my_list,pos2-1),get_element(my_list,pos2)):
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
                while pos2 >= step and not sort_crit(get_element(my_list, pos2-step) , get_element(my_list,pos2)):
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
    left_list = sub_list(my_list, 0, middle)
    right_list = sub_list(my_list, middle, n - middle)

    merge_sort(left_list, sort_crit)
    merge_sort(right_list, sort_crit)

    temp = new_list()
    pos_left = 0
    pos_right = 0
 
    while pos_left < size(left_list) and pos_right < size(right_list):
        if sort_crit(get_element(left_list, pos_left), get_element(right_list, pos_right)):
            add_last(temp,get_element(left_list,pos_left))

            pos_left += 1
        else:
            add_last(temp,get_element(right_list,pos_right))
            pos_right += 1
        
    # Aquellos elementos que no quedaron alterados en el anterior ciclo
    # se van a insertar al final de la lista (tanto en el lado izquierdo como en el derecho)

    while pos_left < size(left_list):
        add_last(temp,get_element(left_list,pos_left))
        pos_left += 1

    while pos_right < size(right_list):
        add_last(temp,get_element(right_list,pos_right))
        pos_right += 1

    for i in range(size(temp)):
        change_info(my_list,i,get_element(temp,i))
    
    return my_list

def heap_sort(my_list, sort_crit):
    """
        IN-PLACE: T
        ESTABLE: F
        ADAPTABLE: T
    """
    elements = my_list["elements"]
    n = size(my_list)

    def sift_down(root, end):
        while True:
            child = 2 * root + 1
            if child >= end:
                return
            if child + 1 < end and sort_crit(elements[child], elements[child + 1]):
                child += 1
            if not sort_crit(elements[root], elements[child]):
                return
            exchange(elements, root, child)
            
            root = child

    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n)

    for end in range(n - 1, 0, -1):
        exchange(elements, 0, end)
        #elements[0], elements[end] = elements[end], elements[0]
        sift_down(0, end)

    return my_list

def quick_sort(my_list,sort_crit):
    """
        IN-PLACE: T
        ESTABLE: F
        ADAPTABLE: F
    """
    if size(my_list) < 2:
        return my_list

    elements = my_list["elements"]
    pending = [(0, len(elements) - 1)]
    while pending:
        low, high = pending.pop()
        while low < high:
            middle = (low + high) // 2
            first = elements[low]
            center = elements[middle]
            last = elements[high]

            if sort_crit(first, center):
                if sort_crit(center, last):
                    pivot = center
                elif sort_crit(first, last):
                    pivot = last
                else:
                    pivot = first
            elif sort_crit(first, last):
                pivot = first
            elif sort_crit(center, last):
                pivot = last
            else:
                pivot = center

            less = low
            current = low
            greater = high
            while current <= greater:
                element = elements[current]
                if sort_crit(element, pivot):
                    elements[less], elements[current] = elements[current], elements[less]
                    less += 1
                    current += 1
                elif sort_crit(pivot, element):
                    elements[current], elements[greater] = elements[greater], elements[current]
                    greater -= 1
                else:
                    current += 1

            left_size = less - low
            right_size = high - greater
            if left_size < right_size:
                if right_size > 1:
                    pending.append((greater + 1, high))
                high = less - 1
            else:
                if left_size > 1:
                    pending.append((low, less - 1))
                low = greater + 1

    return my_list
