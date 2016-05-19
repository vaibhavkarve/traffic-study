"""Read database eg: travel_times_2011.csv, and return all lines that begin
with (begin_node,end_node). Preferable output file name: (link_id)_(year).txt
"""

from sys import argv

# Two additional arguments needed to run script: readfilename and writefilename
script, filename_r, filename_w = argv
BEGIN_NODE_ID = '42443561'  # Node B
END_NODE_ID = '42432703'    # Node D

file_r=open(filename_r,'r')
file_w=open(filename_w,'w')

# To simply copy all column labels
file_w.write(file_r.readline())

# Initialization
j = 0
i = "a"

# While i non-empty, read new line and store if relevant
while len(i):
    i = file_r.readline()
    if BEGIN_NODE_ID+','+END_NODE_ID in i[0:18]:
        file_w.write(i)
        j += 1
    print j

# 8760 = 24*365 is total number of hours in a non-leap year
print 'Amount of data missing = %d percent' %(int((8760-j) * 100.0 / 8760))

file_r.close()
file_w.close()
