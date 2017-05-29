from Globals import *
from numpy import *
from numpy.linalg import norm, cond
from random import random
from matplotlib.pyplot import plot, show, imshow, colorbar


W = loadtxt('./Data_Files/Seeded_0,1/W_trips.txt')
H = loadtxt('./Data_Files/Seeded_0,1/HT_trips.txt').T
Ha = loadtxt('./Data_Files/Seeded_0,1/HT_trips_axed.txt').T

W2 = loadtxt('./Data_Files/05_23/W_trips.txt')
H2 = loadtxt('./Data_Files/05_23/HT_trips.txt').T
Ha2 = loadtxt('./Data_Files/05_23/HT_trips_axed.txt').T

print 'W_mins=', W.min(), W2.min()
print 'W_maxs=', W.max(), W2.max()
print 'H_mins=', H.min(), H2.min()
print 'H_maxs=', H.max(), H2.max()
print 'Random conditon number=',\
      cond(array([random() for i in range(HOURS_IN_YEAR*RANK
                                          )]).reshape(HOURS_IN_YEAR,RANK))

plot([cond(W.T[0:i]) for i in range(1,len(W.T))], 'o-')
plot([cond(W2.T[0:i]) for i in range(1,len(W2.T))], 'o-')
show()

#for i in range(len(W.T)):
#    print sum(W.T[i]**2)

Correlation = [corrcoef(W.T[i],W2.T[j])[0,1] for i in range(50)\
               for j in range(50)]
Correlation = array(Correlation).reshape(50,50)

heatmap = imshow(Correlation, interpolation='nearest')
heatmap.set_cmap('nipy_spectral')
colorbar()
show()


column_entries = [0 for i in range(len(Ha.T))] # list of length 2302
for i in range(len(Ha)): # i varies from 0 to 49
    for j in range(len(Ha.T)): # j varies from 0 to 2301
        if Ha[i,j] != 0:
            column_entries[j] += 1 # Counts number of nonzero entries
                                       # in each column of H

popularity = []
for i in range(len(Ha)):
    popularity.append(0)
    for j in range(len(Ha.T)):
        if Ha[i,j] != 0:
            popularity[i] += 1./column_entries[j]

plot(popularity)

column_entries = [0 for i in range(len(Ha2.T))] # list of length 2302
for i in range(len(Ha2)): # i varies from 0 to 49
    for j in range(len(Ha2.T)): # j varies from 0 to 2301
        if Ha2[i,j] != 0:
            column_entries[j] += 1 # Counts number of nonzero entries
                                       # in each column of H

popularity = []
for i in range(len(Ha2)):
    popularity.append(0)
    for j in range(len(Ha2.T)):
        if Ha2[i,j] != 0:
            popularity[i] += 1./column_entries[j]

plot(popularity)
show()
