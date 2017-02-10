import Globals
filenames = Globals.filenames_PC
RANK  = Globals.RANK
TRIPS = Globals.TRIPS
TOTAL_LINKS = Globals.TOTAL_LINKS
FULL_LINKS = Globals.FULL_LINKS
HOURS_IN_YEAR = Globals.HOURS_IN_YEAR



def entropy():
    from numpy import loadtxt
    from math import log

    W = loadtxt('./W_sorted.txt')
    H = loadtxt('./H_sorted.txt')

    counts = {i:0 for i in range(1,12)}
    for link in range(FULL_LINKS):
        counts[sum([bool(entry) for entry in H.T[link]])] += 1

    probs = [counts[i]/float(FULL_LINKS) for i in counts.keys()]
    print -sum([probs[i]*log(probs[i]) for i in range(len(probs))])
    
    return None


def find_decomposition(trend, W):
    from numpy import array, isnan, dot
    from numpy.linalg import norm
    from scipy.optimize import minimize
    
    W_strip = []
    trend_strip = []
    for hour in range(len(W)):
        if not isnan(trend[hour]):
            W_strip.append(W[hour])
            trend_strip.append(trend[hour])
    W_strip = array(W_strip)
    trend_strip = array(trend_strip)

    func = lambda x: norm(dot(W_strip,array(x).reshape(RANK,1)).T - trend_strip)
    result = minimize(func, [1. for i in range(RANK)],
                      method = 'L-BFGS-B',
                      bounds = [(0,None) for i in range(RANK)])
    return result.x, func(result.x)/norm(trend_strip)*100.


def Phase2(link_id_list, trips=TRIPS):
    from numpy import array, nan, loadtxt, isnan
    from csv import reader as csvreader
    W = loadtxt(filenames['W_trips'])    # W = 8760 x 50
    print 'W read', W.shape
    HT = []
    link_id_list = sorted(link_id_list)
    reader = csvreader(open(filenames['data_trips_transpose'], 'rb'))
    link_id_old = 0
    for link_id in link_id_list:
        for skip in range(link_id_old,link_id):
            trend = reader.next()
        link_id_old = link_id
        trend = [float(entry) if bool(entry) else nan for entry in trend]
        if sum(~isnan(trend)) == 0:
            continue
        # trend should have length 8760 with NaNs
        red_dots, = plot(range(1,49),trend[0+24*24:48+24*24],'ro')
        coeffs, error = find_decomposition(trend, W)        
        print link_id,'\t', error
	with open('./Phase2_results.txt','ab') as writefile:
	    writefile.write(str(link_id)+'\t'+str(error)+'\n')
        HT.append(coeffs)
    return array(HT).T, red_dots # This is H for link_id_list

#from Read_data import find_Phase2_links

from numpy import loadtxt, savetxt, dot, nan
from matplotlib.pyplot import plot, show, legend, xlabel, ylabel, grid
from matplotlib.lines import Line2D
from Read_data import read_full_link_json
from csv import reader
#link_id_list = map(int, loadtxt(filenames['full_link_ids'], delimiter=',', ndmin=1))
#link_id_list = (link_id_list[0],)
#print link_id_list
link_id_list = (3975,)
coeffs, red_dots = Phase2(link_id_list)
W = loadtxt(filenames['W_trips'])
blue_line, = plot(range(1,49),dot(W,coeffs)[0+24*24:48+24*24],'-')
#plot(range(1,51),coeffs)
H = loadtxt(filenames['H_trips'])
#plot(dot(W,H[:,0].T).T[0:48])
#plot(range(1,51),H[:,0])
#red_dots = Line2D([],[],color='red', marker='o', label='Real data')
#blue_line = Line2D([],[],color='blue', marker='', label='Phase 2 Estimation')
legend([blue_line, red_dots],['Phase 2 Estimation','Real Data'])
xlabel('Time (in hours)')
ylabel('Number of Taxis')
grid(True)
show()
#fli, V = read_full_link_json()











