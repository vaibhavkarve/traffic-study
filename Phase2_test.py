from Globals import filenames_PC as filenames


link_id = 1542

from Read_data import read_full_link_json
full_link_ids, V = read_full_link_json(trips=1)

from Phase1 import read_W
from Read_data import replace_placeholder
from json import load
from numpy import array, dot, nan, isnan, multiply, around, mean
from numpy.linalg import norm, solve, det
from matplotlib.pyplot import plot, show
from scipy.optimize import minimize

W = read_W()
print 'W read'
#trend = V[:,full_link_ids.index(link_id)]
for trend in V[:,1000:1050].T:
    W_strip = array([W[hour] for hour in range(len(W)) if ~isnan(trend[hour])])
    trend = array([trend[hour] for hour in range(len(trend)) if ~isnan(trend[hour])])

    #h = mean([solve(W[i:50+i],trend[i:50+i]) for i in range(0,8700,50)], axis=0)
    func = lambda x: norm(dot(W_strip,x)-trend)
    result = minimize(func, array([0 for i in range(50)]),
                      method = 'L-BFGS-B',
                      bounds = [(0,None) for i in range(50)])
    h = result.x
    print func(h)/norm(trend)*100.
#plot(h)

#show()
