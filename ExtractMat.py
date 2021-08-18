import scipy.io as sio
import os
import numpy as np
import pandas as pd
import rdata

def get_mat_data():
    '''
    Function that returns the data of all the matlab data in the Zhang_Desimone_7objects_raster_data folder in the form
    of a list where each index corresponds to the data of one file
    Each index has the following information:
    raster_data is times from -500 to 500 and the data corresponding to these times
    raster_labels labels contains the position and ID (type of image shown)
    raster site info is the site info session ID, recording channel and the unit
    '''
    temp = os.path.join(os.getcwd(), "Zhang_Desimone_7objects_raster_data")
    mat_contents = []
    i = 1
    for name in os.listdir(temp):
        mat_contents.append(sio.loadmat("Zhang_Desimone_7objects_raster_data/"+name))

    parsed = rdata.parser.parse_file("ZD_150bins_50sampled.Rda")
    converted = rdata.conversion.convert(parsed)
    converted = converted['binned_data']
    return mat_contents, converted