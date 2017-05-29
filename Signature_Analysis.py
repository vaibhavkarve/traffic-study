from numpy import loadtxt, mean, array, correlate, append
from matplotlib.pyplot import plot, show
from numpy.linalg  import norm
from Read_data import csv_to_dict, link_id_info

W = loadtxt('./Data_Files/Seeded_0,1/W_trips.txt')
H = loadtxt('./Data_Files/Seeded_0,1/HT_trips.txt').T
Ha = loadtxt('./Data_Files/Seeded_0,1/HT_trips_axed.txt').T

sig = 8     # Signature number ## Periodic sigs are 1,2,8,26
#sig_list = [1,2,8,26]
#for sig in sig_list:
col = sig-1 # Column number of W

W_daily = W[:, col].reshape(365,24) # Signature reshaped so each row is a day

day = 1%7
# Day 0  is a Saturday for 2011
traffic = [plot(W_daily[i], 'g-', linewidth=0.5) for i in range(day,365,7)]
avg = mean(array([W_daily[i] for i in range(day,365,7)]), axis=0)
plot(avg, 'r-')
####traffic = [plot(append(W_daily[i],W_daily[i+1]), 'g-', linewidth=0.5) for i in range(day,365,7)]
####avg = mean(array([append(W_daily[i],W_daily[i+1]) for i in range(day,365,7)]), axis=0)
####plot(avg, 'r-')

#for i in range(day,365,7):
#    if norm(W_daily[i]-avg)/norm(avg)>0.5:
#        plot(W_daily[i], '-', linewidth=1.5)
#        print sig, i

plot(W_daily[1], 'b-', linewidth=2)
plot(W_daily[358], 'k-', linewidth=2)
####plot(append(W_daily[327],W_daily[328]), 'b-', linewidth=2)
####plot([23,23], [0,0.037], 'k--')

show()



'''
def autocorr(x):
    result = correlate(x, x, mode='full')
    return result[result.size/2:]


#plot([autocorr(W[:,i])[7*24] for i in range(50)], 'o')
#show()

sig_links = []
for i in range(len(Ha[2])):
    if Ha[2,i] != 0.:
        sig_links.append(i)

full_link_ids = loadtxt('./Data_Files/full_link_ids.txt', dtype='int')

links_of_interest = []
for i in sig_links:
    info = link_id_info(csv_to_dict('links'), full_link_ids[i])
    links_of_interest.append([(float(info['startY']), float(info['startX'])),\
                              (float(info['endY']), float(info['endX']))])
    print i

import folium
map_osm = folium.Map(location=[40.753957, -73.987672], zoom_start=13)
segments = folium.PolyLine(locations=links_of_interest, weight=8, color='#1410ed')
map_osm.add_child(segments)
map_osm.save('map_sig3.html')
'''



























