from numpy import array, nan, isnan, sum

def data_tensor_create(filename='./Data_Files/Reorganized/Dataset_2011.txt',
                       link_list = [169017], trips = 1):
    # trips = 0 extracts speed data. trips = 1 extracts trips count data.
    with open(filename,'r') as readfile:
        V = [0 for i in range(365*24)]
        hourcounter = 0
        for line in readfile:
            entries = line.split(',')
            V[hourcounter] = [float(entries[i].split()[trips]) if bool(entries[i]) else nan for i in link_list]
            hourcounter += 1
            print entries[0]
    V = array(V).T.reshape(len(link_list),365,24)
    return V

def purge_nanlinks(data, allowed_nan_days = 364):
    # allowed_nan_days = 364 purges links which have less than 24 hours of
    # data on them.
    # allowed_nan_days = 0 purges links which have even a single data entry
    # missing.
    nanlinkindices = [i for i in range(len(data))
                      if sum(isnan(data[i])) > 24*allowed_nan_days]
    V = array([data[i] for i in range(len(data)) if i not in nanlinkindices])
    print 'Tensor of size',data.shape,'has now been reduced to',V.shape
    return V, nanlinkindices
