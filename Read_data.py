from Globals import filenames_PC as filenames


# Reads a csv and returns a list of dictionaries, one for each line
# with first line in csv as keys. Use only for 'links' and 'nodes'. 
def csv_to_dict(filename):
    from csv import DictReader
    with open(filenames[filename], 'rb') as readfile:
        return list(DictReader(readfile))
        

# Search through links_dict to return information for a specific link_id.
# links_dict should be output of csv_to_dict(filenames['links'])
def link_id_info(links_dict, link_id):
    for line in links_dict:
        if line['link_id'] == str(link_id):
            return line


# Reorganize links_dict to assign link_id (as string) to
# begin_node_id, end_node_id pair.
def nodes_to_link_id(links_dict):
    nodes_to_links_dict = {}
    for link in links_dict:
        nodes_to_links_dict[link['begin_node_id']
                            +','
                            +link['end_node_id']] = link['link_id']
    return nodes_to_links_dict


# Input is line from DictReader(csvfile).
def extract_data_from_line(line):
    calendar_days = {'01':0, '02':31, '03':59, '04':90, '05':120,
                         '06':151, '07':181, '08':212, '09':243, '10':273,
                         '11':304, '12':334}
    date, hour = line['datetime'].split()
    month, day = date.split('-')[1:3]
    hour = int(hour[0:2])
    begin_node_id = line['begin_node_id']
    end_node_id = line['end_node_id']
    time = calendar_days[month]*24 + (int(day)-1)*24 + hour
    return time, begin_node_id+','+end_node_id,\
           line['num_trips'], line['travel_time']


# Read raw data file and return rows, columns, entries as lists.
# rows is a list of ints.
# columns_offset_by_one is a list of strings.
# entries is a list of strings.
def read_data_csv():
    from csv import DictReader
    key = 'num_trips'
    key = 'travel_time'
        
    with open(filenames['raw_data'], 'rb') as csvfile:
        reader = DictReader(csvfile)
        links_dict = nodes_to_link_id(csv_to_dict('links'))
        
        times, nodes, entries1, entries2 =\
               map(list,zip(*[extract_data_from_line(line) for line in reader]))
        
        rows = []
        columns_offset_by_one = []
        trips = []
        travel_times = []
        for i in range(len(times)):
            if nodes[i] != '0,0':
                rows.append(times[i])
                columns_offset_by_one.append(links_dict[nodes[i]])
                trips.append(entries1[i])
                traveltimes.append(entries2[i])
    return rows, columns_offset_by_one, trips, traveltimes


def write_data_coo((rows, columns_offset_by_one, trips, traveltimes)):
    with open(filenames['data_coo_form'],'wb') as writefile:
            rows = ','.join(map(str, rows))
            columns_offset_by_one = ','.join(columns_offset_by_one)
            trips = ','.join(trips)
            traveltimes = ','.join(traveltimes)
            writefile.write('rows='+rows+'\n')
            writefile.write('columns_offset_by_one='+columns_offset_by_one+'\n')
            writefile.write('trips='+trips+'\n')
            writefile.write('travel_times='+traveltimes+'\n')
    return None


def write_data_array():
    from time import time
    from numpy import array
    time0 = time()

    with open(filenames['data_coo_form'],'rb') as readfile:
        rows, columns_offset_by_one, trips, traveltimes = readfile.readlines()

    rows = map(int, rows[5:].split(','))
    print 'Rows converted to ints,',time()-time0
    # columns_offset_by_one start at 1 because they are link_ids.
    # columns start at 0.
    columns_offset_by_one = map(int, columns_offset_by_one[22:].split(','))
    print 'Columns converted to ints,',time()-time0
    trips = trips[6:].split(',')
    print 'Trips were read,',time()-time0
    traveltimes = traveltimes[13:].split(',')
    print 'Travel times were read,',time()-time0
    # We reverse all the arrays so that we can write data to the new csv file
    # starting at hour 0 instead of 8759.
    rows.reverse()
    columns_offset_by_one.reverse()
    trips.reverse()
    traveltimes.reverse()
    time = rows[0]
    line_trips = ['' for j in range(260856)]
    line_traveltimes = ['' for j in range(260856)]
        
    with open(filenames['data_trips'],'wb') as writefile_trips,\
         open(filenames['data_traveltimes'],'wb') as writefile_traveltimes:
        for i in range(len(rows)):
            if time == rows[i]:
                line_trips[columns_offset_by_one[i]-1] = trips[i]
                line_traveltimes[columns_offset_by_one[i]-1] = traveltimes[i]
            else:
                time += 1
                writefile_trips.write(','.join(line_trips)+'\n')
                writefile_traveltimes.write(','.join(line_traveltimes)+'\n')
                line_trips = ['' for j in range(260856)]
                line_traveltimes = ['' for j in range(260856)]
                line_trips[columns_offset_by_one[i]-1] = trips[i]
                line_traveltimes[columns_offset_by_one[i]-1] = traveltimes[i]

        writefile_trips.write(','.join(line_trips)+'\n')
        writefile_traveltimes.write(','.join(line_traveltimes)+'\n')
    return None


