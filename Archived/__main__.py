from Data_matrix import data_matrix_create, replace_placeholder
from Non_negative_matrix_factorization import NMF, NMF_round
from matplotlib.pyplot import plot, show
from numpy import nan, around, multiply, array, arange
from Daily_trends import daily_trends
from NTF import NTF

#data = data_matrix_create('./Data_Files/Trips_CD_2011.txt')
#data = replace_placeholder(data,nan,0)
#daily_trends(data)
#show()

file1 = open('./Data_Files/Reorganized/Link_order.txt','r')
file2 = open('./Data_Files/travel_times_2011.csv','r')
file3 = open('./Data_Files/Reorganized/Trips_2011.txt','w+')
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

file1.readline()
begin_node_ids = []
end_node_ids = []
link_lengths = []
for line in file1:
    a = line.split()
    begin_node_ids.append(a[0])
    end_node_ids.append(a[1])
    link_lengths.append(float(a[2]))

begin_enumerate = enumerate(begin_node_ids)

'''
for i in range(len(begin_node_ids)):
    for j in range(365*24-1):
        file3.write('0,')
    file3.write('0\n')
    print i
'''
for line in file2:
    a = line.split(',')
    indices = []
    for i,j in begin_enumerate:
        if j==a[0]:
            indices.append(i)
    for i in indices:
        if end_node_ids[i] == a[1]:
            link_id = i+1
    b = a[2].split()
    month, date = b[0].split('-')
    month = int(month)
    date = int(date)
    month -= 1
    date -= 1
    day = sum(months[0:month])+date
    hour = int(b[1].split(':')[0])
    file3.seek(0)
    for i in range(link_id):
        line = file3.readline()
    line = line.split(',')
    line[day*24+hour] = a[4]
    line = ','.join(line)
    file3.seek(0)
    for i in range(link_id-1):
        line = file3.readline()

file1.close()
file2.close()
file3.close()
