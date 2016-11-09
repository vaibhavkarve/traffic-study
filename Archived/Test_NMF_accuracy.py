from Data_matrix import *
from Non_negative_matrix_factorization import*
from Daily_trends import *

from matplotlib.pyplot import plot, show
from numpy import arange, mean
from numpy.random import choice
from math import sqrt

data = data_matrix_create('./Data_Files/Traveltimes_AC_2011.txt')
W, H = NMF(data,2)
matrix = dot(W,H)

data = replace_placeholder(data,nan,0.0001)

mean1 = mean(matrix)
mean2 = mean(data)

matrix_errors = []
data_errors = []

'''
for percentage in arange(0.05,0.8,0.05):
    matrix = matrix.flatten()
    data = data.flatten()
    for i in choice(matrix.size, int(percentage*matrix.size), replace=False):
        matrix[i] = 0.001
        data[i] = 0.001

    matrix = matrix.reshape(168,53)
    data = data.reshape(168,53)


    W2, H2 = NMF(matrix,2)
    matrix2 = dot(W2,H2)

    W3, H3 = NMF(data,2)
    data2 = dot(W3,H3)

    matrix_errors.append(sqrt(sum((matrix-matrix2)**2)/matrix.size)/mean1)
    data_errors.append(sqrt(sum((data-data2)**2)/data.size)/mean2)
    #print sum(isnan(data2))

plot(arange(0.05,0.8,0.05),matrix_errors)
plot(arange(0.05,0.8,0.05),data_errors)
show()
'''


from numpy import arange, argmax, mean, var
from matplotlib.pyplot import bar, xticks, xlabel, ylabel, title, hist
from matplotlib.mlab import normpdf

percentage = 0.2
data2 = data.flatten()
for i in choice(data2.size, int(percentage*data2.size), replace=False):
    data2[i] = 0.001

data2 = data2.reshape(168,53)

W3, H3 = NMF(data,2)
data3 = dot(W3,H3)

#errors = (data-data2).flatten()
errors = (data2-data3)
#errors = array([[j if (j>10 or j<-50) else nan for j in i] for i in errors])
errors = [[errors[i,j] if data[i,j]>=1 else nan
               for j in range(len(errors[i]))]
              for i in range(len(errors))]
errors = errors/data
#for i in datapoints:
#    for j in i:
#        if ~isnan(j):
#            print j

#print errors.shape
for i in range(53):
    plot(range(168), errors[:,i], 'o')
    xlabel('Hours of the week')
    ylabel('Relative error')
show()




'''
mu = mean(errors)
sigma = sqrt(var(errors))
n,bins,patches = hist(errors,bins=100, normed=True, range = (-50,50), alpha=0.7)
y = normpdf(bins, mu, sigma)
plot(bins, y, 'r-')
show()
'''
