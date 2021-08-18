from io import TextIOBase
from numpy.core.numeric import correlate
from ExtractMat import get_mat_data
import numpy as np
import pandas as pd
from TransformRaster import transform_raster
import datetime
import time
import pickle
from data import Data
from ml import train, predict
from helpers import concatenate
from sklearn.metrics import matthews_corrcoef
import sys
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import datetime
import matplotlib.animation as animation
import time
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
from plots import update_plot1, update_plot2
#Helper functions:
def grab_size(start, data, size):
    '''
    Function that grabs size recordings of data from matrix that is supposed to mimic that of open Ephys
    data is the neurons array, and in this case its the raster data, start is the start column to read from 
    '''
    result = [] #This is going to be the neurons + 1 by size array
    for x in range(len(data)): # for each channel
        temp = []
        for y in range(size):
            temp.append(data[x][y+start])
        
        result.append(temp)
    return result

def add_to_trainset(train, added):
    '''
    train is our train set and adds added to the training set which is the labels and neurons array
    '''
    if train.sampled_data == []: #here our train set is un initialized
        for x in range (len(added)-1): # set up the 132 rows
            train.sampled_data.append(added[x+1])
        train.labels = concatenate(train.labels, (added[0]))
    else:
        for x in range (len(added )-1): # go through the 132 rows 
            train.sampled_data[x] = concatenate(train.sampled_data[x], added[x+1])
            
        train.labels = concatenate(train.labels, (added[0]))
    return train


#Setting up our live, where labels are our labels and sampled data is our spike sorted data

with open('openephys.pkl', 'rb') as f:
    data = pickle.load(f)
#Now data is in the form of how our data should be read from open ephys, the first channel is the labels and the 
#following channels are the neuron data

index = 0
train_set = Data()
train_set.sampled_data = [] 
train_set.labels = []

t1 = datetime.datetime.now()
t2 = datetime.datetime.now()
num_channels = len(data)
#setting up plots
plt.ion()
fig, axis = plt.subplots(1,2)
ax1 = axis[0]
ax2 = axis[1]
x1=[]
y1= []
for x in range(132):
    y1.append([])
lines = None
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax1.text(0.15, 0.5, "Waiting for predicting period" , transform=ax1.transAxes, fontsize=15, verticalalignment='top', bbox=props)
ax1.title.set_text('Bar plot showing the correlation of the current data with each class')
ax1.set_ylabel('Correlation')


loop_counter = 0
while index < len(data[0]) * 0.8:#((t2 - t1).total_seconds() < 18.5): #For 0.8 of the data, the loop takes about 18.5 seconds
    temp_set = Data()
    temp = grab_size(index, data, 200) #In the open ephys, this temp would be simply the data receieved from the plugin
    train_set = add_to_trainset(train_set,temp)#We now want to add temp to our training set 
    temp_set = add_to_trainset(temp_set,temp)

    #plot
    temp = []
    for x in range (len(temp_set.sampled_data)):
        temp.append(temp_set.labels)
    temp_set.labels = temp
    temp_set = temp_set.bin_data(200,200)
    lines, x1 , y1 = update_plot2(fig ,num_channels-1, ax2, x1, y1,  lines, loop_counter, temp_set)
    #

    index = index + 200

    if (index > len(data[0])):
        index = 0 

    t2 = datetime.datetime.now()
    loop_counter = loop_counter +1

#print((t2 - t1).total_seconds())
#We now have finished collected data from the training set, now realigning our training set 
temp = []

for x in range (len(train_set.sampled_data)):
    temp.append(train_set.labels)
train_set.labels = temp

#finished accumulating data, time to bin and then train the data.

train_set = train_set.bin_data(200,200)
classes = train(train_set)

#now predicting
actual = []
rpredicted = []
msepredicted = []
cospredicted = []

count = 0

while index < len(data[0]) :#((t2 - t1).total_seconds() < 78): #This loop takes about 78 seconds to go through rest of the data
    test_set = Data()
    temp = grab_size(index, data, 200) 
    test_set = add_to_trainset(test_set,temp)

    temp = []
    for x in range (len(test_set.sampled_data)):
        temp.append(test_set.labels)
    test_set.labels = temp

    test_set = test_set.bin_data(200,200)
    a, r, mse, cos, cors = predict(test_set, classes)
    #plots
    update_plot1(fig,ax1,cors,a,r,mse,cos)
    
    lines, x1 , y1 = update_plot2(fig ,num_channels-1, ax2, x1, y1, lines, loop_counter, test_set)
    #end plots
    actual = concatenate(actual, a)
    rpredicted = concatenate(rpredicted, r)
    msepredicted = concatenate(msepredicted, mse)
    cospredicted = concatenate(cospredicted, cos)

    index = index + 200
    # if (index + 200 > len(data[0])):
    #     index = 0 

    #now we plot
    #

    time.sleep(0.1)
    t2 = datetime.datetime.now()
    count = count+1
    loop_counter = loop_counter + 1
    


#print((t2 - t1).total_seconds())
len1 = len(actual)

actual = [value for value in actual if value != 'pass']
rpredicted = [value for value in rpredicted if value != 'pass']
msepredicted = [value for value in msepredicted if value != 'pass']
cospredicted = [value for value in cospredicted if value != 'pass']
len2  = len(actual)

print()

print("Accuracy: ", round(accuracy_score(actual, rpredicted)*100,2), "%", "\tmatthews corr coef: ", round(matthews_corrcoef(actual, rpredicted),2),"\tF1: ", round(f1_score(actual, rpredicted, average = 'weighted'),2), sep = "")
print()
