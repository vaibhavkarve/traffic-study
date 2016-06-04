'''1. data_list_create reads a file line-by-line. Starts with an empty list,
    appends numbers from file and finally, reverses the list.
    Input = name of readfile
    Output = list
2. data_matrix_create does what data_list_create does, but stores data into a
    matrix (of type array) by imposing a periodicity on the data.
    Input = name of readfile, period (in days)
    Output = array of size ()
3. replace_placeholder replaces all entries of value placeholder in a
    list/ndarray with a specified value.
    Input = list or ndarray, placeholder (default=nan), value
    Output = list, if input type was list.
            array, if input type was ndarray. It retains the shape of input.
4. matrix_derivative finds column-wise derivative of an ndarray.
    Input = ndarray
    Output = ndarray of columnwise derivative.
5. matrix_integrate finds column-wise integration of an ndarray, with given
    initial vector.
    Input = ndarray, initial_vector (which is treated as first column of the
            output.
    Output = ndarray
    Note: matrix_integrate is the inverse function of matrix_derivative
'''

from numpy import nan, array, nanmean, nanvar, ndarray, isnan


def data_list_create(readfilename = './Data_Files/Trips_AC_2011.txt'):
    with open(readfilename, 'r') as readfile:
        data = []
        for line in readfile:
            if len(line):
                data.append(float(line[0:-1]))

    # Rearrange data so that hours now increase instead of decreasing.
    data.reverse()
    return list(data)


def data_matrix_create(readfilename = './Data_Files/Trips_AC_2011.txt',
                       PERIOD = 7):
    data = data_list_create(readfilename)
    PERIOD = int(PERIOD)
    # PERIOD is specified in days. (PERIOD in hours) = 24*(PERIOD in days).
    # In order to divide data into bins of length 24*PERIOD, len(data) should
    # be a multiple. If not, append nan's.
    while len(data)%(24*PERIOD) != 0:
        data.append(nan)
    data = array(data).reshape(len(data)/(24.*PERIOD), 24*PERIOD)
    return data


def replace_placeholder(data, placeholder = nan, value = 0):
    data_type = type(data)
    if data_type is ndarray:
        shape = data.shape
        data = list(data.flatten())
    if isnan(placeholder):
        data = [i if ~isnan(i) else value for i in data]
    else:
        data = [i if i!=placeholder else value for i in data]
    if data_type is list:
        return data
    elif data_type is ndarray:
        return array(data).reshape(shape)
    else:
        print 'Error: check type() of data\n'
        return None


def matrix_derivative(data):
    data = array(data)
    data_T = data.T     # We want column-wise derivative.
    difference = []
    for i in range(len(data_T)-1):
        difference.append(data_T[i+1]-data_T[i])
    return array(difference).T


def matrix_integrate(data, initial_vector):
    data = array(data)
    initial_vector = list(initial_vector)
    data_T = data.T     # We want column-wise integration
    integration = [initial_vector]
    for i in range(len(data_T)):
        integration.append(integration[i] + data_T[i])
    return array(integration).T
