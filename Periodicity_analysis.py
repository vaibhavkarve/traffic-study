'''Read file (either output of Traveltime_and_trips.py) and by treating data as
stratified with stratum size = 'period' days, ruturns graph of optimal period.
'''

from sys import argv
from numpy import mean, var
from matplotlib.pyplot import plot, xlabel, ylabel, axis, show

# Store readfile contents into list data.
with open(argv[1], 'r') as readfile:
    data = []
    for line in readfile:
        if len(line):
            data.append(float(line[0:-1]))

# Rearrange data so that hours now increase instead of decreasing.
data.reverse()

# Assume different 'periods' in the data, seperate data into bins and calculate
# variance for data srtatified thusly.
START_PERIOD_VALUE = 2
END_PERIOD_VALUE = 39
cumulative_strata_variances = {period:0 for period in
                               range(START_PERIOD_VALUE, END_PERIOD_VALUE+1)}

for period in range(START_PERIOD_VALUE, END_PERIOD_VALUE + 1):
    # Convert period in days to period in hours.
    period_in_hours = 24 * period
    # Initialization
    stratified_data = [[] for i in range(period_in_hours)]
    stratified_data_inferred = [[] for i in range(period_in_hours)]
    stratified_means = [0 for i in range(period_in_hours)]
    stratified_variances = [0 for i in range(period_in_hours)]
    # Stratify the data, ignore '-1' values.
    for i in range(len(data)):
        hour = i % period_in_hours
        if data[i] != -1:
            stratified_data[hour].append(data[i])
    # Record means of each stratum (we've ignored the '-1' values).
    for i in range(period_in_hours):
        stratum_mean = round(mean(stratified_data[i]), 2)
        stratified_means[i] = stratum_mean
    # Replace '-1' (missing) values with  stratum mean. This is inferred data,
    # no more true data.
    for i in range(len(data)):
        hour = i % period_in_hours
        if data[i] != -1:
            stratified_data_inferred[hour].append(data[i])
        else:
            stratified_data_inferred[hour].append(stratified_means[hour])
    # Record variance of each stratum
    for i in range(period_in_hours):
        stratum_variance = round(var(stratified_data_inferred[i]), 2)
        stratified_variances[i] = stratum_variance
    # Record the mean of stratum variances across all strata
    cumulative_strata_variances[period] = mean(stratified_variances)
    print ("Period = %d, Cumulative Strata Variance = %d"
           %(period, cumulative_strata_variances[period]))

# Dips in plot correspond to low cumulative variance i.e. high periodicity
# trend.
plot(cumulative_strata_variances.keys(),
     cumulative_strata_variances.values(),'o')
ylabel('Cumulative variance of stratified data')
xlabel('Assumed period of data')
show()
