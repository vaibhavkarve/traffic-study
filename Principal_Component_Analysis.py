from sys import argv
from numpy import mean, var, matrix, argsort, concatenate
from numpy.linalg import eig

files = [open(i, 'r') for i in argv[1:5]]

data = [[] for file_counter in range(len(files))]

line = ' '
file_counter = 0
while (len(line)):
    for file_counter in range(len(files)):
        line = files[file_counter].readline()
        if len(line):
            data[file_counter].append(float(line))

data_known = [[] for counter in range(len(data))]
means = [0 for counter in range(len(data))]
data_corrected = [[] for counter in range(len(data))]
data_centred = [[] for counter in range(len(data))]
#variances = [[] for counter in range(len(data))]

            
for counter in range(len(data)):
    data[counter].reverse()
    data_known[counter]=[i for i in data[counter] if i!=-1]
    means[counter] = mean(data_known[counter])
    data_corrected[counter] = [i if i!=-1 else means[counter] for i in data[counter]]
    data_centred[counter] = [i-means[counter] for i in data_corrected[counter]]

n = matrix(data).shape[1]
covariance = 1./(n-1)*matrix(data_centred)*matrix(data_centred).T
eigenvals, eigenvecs = eig(covariance)
sorting = list(argsort(eigenvals))
sorting.reverse()
eigenvals = [eigenvals[i] for i in sorting]
eigenvecs = concatenate([eigenvecs[i] for i in sorting])

