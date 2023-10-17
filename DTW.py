import numpy as np

def distance(x,y):
    return abs(x-y)

def dtwEA(stream1, stream2, threshold):
    d = np.full((len(stream1),len(stream2)), np.inf)
    for j in range(len(stream2)):
        d[0][j] = distance(stream1[0], stream2[j])
    for i in range(len(stream1)):
        d[i][0] = distance(stream1[i], stream2[0])
    for i in range(1,len(stream1)):
        for j in range(1,len(stream2)):
            cost = [d[i-1][j],d[i][j-1],d[i-1][j-1]]
            cost = [i for i in cost if i != np.inf] 
            if not cost:
                continue
            d[i][j] = distance(stream1[i],stream2[j]) + min(cost)
            if d[i][j] > threshold:
                d[i][j] = np.inf

    i, j = len(stream1)-1,len(stream2)-1
    shortestPath = [d[i][j]]
    while i != 0 and j !=0:
        cost = [d[i-1][j],d[i][j-1],d[i-1][j-1]]
        minP = min(cost)
        if minP == cost[0]:
            i -= 1
        elif minP == cost[1]:
            j -= 1
        elif minP == cost[2]:
            i -= 1
            j -= 1
        shortestPath.append(minP)

    distanceP = np.sum(shortestPath)/len(stream1)
    return distanceP