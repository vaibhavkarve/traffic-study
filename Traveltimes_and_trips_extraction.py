'''Uses data for fixed link to return two files: one for Travel times in
seconds and second for No. of Trips respectively.
'''

from numpy import nan   # nan stands for Not-A-Number. We use it as a
                        # placeholder for missing values in our data

def traveltimes_and_trips(readfile = './Data_Files/Link_BA_2011.txt',
                          traveltimesfile =
                          './Data_Files/Traveltimes_BA_2011.txt',
                          tripsfile = './Data_Files/Trips_BA_2011.txt'):
    # One read-file, two write-files for Travel times and Trips respectively.
    # 'w+' gives both read & write permissions.
    traveltimes = open(traveltimesfile, 'w+')
    trips = open(tripsfile , 'w+')

    with open(readfile, 'r') as linkdata:
        # To skip column headings in read-file.
        linkdata.readline()
        # hour always considered mod 24.(hour=0)=>midnight.First reading should
        # be 23:00-midnight
        hour = 23
    
        for line in linkdata:
            # Removes leading & trailing whitespaces
            line = line.strip()
        
            # While line non-empty, write entry before ',' into traveltimes,
            # remaining into trips.
            while len(line):
                if len(line) and hour == (int(line[29:31])%24):
                    traveltimes.write(line[38:line.index(',',38)]+'\n')
                    trips.write(line[line.index(',',38)+1:len(line)]+'\n')
                    # Hours in readfile are indexed backwards.
                    hour -= 1; hour %= 24
                    break
                else:
                    # nan denotes missing values.
                    traveltimes.write('nan\n')
                    trips.write('nan\n')
                    hour -= 1; hour %= 24
        # In case the file is trailing with missing values, write some
        # more nan's.
        while hour != 23:
            traveltimes.write('nan\n')
            trips.write('nan\n')
            hour -= 1; hour %= 24

    # Uncomment following code if you with to get rid of trailing newline
    # character in writefiles.
    ##traveltimes.seek(0)
    ##for line in traveltimes:
    ##    traveltimes.write(line.strip())
    ##for line in trips:
    ##    trips.write(line.strip())

    traveltimes.close()
    trips.close()
