'''Function reads file (either output of Traveltime_and_trips.py) and by
treating data as stratified with stratum size = 'period' days, ruturns
dictionary of cumulative strata variances. These can then be graphed to
figure out the optimal period.
Input = filename, starting integer, ending integer.
Output = a dictionary

Note: For graphing, include following lines into main.py:
from matplotlib.pyplot import plot, xlabel, ylabel, axis, show
# Dips in plot correspond to low cumulative variance i.e. high periodicity
# trend.
plot(cumulative_strata_variances.keys(),
     cumulative_strata_variances.values(),'o')
ylabel('Cumulative variance of stratified data')
xlabel('Assumed period of data')
show()
'''

# nanmean() calculates mean by ignoring nan's. nanvar() calculates variance by
# ignoring nan's
from numpy import nanmean, nanvar 

from Data_matrix import data_matrix_create
from Data_matrix import replace_placeholder

def periodicity_analysis(readfile = './Data_Files/Trips_BA_2011.txt',
                         START_PERIOD = 1, END_PERIOD = 38):
    cumulative_strata_variances = {period:0 for period in
                                   range(START_PERIOD, END_PERIOD + 1)}
    # Assume different 'periods' in the data, seperate data into bins and
    # calculate variance for data stratified thusly.
    for period in range(START_PERIOD, END_PERIOD + 1):
        data_stratified = data_matrix_create(readfile, period)
        data_variances = nanvar(data_stratified, axis=1)
        cumulative_strata_variances[period] = nanmean(data_variances)
    return cumulative_strata_variances
