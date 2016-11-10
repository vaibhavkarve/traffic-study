from Globals import filenames_PC as filenames


# Takes link_id and creates a json with its data, for trips, with NaNs.
'''
def pick_nanlink_data(link_id):
    from csv import reader
    from numpy import nan
    from json import dump
    
    with open(filenames['data_trips'], 'rb') as datafile:
        reader = reader(datafile)
        trend = [line[link_id-1] for line in reader]
        print 'Done reading trend'

    trend = [float(entry) if bool(entry) else nan for entry in trend]
    print 'Converted to float'
    print len(trend)
 
    with open(filenames['nanlink1'], 'wb') as writefile:
        dump(trend, writefile)
        print 'Written to json'
    return None

pick_nanlink_data(1542)
'''
link_id = 1542

from Read_data import read_full_link_json
full_link_ids, V = read_full_link_json(trips=1)

from Phase1 import read_W
from Read_data import replace_placeholder
from json import load
from numpy import array, dot, nan, isnan, multiply, around
from numpy.linalg import norm

W = read_W()
print 'W read'
trend = V[:,full_link_ids.index(link_id)]
#W_strip = multiply(W.T, ~isnan(trend)).T
trend_positions = ~isnan(trend) #return list of Trues/Falses that correspond to data entries /nan entries, respectively
trend = replace_placeholder(trend, value=0.) #replace nans with 0

projections = [dot(sig,trend.T)/norm(multiply(sig,trend_positions))**2*sig for sig in W.T] #list of projections of the trend onto each signature
errors = [norm(trend - multiply(projections[i],trend_positions))/norm(trend)*100 for i in range(len(W.T))] #relative error for each projection
best_sig_index = errors.index(min(errors))
print min(errors)
print best_sig_index

threshold = 25 # percent error in full_link SNMF (relaxed)
trend_approx = projections[best_sig_index] #best projection onto a single signature
print 0 in W.T[best_sig_index] #check whether we have a 0 in our projection (could cause issues later)
if min(errors) > threshold: #check whether are projection/approximation is good enough
    correction_factors = multiply(trend,1./trend_approx)/1.
    c = min([correction_factors[i] for i in range(len(trend_positions)) if trend_positions[i]])
    print c
    if c>0:
        trend = trend - c*trend_approx
        #print norm(trend_old - trend)/norm(trend_old)*100
    else:
        print 'here'
        trend = trend - trend_approx

projections = [dot(sig,trend.T)/norm(multiply(sig,trend_positions))**2*sig for sig in W.T]
errors = [norm(trend - multiply(projections[i],trend_positions))/norm(trend)*100 for i in range(len(W.T))]
best_sig_index = errors.index(min(errors))
print min(errors)
print best_sig_index

threshold = 25 # percent error in full_link SNMF (relaxed)
trend_approx = projections[best_sig_index]
print 0 in W.T[best_sig_index]
if min(errors) > threshold:
    correction_factors = multiply(trend,1./trend_approx)/100.
    c = min([correction_factors[i] for i in range(len(trend_positions)) if trend_positions[i]])
    print c
    if c>0:
        trend = trend - c*trend_approx
        #print norm(trend_old - trend)/norm(trend_old)*100
    else:
        print 'here'
        trend = trend - trend_approx

projections = [dot(sig,trend.T)/norm(multiply(sig,trend_positions))**2*sig for sig in W.T]
errors = [norm(trend - multiply(projections[i],trend_positions))/norm(trend)*100 for i in range(len(W.T))]
best_sig_index = errors.index(min(errors))
print min(errors)
print best_sig_index







