''' * This file defines addresses to all data files, input files and output files.
    * It also lists all the Global variables used in Non-Negative Matrix Factorization.
    * In case any of the Factorization paramaters need to be changed, they should be changed in this file instead of locally within each program.'''


def generate_filenames(path, path_for_data=None):
    if path_for_data is None:
        path_for_data = path
    filenames = {# Raw data files
                 'links':                path + 'links.csv',
                 'nodes':                path + 'nodes.csv',
                 'raw_data':             path_for_data + 'travel_times_2011.csv',
                 'data_coo_form':        path_for_data + 'data_coo_form.txt',
                 'data_trips':           path_for_data + 'data_trips.csv',
                 'data_traveltimes':     path_for_data + 'data_travel_times.csv',
                 'data_trips_transpose': path_for_data + 'data_trips_transpose.csv',
    
                 # Inputs and Outputs of Read_data.py
                 'full_link_ids':         path + 'full_link_ids.txt',
                 'empty_link_ids':        path + 'empty_link_ids.txt',
                 'full_link_trips':       path + 'full_link_trips.json',
                 'full_link_traveltimes': path + 'full_link_travel_times.json',
                 'full_link_speeds':      path + 'full_link_speeds.json',

                 # Inputs and Outputs of Phase1.py
                 'random':             path + 'Random_numbers.txt',
                 'W_trips':            path + 'W_trips.txt',
                 'W_speeds':           path + 'W_speeds.txt',
                 'W_trips_seed':       path + 'Seeded0,1/W_trips.txt',
                 'W_speeds_seed':      path + 'Seeded0,1/W_speeds.txt',
                 'HT_trips':           path + 'HT_trips.txt',
                 'HT_speeds':          path + 'HT_speeds.txt',
                 'HT_trips_seed':      path + 'Seeded0,1/HT_trips.txt',
                 'HT_speeds_seed':     path + 'Seeded0,1/HT_speeds.txt',
                 'HT_trips_axed':      path + 'HT_trips_axed.txt',
                 'HT_speeds_axed':     path + 'HT_speeds_axed.txt',
                 'HT_trips_axed_seed': path + 'Seeded0,1/HT_trips_axed.txt',
                 'W_speeds_axed_seed': path + 'Seeded0,1/HT_speeds_axed.txt'}
    return filenames


'''Global variables'''

RANK = 50            # Rank for Matrix Factorization in Phase1.py
TRIPS = 1            # Boolean variable: 0 reads travel_speeds data, 1 reads number_of_trips data. 
HOURS_IN_YEAR = 8760 # 24*365
SEEDED = 1           # Boolean variable: 1 or 0 means Phase1.py is seeded or not respectively.

TOTAL_LINKS = 260855 # Total Links aka Road-segments in NYC.
FULL_LINKS = 2302    # Links with less than 720 hours worth of missing data in a year.
EMPTY_LINKS = 234892 # Links with less that 720 hours worth of data in a year.
MID_LINKS = 23661  # TOTAL_LINKS - FULL_LINKS - EMPTY_LINKS
assert MID_LINKS == TOTAL_LINKS - FULL_LINKS - EMPTY_LINKS