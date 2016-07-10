from Data_tensor import data_tensor_create, purge_nanlinks
from numpy import isnan, array
from time import time

###
###
### DO NOT RUN THE FOLLOWING CODE!!! TAKE BACKUP FIRST!!!
'''
time0 = time()
link_list = range(260000, 260855)
V = data_tensor_create(link_list = link_list, trips=1)
print 'Data tensor successfully created in',time()-time0,'seconds.'
V, nanlinkindices = purge_nanlinks(V, 60)
nanlinks = [link_list[i] for i in nanlinkindices]
print 'Nanlinks successfully purged in',time()-time0,'seconds.'

with open('./Data_Files/Reorganized/Full_Link_Ids.txt', 'a') as filename1:
    writeline = []
    for i in link_list:
        if i not in nanlinks:
            writeline.append(str(i))
            print i
    filename1.write(','.join(writeline)+',')
print 'Full_link_ids successfully recorded in',time()-time0,'seconds.'
with open('./Data_Files/Reorganized/Full_Link_Data.txt', 'a') as filename2:
    for link in V:
        writeline = []
        for entry in link.flatten():
            writeline.append(str(entry))
        filename2.write(','.join(writeline)+'\n')
print 'Full_links_data successfully recorded in',time()-time0,'seconds.'

'''
