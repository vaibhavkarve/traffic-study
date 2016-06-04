OVERVIEW:
This folder contains traffic estimates for individual links of the NYC road network for the years 2010-2013.  An estimate is given for every hour of the dataset  The traffic estimates are obtained from taxi trips, which can be downloaded at https://uofi.box.com/NYCtaxidata, using an algorithm very similar to the one described in the Supporting Information of this paper: http://www.pnas.org/content/111/37/13290.full .  The actual code that we used to perform this analysis is located at https://github.com/Lab-Work/taxisim .  For technical questions, feel free to contact bpdonov2@illinois.edu.


INSTRUCTIONS:
First, extract the four zip files travel_times_2010.zip, travel_times_2011.zip, travel_times_2012.zip, travel_times_2013.zip .  This should produce the files travel_times_2010.csv, travel_times_2011.csv, travel_times_2012.csv, travel_times_2013.csv , which should total approximately 20GB.


ROAD NETWORK GRAPH DATA FORMAT:
This folder includes the traffic estimates, and the corresponding road network graph, so the traffic estimates can be interpretted and understood.  The files nodes.csv and links.csv contain the road network, and the larger files contain the traffic estimates.  The road network is represented as a directed graph, where the Nodes and Links have additional properties.  The simplest way to use this graph is with the Python class /routing/Map.py from our source code at https://github.com/Lab-Work/taxisim .  The map itself was downloaded from OpenStreetMap and processed using the AwesomeStitch (https://github.com/Lab-Work/AwesomeStitch) library.

If you don't want to use our software, the data format is fairly straightforward.  Each row in the nodes.csv file corresponds to one node, which is an intersection in the road network graph.  The following properties are important:
node_id - a unique identifier for each node
xcoord - the longitude of that node
ycoord - the latitude of that node

Each row in the links.csv file corresponds to one link, which is a small road segment that connects two nodes.  In general, a street consists of many Links, end to end.  Two-way streets are represented as two links going in opposite directions.  Note that this implies that both directions can have different traffic estimates.  The following link properties are important:
link_id - a unique identifier for each link
begin_node_id - refers to the first node that this link attaches to
end_node_id - refers to the second node that this link attaches to.  The link direction is begin_node_id --> end_node_id
begin_angle - Angle of the link, viewed from the begin_node.  An angle of 0 is a link pointing due north, and it increases CCW.
end_angle - Angle of the link, viewed from the end_node.  An angle of 180 is a link pointing due north and it increases CCW.  If the link is perfectly straight, then the begin and end angles should differ by exactly 180 degrees.  But if it is curved, they will be slightly different.
street_length - length of the Link in meters
osm_name - the name of the street
osm_class - the type of street (highway, residential, etc...)
startX, startY, endX, endY - same as the xcoord and ycoords of the begin_node and end_node


TRAFFIC ESTIMATE DATA FORMAT:
Again, the easiest way to use these traffic estimates is with our sourcecode at (https://github.com/Lab-Work/taxisim).  In order to do this, the four large CSV files should be dumped into a single table in a PostGreSQL database.  Then, the function taxisim/db_functions/db_travel_times.py/load_travel_times() can be used to load the traffic estimates from the DB and assign them to the appropriate links of the graph.  See the documentation of the taxisim library for more information about how to do this.

If you do not wish to use our software, the data format is described here.  Each row of the CSV files (travel_times_2010.csv, travel_times_2011.csv, travel_times_2012.csv, travel_times_2013.csv) represents the traffic conditions of a particular link of the road network during a particular hour, since the traffic conditions change over time.  The columns are described as follows:

begin_node_id - The begin_node_id of the relevant link
end_node_id - the end_node_id of the relevant link.  (Note that the ordered pair begin_node_id, end_node_id is enough to uniquely identify a link, since only one link may connect the same two nodes in one direction).
datetime - The hour in which the given traffic estimate occurs.  Since we are using one hour intervals, this date represents the beginning of that hour.
travel_time - the estimated amount of time for a vehicle to travel over this link.
num_trips - the estimated number of taxis that drove over this link during the hour.  Links with more trips are more likely to contain accurate estimates.  Note that a lot of links had 0 trips during certain hours.  These rows are not included, in order to save space.

Take the following data as an example:

begin_node_id, end_node_id, datetime,           travel_time, num_trips
42438774,      42444458,   2011-12-31 23:00:00, 10.9921,     11

This is the traffic estimate for a link that connects node 42438774 to node 42444458 (this happens to be link 151961), on December 31, 2011 between 11pm and midnight.  During this hour, 11 taxis drove over that link, and the estimated travel time for each of them is 10.9921 seconds.









