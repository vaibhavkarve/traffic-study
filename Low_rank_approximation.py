#from sys import argv
from numpy import array, nan
from matplotlib.pyplot import plot, show

def mat_derivative(A=[0]):
    B = [[] for i in range((len(A)))]
    for i in range(len(A)):
        for j in range(len(A[i])-1):
            if A[i][j]==nan or A[i][j+1]==nan:
                B[i].append(nan)
            else:
                B[i].append(A[i][j+1]-A[i][j])
    return B


filenames = ['Trips_BA_2011.txt', 'Trips_AC_2011.txt',
             'Trips_CD_2011.txt', 'Trips_DB_2011.txt']
#filenames = ['Traveltimes_BA_2011.txt', 'Traveltimes_AC_2011.txt',
#             'Traveltimes_CD_2011.txt', 'Traveltimes_DB_2011.txt']

data = [[] for i in range(len(filenames))]

# Store readfile contents into list data.
for i in range(len(filenames)):
    with open(filenames[i], 'r') as readfile:
        for line in readfile:
            if len(line):
                data[i].append(float(line[0:-1]))
    # Rearrange data so that hours now increase instead of decreasing.
    data[i].reverse()

dM = mat_derivative(data)
print len(dM[0])

plot(dM[0],'bo')

for i in range(len(filenames)):
    data[i] = [j if j!=-1 else nan for j in data[i]]

dM = mat_derivative(data)
print len(dM[0])
plot(dM[0],'ro')
show()
