from helpers import unique
from numpy import inf, log10
from data import Data
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import matthews_corrcoef
import sys
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity
from sklearn.metrics import f1_score
# #Binned data is normally 7560 in length, train on 6048 and predict on the 1512

# with open('binned.pkl', 'rb') as f:
#     binned = pickle.load(f)

def train(train_set):
    '''
    Trains our model and returns our models for our classes. Here train_set represnts our training set
    '''
    names = []
    for x in range(len(train_set.labels[0])):
        names.append(train_set.labels[0][x]['type'])

    class_names = unique(names) #the 8 class names

    classes = {} # this is a dictionary of the 8 classes which have arrays of the length of the number of neurons
    zeroed = [0] * (len(train_set.sampled_data)+1) # the extra 1 indicates the number of occurences 
    for name in class_names :
        classes[name] = np.array(zeroed)
    #training:
    for x in range(len(train_set.sampled_data[0])):
        label = train_set.labels[0][x]['type']
        #print(label)
        neurons = []
        for y in range(len(train_set.sampled_data)):
            neurons.append(train_set.sampled_data[y][x])
        neurons.append(1)
        neurons = np.array(neurons)
        #neuron is now of length 133, containing a column of raster data, and 1 for once occurence
        #Now adding it to the relevant class
        classes[label] = classes[label]+neurons 


    for key in classes :
        array = (classes[key]/classes[key][len(classes[key])-1])
        classes[key] = array[0:len(classes[key])-1] #Get the average over all the bins and remove the counter 

    return classes

def predict(test_set, classes):
    '''
    makes predictions for the passed in set and returns arrays of the actual labels, and the corresponding predictions
    '''
    correlations = []
    actual = []
    rpredicted = []
    msepredicted = []
    cospredicted = []

    for x in range(len(test_set.sampled_data[0])):
        label = test_set.labels[0][x]['type']
        neurons = []
        for y in range(len(test_set.sampled_data)):
            neurons.append(test_set.sampled_data[y][x])
        neurons = np.array(neurons)

        rs = {}
        mses = {}
        coses ={}

        for key in classes :
            object = key
            array = classes[key]
            mse = ((array - neurons)**2).mean()
            cos =cosine_similarity([array], [neurons])[0][0]
            try :
                r = np.corrcoef(array, neurons)[0,1]
            except:
                r = mse

            rs[key] = r
            mses[key] = mse
            coses[key] = cos
            
        r_prediction = max(rs, key=rs.get)
        mse_prediction = min(mses, key=mses.get)
        cos_prediction = max(coses, key=coses.get)
        
        p = False
        if (round(rs[r_prediction],2) <0.4):
            p = True
            actual.append('pass')
            rpredicted.append('pass')
            msepredicted.append('pass')
            cospredicted.append('pass')
        else:
            actual.append(label)
            msepredicted.append(mse_prediction)
            rpredicted.append(r_prediction)
            cospredicted.append(cos_prediction)

        correlations.append(rs)
        #print("label: " + label + "\tr^2 " +str(round(rs[r_prediction],2))+": " +r_prediction)

    return actual, rpredicted, msepredicted, cospredicted, correlations
    # print("r^2:\tAccuracy: ", round((r_hits/len(test_set.sampled_data[0]))*100,2), "%", "\tmatthews corr coef: ", round(matthews_corrcoef(actual, rpredicted),2),"\tF1: ", round(f1_score(actual, rpredicted, average = 'weighted'),2), sep = "")
    # print("MSE:\tAccuracy: ", round((mse_hits/len(test_set.sampled_data[0]))*100,2), "%", "\tmatthews corr coef: ",round(matthews_corrcoef(actual, msepredicted),2), "\tF1: ",round(f1_score(actual, msepredicted, average = 'weighted'),2), sep = "")
    # print("Cosine:\tAccuracy: ", round((cos_hits/len(test_set.sampled_data[0]))*100,2), "%", "\tmatthews corr coef: ", round(matthews_corrcoef(actual, cospredicted),2), "\tF1: ", round(f1_score(actual, cospredicted, average = 'weighted'),2), sep = "")



