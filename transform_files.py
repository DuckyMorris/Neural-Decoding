from ExtractMat import get_mat_data
import numpy as np
import pandas as pd
from TransformRaster import transform_raster
import datetime
import time
import pickle
from data import Data
from ml import train, predict
import csv
#Goals of this program:
#This program converts the matlab files to other formats compatible for different programs in this directory
#Running each time slightly alters the order of the pseudo populations and overwrites the picklefiles to give 
#a slightly different version to test the algorithms. 

NeuralData, BinnedData = get_mat_data() 
#Extracts matlab data
#Binned data has 420 entries for each neuron, where each entry is 1 second of data. 

#Neural data is of length 132 and holds the raster data for each neuron. 
#Each entry in Neural data is a dictionary with 'raster_data', 'raster_labels' and 'raster_site_info'

sampled_data, labels, timestaps = transform_raster(NeuralData) #sampled data now contains neural samples of 132 neurons, sampled at 1000Hz for 420 seconds. (132 x 420000)
        

with open('sampled_data.pkl', 'wb') as f:
    pickle.dump(sampled_data, f)
    
with open('times.pkl', 'wb') as f:
    pickle.dump(timestaps, f)

with open('labels.pkl', 'wb') as f:
    pickle.dump(labels, f)

    
data = Data()
#we need to select which neurons we want to work with 

data.sampled_data = sampled_data
data.labels = labels
data.time_stamps = timestaps
binned_data = data.bin_data(150,50)

with open('binned.pkl', 'wb') as f:
    pickle.dump(binned_data, f)

#Here we convert to a format that mimics the spike sorted open_ephys data
data = []
data.append(labels[0])
for x in range(len(sampled_data)):
    data.append(sampled_data[x])

with open('openephys.pkl', 'wb') as f:
    pickle.dump(data, f)