def find_full_links():
    with open(filenames['data_coo_form'], 'rb') as coofile:
	print 'data_coo_form.txt is opened'
	coofile.readline()
	print 'First line is read and skipped'
	columns_offset = coofile.readline()[22:].split(',')
	print 'columns_offset was read successfully.'
    full_link_ids = []
    # 30 represents the number of allowed nan_days.
    for link_id in range(1,260856+1):
        if columns_offset.count(str(link_id)) >= (365-30)*24:
            full_link_ids.append(link_id)
            print link_id
    return full_link_ids


def write_full_link_data():
    from csv import reader
    from json import dump
    from numpy import nan
    with open(filenames['full_link_ids'],'rb') as readfile:
        full_link_ids = list(reader(readfile))[0]
        full_link_ids = map(int, full_link_ids)
    V = []
    with open(filenames['data_trips'],'rb') as readfile:
        reader = reader(readfile)
        for line in reader:
            V.append(map(float, [line[i-1] if bool(line[i-1]) else nan
                                 for i in full_link_ids]))
            print reader.line_num
    dump(V, open(filenames['full_link_trips'], 'wb'))

    V = []
    with open(filenames['data_traveltimes'],'rb') as readfile:
        reader = reader(readfile)
        for line in reader:
            V.append(map(float, [line[i-1] if bool(line[i-1]) else nan
                                 for i in full_link_ids]))
            print reader.line_num
    dump(V, open(filenames['full_link_traveltimes'], 'wb'))
    return None


# Use the following when you wish to read the array for only 2302 full links.
def read_full_link_json(trips = 1):
    from csv import reader
    from json import load
    from numpy import array
    with open(filenames['full_link_ids'],'rb') as readfile:
        full_link_ids = list(reader(readfile))[0]
        full_link_ids = map(int, full_link_ids)
    if trips == 0:
        filename = filenames['full_link_traveltimes']
    elif trips == 1:
        filename = filenames['full_link_trips']
    else:
        print 'Error: invalid argument'
        return None
    V = load(open(filename, 'rb'))
    return full_link_ids, array(V)


from numpy import nan
def replace_placeholder(data, placeholder = nan, value = 0.):
    from numpy import isnan, array
    if isnan(placeholder):
        V = [i if ~isnan(i) else value for i in data.flatten()]
    else:
        V = [i if i!=placeholder else value for i in data.flatten()]
    return array(V).reshape(data.shape)


def autocorrelation(data):
    from matplotlib.pyplot import plot, xlabel, ylabel, show
    from numpy import nanmean, nanvar, mean, multiply, arange
    # We choose 38 days as the max possible periodicity in traffic.
    START_PERIOD = 1
    END_PERIOD = 38
    V = replace_placeholder(data, value = nanmean(data))
    # We don't take the variance of entries that we replaced with nanmean.
    sigma2 = nanvar(data)
    autocorr_dict = {period:0 for period in range(START_PERIOD,END_PERIOD+1)}
    Deviations = V - nanmean(V, axis=0)
    for period in range(START_PERIOD, END_PERIOD+1):
        # Convert period in days to period in hours as 24*period.
        autocorr = nanmean([multiply(Deviations[t],Deviations[t+24*period])
                            for t in range(len(V)-24*period)])/sigma2
        autocorr_dict[period] = autocorr
        print period

    # Peaks in plot correspond to high autocorrelation i.e. high
    # periodicity trend.
    plot(arange(START_PERIOD-0.5, END_PERIOD-0.5+1),
         [autocorr_dict[period] for period in range(START_PERIOD, END_PERIOD+1)],
         'o-')

    ylabel('Average autocorellation over full links')
    xlabel('Assumed period of data (in days)')
    show()
    #legend(bbox_to_anchor=(1.35, 0.95))
    return None

def autocorrelation_hourly(data):
    from matplotlib.pyplot import plot, xlabel, ylabel, show
    from numpy import nanmean, nanvar, mean, multiply, arange
    # We choose 7 days and plus-minus 6 hours as the possible periodicity
    # in traffic.
    START_PERIOD = 7*24 - 6
    END_PERIOD = 7*24 + 6
    V = replace_placeholder(data, value = nanmean(data))
    # We don't take the variance of entries that we replaced with nanmean.
    sigma2 = nanvar(data)
    autocorr_dict = {period:0 for period in range(START_PERIOD,END_PERIOD+1)}
    Deviations = V - nanmean(V, axis=0)
    for period in range(START_PERIOD, END_PERIOD+1):
        autocorr = nanmean([multiply(Deviations[t],Deviations[t+period])
                            for t in range(len(V)-period)])/sigma2
        autocorr_dict[period] = autocorr
        print period

    # Peaks in plot correspond to high autocorrelation i.e. high
    # periodicity trend.
    plot(arange(START_PERIOD, END_PERIOD+1),
         [autocorr_dict[period] for period in range(START_PERIOD, END_PERIOD+1)],
         'o-')

    ylabel('Average autocorellation over full links')
    xlabel('Assumed period of data (in hours)')
    show()
    #legend(bbox_to_anchor=(1.35, 0.95))
    return None

'''
from matplotlib.pyplot import plot, show
full_link_ids, V = read_full_link_json(trips=1)
print type(full_link_ids[0])
print full_link_ids.index(169017)
[plot(range(24), V[i*24:(i+1)*24,1]) for i in range(7)]
show()
'''


















