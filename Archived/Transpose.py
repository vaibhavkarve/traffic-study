import Globals
filenames = Globals.filenames_PC

from time import time
time0 = time()
with open('../../data_travel_times.csv','rb') as readfile:
    lis = [x.strip().split(',') for x in readfile]
    print time()-time0

with open('../../data_travel_times_transpose.csv','wb') as writefile:
    i=0
    for x in zip(*lis):
        print i
        i+=1
        writefile.write(','.join(x)+'\n')
