import numpy as np
import random
import sys

def random_sequence(objects, size):
    '''
    Function that returns a random sequence of valid objects shown to the mice where objects is the valid objects
    that can be shown and size is the number of trials we want to try
    '''
    order_num = np.random.randint(0,(len(objects)),size)
    order_objects = []
    for x in range (size):
        order_objects.append(objects[order_num[x]])

    return order_objects

def unique(list1):
    '''
    Function returns unique elements in a list
    '''
    # intilize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def concatenate (arr1, arr2):
    '''
    concatenates arr2 to arr1
    '''
    for x in range(len(arr2)):
        arr1.append(arr2[x])
    
    return arr1