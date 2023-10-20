import numpy as np
import pandas as pd
import json
import flaskserver
import matplotlib.pyplot as plt
import math
from statistics import mean
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean
from dtw import dtw
from fastdtw import fastdtw

s1_alldata = {
    "accelerometer": [],
    "gravity": [],
    "gyroscope": [],
    "orientation": [],
    "magnetometer": [],
    "barometer": [],
    "location": [],
    "microphone": [],
    "pedometer": [],
    "headphone": [],
    "battery": [],
    "brightness": [],
    "network": [],
}

s2_alldata = {
    "accelerometer": [],
    "gravity": [],
    "gyroscope": [],
    "orientation": [],
    "magnetometer": [],
    "barometer": [],
    "location": [],
    "microphone": [],
    "pedometer": [],
    "headphone": [],
    "battery": [],
    "brightness": [],
    "network": [],
}

#Read the raw data written to the CSV
csv1 = pd.read_csv('10120316.csv')
csv2 = pd.read_csv('19123034.csv')

#Read the data from the CSV and store in dictionaries
for label, series in csv1.iterrows():
    all_data = json.loads(series['payload'].replace("'",'"'))#Converts Json obj to Py obj, contains list of objects which each contain multiple fields (names, values, etc.)
    for data in all_data:
        sensor_name = data['name']
        if sensor_name in s1_alldata:
            vals = list(data['values'].values())
            s1_alldata[sensor_name].append(vals)

for label, series in csv2.iterrows():
    all_data = json.loads(series['payload'].replace("'",'"'))#Converts Json obj to Py obj, contains list of objects which each contain multiple fields (names, values, etc.)
    for data in all_data:
        sensor_name = data['name']
        if sensor_name in s2_alldata:
            vals = list(data['values'].values())
            s2_alldata[sensor_name].append(vals)

#Checks which sensors have data in both csv's
s1_keys = set()
s2_keys = set()
for s1_key, s1_data in s1_alldata.copy().items():
    if s1_data:
        s1_keys.add(s1_key)#Stores the names of sensors that recorded data
for s2_key, s2_data in s2_alldata.copy().items():
    if s2_data:
        s2_keys.add(s2_key)#Stores the names of sensors that recorded data
mutual_sensors = s1_keys.intersection(s2_keys)

#Implement DTW Algorithm on two time series streams from the same sensor
for sensor in mutual_sensors:
    #print(s1_alldata[sensor][:2])
    #print(s2_alldata[sensor][:2])
    distance, path = fastdtw(np.array(s1_alldata[sensor]), np.array(s2_alldata[sensor]), dist = euclidean)
    print('The DTW Distance is: %s' %distance)



