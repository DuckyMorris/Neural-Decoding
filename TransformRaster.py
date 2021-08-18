from helpers import unique
from ExtractMat import get_mat_data
import numpy as np
import pandas as pd
from ExtractMat import get_mat_data
from helpers import random_sequence
import random

def transform_raster(temp):
    '''
    Function takes in parameter, temp, which contains many dictionaries, each extracted 
    from one .mat files containing information from one neuron.  The function converts this data into a np matrix
    of neurons x number of samples taken (frequency x time)
    It also respons the corresponding labels in the format 132 x 420 where each entry is a dictionary of the 
    location and type of stimulus, as well as the combined. 
    '''
    data = []
    labels = []
    objects = []
    times = []
    for x in range(len(temp)):
        data.append(temp[x]['raster_data'])
        labels.append(temp[x]['raster_labels'])
        # objects.append(labels[x][0][0][0][0][0][0])
    #data is neurons x time x frequency, we want to now convert this to neurons x (time x frequency)
    #labels is neurons x 1 x 1 x 3(location, type and combination) x 1 x 420 x 1. we want to transform this to neurons x (time x frequency) 
    #Here each element will be a dictionary. 
    num_trials = len(data[0])-1  # the rows in one file representing the number of trials. -1 for the 419 trial tests
    num_neurons = len(data)
    labels = np.array(labels)
    for x in range (num_neurons):
        for y in range (num_trials-1):
            objects.append(labels[x][0][0][2][0][y][0])

    objects = unique(objects) #objects is now all the unique combination of location and type of stimulus shown
    #print(objects)
    order = random_sequence(objects, num_trials)
    sample = [] #sample is going to store our neurons x (time x frequency)
    new_labels = []

    for x in range (num_neurons): #number of neurons
        time = 0
        time_array = []
        temp = np.array([])
        temp_label = []
        for y in range (len(order)): #going through the order of our pseudo population
            valid_indexes = []
            for z in range(num_trials):
                if labels[x][0][0][2][0][z][0] == order[y]:
                    valid_indexes.append(z)
            index = random.choice(valid_indexes)

            temp1 = np.array(data[x][index])
            temp_label1 = {}
            temp_label1['location'] = labels[x][0][0][1][0][index][0]
            temp_label1['type'] = labels[x][0][0][0][0][index][0]
            temp_label1['combined'] = labels[x][0][0][2][0][index][0]
            temp_label.append(temp_label1)
            temp = np.concatenate((temp,temp1))
            time_array.append(time)
            time = time + 0.001
            time = round(time,3)
        sample.append(temp) 
        new_labels.append(temp_label)
        times.append(time_array)

    temp = []
    no_stimuli = {}
    no_stimuli['location'] = "None"
    no_stimuli['type'] = "None"
    no_stimuli['combined'] = "None"
    for x in range (len(new_labels)):
        temp1 = []
        for y in range (len(new_labels[x])):
            for i in range (500):
                temp1.append(no_stimuli)
            for i in range (500):
                temp1.append(new_labels[x][y])
        temp.append(temp1)

    new_labels = temp # labels is now the same dimension of sample
    # sample = np.array(sample)
    # times = np.array(times)
    return sample, new_labels, times



# NeuralData, BinnedData = get_mat_data() 

# sampled_data, labels, timestaps = transform_raster(NeuralData) 
