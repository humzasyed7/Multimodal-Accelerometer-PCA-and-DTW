import pandas as pd
import numpy as np
import json
import flaskserver
import matplotlib.pyplot as plt
import math
from statistics import mean
from sklearn.decomposition import PCA
from dtw import dtw
from fastdtw import fastdtw
from sklearn.svm import OneClassSVM

# Create a dictionary containing all the possible sensor types
all_sensor_data = {
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

# Read the raw data written to the CSV
dfcsv = pd.read_csv('10120316.csv')

# Read the data from the CSV to all_sensor_data
for label, series in dfcsv.iterrows():
    all_data = json.loads(series['payload'].replace("'",'"'))#Converts Json obj to Py obj, contains list of objects which each contain multiple fields (names, values, etc.)
    for data in all_data:
        sensor_name = data['name']
        if sensor_name in all_sensor_data:
            vals = list(data['values'].values())
            all_sensor_data[sensor_name].append(vals)

# Calculate the Covariance Matrix for each Sensor's Dataset
for sensor_name, data in all_sensor_data.items():
    if len(data) > 1:
        covar_mat = np.cov(data, rowvar = False)
        print("Covariance Matrix for %s:\n" %sensor_name, covar_mat )

def create_windows(data, window_size):
    return [data[i:i + window_size] for i in range(len(data) - window_size + 1)]

Window_Span = 10
windowed_sensor_data = {sensor: create_windows(data, Window_Span) for sensor, data in all_sensor_data.items()}

def pca_analysis(sensor_name, data, windows):
    if not data or len(data[0]) <= 1:  # Check if data is empty or not 2D
        return  # If so, skip the plotting for this sensor
    
    # Use sklearn library to perform PCA (Eigendecomposition of Covariance Matrix):
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(data)

    #To visualize the eigenvectors themselves, we'll take the Principal Components from the first window (size 10) and overlay the vectors on the PCA Transformed Data
    window = windows[sensor_name][0]

    # Get the PCA transformation of the first window
    first_pcs = pca.transform(window)

    # Plot the data with 2D PCA as vectors centered at the origin
    plt.figure(figsize=(10, 6))
    plt.scatter(pca_data[:, 0], pca_data[:, 1], alpha=0.5, label="PCA Transformed Data", color = 'green')
    # Plot eigenvectors (Principal Components)
    for pc in first_pcs:
        plt.arrow(0, 0, pc[0], pc[1], head_width=0.5, head_length=0.5, fc='blue', ec='blue')

    # Plot Aesthetics
    plt.legend()
    plt.grid(True)
    plt.title(f"2D PCA of {sensor_name} Data")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.grid(True)
    plt.show()


# Plot PCA for each sensor
for sensor_name in windowed_sensor_data:
    pca_analysis(sensor_name, all_sensor_data[sensor_name], windowed_sensor_data)





