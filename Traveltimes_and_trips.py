'''Uses data for fixed link to return two files: one for Travel times in
seconds and second for No. of Trips respectively.
'''

from sys import argv

# One read-file, two write-files for Travel times and Trips respectively.
# 'w+' gives both read & write permissions.
traveltimes = open(argv[2], 'w+')
trips = open(argv[3] , 'w+')

with open(argv[1], 'r') as linkdata:
    # To skip column headings in read-file.
    linkdata.readline()
    # hour always considered mod 24.(hour=0)=>midnight.
    hour = 0
    
    for line in linkdata:
        # Removes leading & trailing whitespaces
        line = line.strip()

        # While line non-empty, write entry before ',' into traveltimes,
        # remaining into trips.
        while len(line):
            if hour == (int(line[29:31])%24):
                traveltimes.write(line[38:line.index(',',38)]+'\n')
                trips.write(line[line.index(',',38)+1:len(line)]+'\n')
                # Hours in readfile are indexed backwards.
                hour -= 1; hour %= 24
                break
            else:
                # '-1' denotes missing values.
                traveltimes.write('-1\n')
                trips.write('-1\n')
                hour -= 1; hour %= 24

# Uncomment following code if you with to get rid of trailing newline character
# in writefiles.
##traveltimes.seek(0)
##for line in traveltimes:
##    traveltimes.write(line.strip())
##for line in trips:
##    trips.write(line.strip())

traveltimes.close()
trips.close()
