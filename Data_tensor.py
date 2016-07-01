from numpy import array, nan, around, sum, isnan, copy, argmax
from time import time
from matplotlib.pyplot import plot, show
from NTF import NTF, SNTF

time0 = time()
'''
a = array([88, 69, 64, 65, 19, 93, 72, 100, 50, 22, 26, 63, 90, 39, 82, 58, 93,
           20, 18, 70, 70, 4, 77, 40, 89, 90, 90, 53, 19, 50])
b = array([51, 59, 63, 17, 82, 96, 19, 42, 36, 22, 72, 85, 49, 73, 99, 16, 58,
           55, 75, 64, 53, 82, 14, 94, 83, 48, 63, 5, 73, 91])
c = array([86, 74, 21, 49, 97, 68, 64, 67, 49, 73, 89, 18, 29, 48, 11, 80, 76,
           2, 19, 8, 22, 19, 75, 41, 25, 69, 58, 63, 88, 12])
d = array([12, 23, 0, 72, 86, 19, 8, 91, 24, 79, 23, 11, 69, 96, 87, 55, 18,
           80, 33, 77, 19, 10, 44, 11, 67, 0, 44, 99, 19, 19])
e = array([18, 36, 39, 55, 37, 68, 72, 90, 98, 17, 38, 62, 74, 77, 98, 61, 85,
           32, 84, 8, 95, 46, 71, 26, 96, 13, 31, 100, 59, 78])
f = array([98, 100, 80, 80, 15, 91, 15, 17, 72, 78, 96, 12, 88, 38, 44, 59, 11,
           12, 41, 41, 63, 63, 38, 34, 21, 82, 42, 53, 71, 77])
D = array([a,b,c,d,e,f,f,e,d,c,b,a,d,d,a,b,c,f,e,e,a])#(21,30)
W2, H2 = NTF2(D.T, 6, beta=10, eta=0.001) #(30,21) = (30,6)X(6,21)
[plot(range(6),H2[:,i],'o-') for i in range(21)]
show()
'''



readfile = open('./Data_Files/Reorganized/Dataset_2011.txt', 'r')

colors = 'bgrmyc'
links = 5000
V = []

for line in readfile:
    entries = line.split(',')
    #V.append([float(entries[i].split()[1]) if bool(entries[i]) else 0.0001
    #          for i in range(151940,links+151940)])
    V.append([float(entries[i].split()[1]) if bool(entries[i]) else nan
              for i in range(169000,links+169000)])
    
    print entries[0]
V = array(V).T.reshape(links,365,24)
print V.shape # (1000,365,24)

allowed_missing_days = 30
notnanlinks = [i for i in range(links) if sum(isnan(V[i])) <= V[i].size-24*allowed_missing_days]
print len(notnanlinks)
A = array([V[i] for i in range(links) if i in notnanlinks])
V = A
print V.shape

#print [sum(isnan(i)) for i in V]


print time()-time0
#W, H  = SNTF(V.T,2,1,1,0.001) #(24,365,nnl) = (24,365,2)X(2,nnl)
#W2, H2 = SNTF(V.T,2,1,1,0.001)
W, H = NTF(V.T,2,1,0)
#W2, H2 = NTF(V.T,2,1,0)
#a1 = array([argmax(H[:,i]) for i in range(len(notnanlinks))])
#a2 = array([argmax(H[:,i]) for i in range(len(notnanlinks))])
#print a1-a2
#plot(range(len(notnanlinks)),a1,'o')
#plot(range(len(notnanlinks)),a2,'o')
#[[plot(range(24),W[:,i,j], colors[j]) for i in range(30)] for j in range(2)]
[plot(range(2),H[:,i],colors[argmax(H[:,i])]) for i in range(len(notnanlinks))]
show()

readfile.close()
