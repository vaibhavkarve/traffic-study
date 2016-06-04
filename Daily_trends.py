'''Extract data corresponding to specified day of the week from a data matrix
of periodicity 7 days. Then, fit a cubic curve into data points and plot these
cubics on top of each other, one for each of the 53 weeks in year.
Input = ndarray with dimensions (53,24*7),
        day of the week (int between 0 to 6). Note that day=0 corresponds to
        the day of Jan 1 of that year. 'days' matrix needs to be changed for
        each year.
Output = plot of specified day. Use matplotlib.pyplot.show() in main.py to
        display plot.

Note that any week with a nan value will not get plotted. This can be corrected
by replace_placeholder() function from Data_matrix.py.
'''

from numpy import array, linspace
from scipy.interpolate import interp1d
from matplotlib.pyplot import plot, title, show

# For the year 2011, Jan 1 was a Saturday.
days = ['Saturdays', 'Sundays', 'Mondays', 'Tuesdays', 'Wednesdays',
        'Thursdays', 'Fridays']
# Colors of the graphs.
colors = 'cmygcmy'
#colors = 'rrbbbbb'


def daily_trends(data, day = 0):
    data = array(data)
    if day>6 or day<0:
        print 'Error: Incorrect value for day entered.'
        print 'Should be an integer with value in 0-6.'
        return None
    if len(data.T) != 24*7:
        print 'Data dimensions are not correct for carrying out daily_trends.'
        return None

    x = linspace(0, 23, num=1000, endpoint=True)
    for weekly_data in data:
        f = interp1d(range(24), weekly_data[day*24:(day+1)*24], kind = 'cubic')
        plot(x, f(x), colors[day])
    title(days[day])
    return None
