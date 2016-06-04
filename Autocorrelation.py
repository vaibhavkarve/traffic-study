'''Function measures autocorrelation of data. Reads trips data or traveltimes
data and return a plot of autocorrelation coefficient for each period value in
a specified interval, for each specified file.
INPUT = Start period value, End period value
OUTPUT = a plot showing autocorrelation coefficients for each file in
        'filenames'.
        To display plot, use matplotlib.pyplot.show() in main.py.
Note: Peaks in plot correspond to high autocorrelation i.e. high periodicity
trend.
'''

from matplotlib.pyplot import plot, xlabel, ylabel, show, legend
from numpy import nanmean, nanvar

from Data_matrix import data_list_create, replace_placeholder

filenames = ['./Data_Files/Trips_BA_2011.txt',
             './Data_Files/Trips_AC_2011.txt',
             './Data_Files/Trips_CD_2011.txt',
             './Data_Files/Trips_DB_2011.txt']
# OR
#filenames = ['./Data_Files/Traveltimes_BA_2011.txt',
#             './Data_Files/Traveltimes_AC_2011.txt',
#             './Data_Files/Traveltimes_CD_2011.txt',
#             './Data_Files/Traveltimes_DB_2011.txt']

def autocorrelation_analysis(START_PERIOD = 1, END_PERIOD = 38):
    for filename in filenames:
        data = data_list_create(filename)
        data = replace_placeholder(data, value = nanmean(data))
        sigma2 = nanvar(data)
        deviations = [i-nanmean(data) for i in data]
        Autocorrelations = {period:0 for period in
                            range(START_PERIOD, END_PERIOD+1)}
        for period in range(START_PERIOD, END_PERIOD+1):
            # Convert period in days to period in hours as 24*period.
            autocorr = nanmean([deviations[i]*deviations[i+24*period]
                                for i in range(len(data)-24*period)])/sigma2
            Autocorrelations[period] = autocorr

        # Peaks in plot correspond to high autocorrelation i.e. high
        # periodicity trend.
        plot(Autocorrelations.keys(), Autocorrelations.values(),
             'o-', label=filename)

    ylabel('Autocorellations(period)')
    xlabel('Assumed period of data')
    legend(bbox_to_anchor=(1.35, 0.95))
    return None
