import pandas as pd
import numpy as np
import json
import flaskserver

dfcsv = pd.read_csv('10120316.csv')

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

x = np.array(x)
y = np.array(y)
z = np.array(z)

axes = np.vstack([x,y,z]) #Combines x,y,z positional data into a stack of

print(axes)

covar = np.cov(axes)

print(covar)

eig_vals, eig_vecs =  np.linalg.eig(covar)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)
