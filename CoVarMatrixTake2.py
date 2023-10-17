import pandas as pd
import numpy as np
import json
import flaskserver
import DTW
import matplotlib.pyplot as plt
import math
from statistics import mean

#Read the raw data written to the CSV
dfcsv = pd.read_csv('10120316.csv')

#Declare array values for x,y,z positional data
x = []
y = []
z = []

for index, row in dfcsv.iterrows():
    dfJsonToPy = json.loads(row['payload'].replace("'",'"'))#Replaces Single Quotes with Double Quotes 
    for data in dfJsonToPy:
        if data['name'] == 'accelerometer':
            x.append(data['values']['x'])
            y.append(data['values']['y'])
            z.append(data['values']['z'])

#Cast data into arrays so that they can be combined
x = np.array(x)
y = np.array(y)
z = np.array(z)

axes = np.vstack([x,y,z]) #Combines x,y,z positional data into single variable

print(axes)

#Use numpy library to compute the Covariance Matix
covar = np.cov(axes)

print(covar)

#Perform Eigen decomposition using Numpy Library
eig_vals, eig_vecs =  np.linalg.eig(covar)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)

scaled_eigvecs = [ eig_vals[0]*np.array(eig_vecs[0][:2]), eig_vals[1]*np.array(eig_vecs[1][:2]) ]
origin = [mean(x), mean(y)]

plt.scatter(x, y, color = 'blue', label = 'Raw Data')
plt.quiver(*origin, scaled_eigvecs[:,0], scaled_eigvecs[:,1], angles='xy', scale_units='xy', scale=1)

print('EigenVec 1 XY:\n%s' %scaled_eigvecs[0])
print('EigenVec 2 XY:\n%s' %scaled_eigvecs[1])

plt.xlabel("X Positional Data") 
plt.ylabel("Y Positional Data") 
plt.title("Projected 2D Data with Principal Components") 


plt.show()

