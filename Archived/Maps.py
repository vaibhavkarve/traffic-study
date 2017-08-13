from numpy import loadtxt, mean, array, correlate, append, savetxt, nonzero
from matplotlib.pyplot import plot, show, savefig, close, figure
from numpy.linalg  import norm
from Read_data import csv_to_dict, link_id_info
from Globals import filenames_PC as filenames
import folium

def write_sig_links():
    # Do not run this! Takes too long to run!
    # Loads Seeded files
    W = loadtxt(filenames['W_trips_seed'])
    H = loadtxt(filenames['HT_trips_seed']).T
    Ha = loadtxt(filenames['HT_trips_axed_seed']).T

    full_link_ids = loadtxt(filenames['full_link_ids'], dtype='int')
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

    for sig in range(1,51):
        savetxt('./Data_Files/Seeded_0,1/Maps/sig%d_links.txt' %sig, links_of_interest[sig-1], fmt='%f')

    return None

def make_maps(sig):
    map_osm = folium.Map(location=[40.753957, -73.987672],tiles='Stamen Terrain',\
                         zoom_start=12)
    coords = loadtxt('./Data_Files/Seeded_0,1/Maps/sig%d_links.txt' %sig)
    coords = coords.reshape(len(coords),2,2)
    segments = folium.PolyLine(locations=coords, weight=4, color='#1410ed',\
                               opacity=0.8)
    map_osm.add_child(segments)
    map_osm.save('./Data_Files/Seeded_0,1/Maps/Sig%d.html' %sig)
    return None

'''for sig in range(1,51):
    make_maps(sig)
'''

map_osm = folium.Map(location=[40.753957, -73.987672],tiles='Stamen Terrain',\
                     zoom_start=12)
coords = loadtxt('./Data_Files/Seeded_0,1/Maps/sig%d_links.txt' %sig)
coords = coords.reshape(len(coords),2,2)
segments = folium.PolyLine(locations=coords, weight=4, color='#1410ed',\
                           opacity=0.8)
map_osm.add_child(segments)
map_osm.save('./Data_Files/Seeded_0,1/Maps/Sig%d.html' %sig)
