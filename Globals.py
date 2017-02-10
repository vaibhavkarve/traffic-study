filenames_PC = {'links':'./Data_Files/links.csv',
                'nodes':'./Data_Files/nodes.csv',
                'raw_data':'../../travel_times_2011.csv',
                'data_coo_form':'../../data_coo_form.txt',
                'data_trips':'../../data_trips.csv',
                'data_traveltimes':'../../data_travel_times.csv',
                'full_link_ids':'./Data_Files/full_link_ids.txt',
                'empty_link_ids':'./Data_Files/empty_link_ids.txt',
                'full_link_trips':'./Data_Files/full_link_trips.json',
                'full_link_traveltimes':'./Data_Files/full_link_travel_times.json',
                'W_trips':'./Data_Files/W_trips.txt',
                'W_traveltimes':'./Data_Files/W_travel_times.txt',
                'H_trips':'./Data_Files/H_trips.txt',
                'H_traveltimes':'./Data_Files/H_travel_times.txt',
                'random':'./Data_Files/Random_numbers.txt',
                'data_trips_transpose':'../../data_trips_transpose.csv'}


filenames_cluster = {'links':'./scratch/links.csv',
                     'nodes':'./scratch/nodes.csv',
                     'raw_data':'./scratch/travel_times_2011.csv',
                     'data_coo_form':'./scratch/data_coo_form.txt',
                     'data_trips':'./scratch/data_trips.csv',
                     'data_traveltimes':'./scratch/data_travel_times.csv',
                     'full_link_ids':'./scratch/full_link_ids.txt',
                     'empty_link_ids':'./scratch/empty_link_ids.txt',
                     'full_link_trips':'./scratch/full_link_trips.json',
                     'full_link_traveltimes':'./scratch/full_link_travel_times.json',
                     'W_trips':'./scratch/W_trips.txt',
                     'W_traveltimes':'./scratch/W_travel_times.txt',
                     'H_trips':'./scratch/H_trips.txt',
                     'W_traveltimes':'./scratch/H_travel_times.txt',
                     'random':'./scratch/Random_numbers.txt',
                     'data_trips_transpose':'./scratch/data_trips_transpose.csv'}


RANK = 50
TRIPS = 1
TOTAL_LINKS = 260855
FULL_LINKS = 2302
EMPTY_LINKS = 234892
MID_LINKS = TOTAL_LINKS - FULL_LINKS - EMPTY_LINKS #= 23661
HOURS_IN_YEAR = 8760
