from numpy import loadtxt, mean, array, correlate, append, savetxt, nonzero
from matplotlib.pyplot import plot, show, savefig, close, figure
from numpy.linalg  import norm
from Read_data import csv_to_dict, link_id_info

# Loads Seeded files
W = loadtxt('./Data_Files/Seeded_0,1/W_trips.txt')
H = loadtxt('./Data_Files/Seeded_0,1/HT_trips.txt').T
Ha = loadtxt('./Data_Files/Seeded_0,1/HT_trips_axed.txt').T

'''
for sig in range(1,51):
    col = sig-1 # Column number of W

    W_daily = W[:, col].reshape(365,24) # Signature reshaped so each row is a day

    day = 0
    # Day 0  is a Saturday for 2011

    fig = figure()
    #traffic = [plot(W_daily[i:i+7].flatten(), 'g-', linewidth=0.5) for i in range(day,365,7)]
    saturday = mean(array([W_daily[i] for i in range(day,365,7)]), axis=0)
    plot(saturday.flatten(), 'b-')
    sunday = mean(array([W_daily[i] for i in range(day+1,365,7)]), axis=0)
    plot(range(0, 24), sunday.flatten(), 'g-')
    weekday = mean(array([mean(W_daily[i:i+4], axis=0) for i in range(day+2,365,7)]), axis=0)
    plot(range(23, 23+24), weekday.flatten(), 'r-')
    friday = mean(array([W_daily[i] for i in range(day+5,365,7)]), axis=0)
    plot(range(23, 23+24), friday.flatten(), 'k-')
    
    
    fig.set_size_inches(14,8.5)
    #fig.set_dpi(300)
    [plot([23+24*i, 23+24*i],[0, 0.035], 'k--') for i in range(1)]
    savefig('./Data_Files/Seeded_0,1/Graphs/Weekend_Weekday/sig%02d.png'\
            %(sig), bbox_inches='tight', )
    close()

    #for i in range(day,365,7):
    #    if norm(W_daily[i]-avg)/norm(avg)>0.5:
    #        plot(W_daily[i], '-', linewidth=1.5)
    #        print sig, i


    #show()


def autocorr(x):
    result = correlate(x, x, mode='full')
    return result[result.size/2:]


#plot([autocorr(W[:,i])[7*24] for i in range(50)], 'o')
#show()
'''


full_link_ids = loadtxt('./Data_Files/full_link_ids.txt', dtype='int')
print 'full_link_ids were read.'

rows, cols = nonzero(Ha)
print rows
links_of_interest = [[] for i in range(50)]

for i in range(len(rows)):
    sig = rows[i]+1
    link = cols[i]+1
    info = link_id_info(csv_to_dict('links'), full_link_ids[link-1])
    links_of_interest[sig-1].append(map(float,[info['startY'],\
                                               info['startX'],\
                                               info['endY'], info['endX']]))
    print sig, link

for sig in range(50):
    savetxt('./Data_Files/Seeded_0,1/Graphs/Maps/sig%d_links.txt' %sig,
                links_of_interest[sig-1], fmt='%f')

'''
import folium
map_osm = folium.Map(location=[40.753957, -73.987672], zoom_start=13)
segments = folium.PolyLine(locations=links_of_interest, weight=8, color='#1410ed')
map_osm.add_child(segments)
map_osm.save('map_sig3.html')
'''



























