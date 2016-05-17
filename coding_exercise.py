#!/usr/bin/env python3 -Wall
import logging
import sys
import pprint
import argparse
from collections import defaultdict

#setup logging -- send to stdout for testing; later move to logfile
log = logging.getLogger('coding_exercise_logger')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

#example graph representation (with adjacency lists)
#i.e. place key, value with place type, and ordered places with weights 
#graph = { 0 : { "type": 0, "adj": [0, 7, 10]},
#          1 : { "type": 0, "adj": [7, 0, 5]},
#          2 : { "type": 0, "adj": [10, 5, 0]},
#        }  

graph = {}

#example historical_routes representation
#i.e. route key and route frequency value
#historical_routes = { '0 1 2':	1,
#                      '2 1 0': 1,  
#                      '2 1': 1,  
#                      '0 2': 1,  
#                      '0 2 1': 1,  
#                    }

historical_routes = defaultdict(int)

#example most_popular representation - total historic count for each place
#i.e. element zero = place zero total, element one = place one total, etc.
#place_totals = [4, 4, 5]

place_totals = []

#example current_route representation
#current_route = [1, 2]

current_route = []


def read_file(filename):
    """ consumes contents of filename, with a big assumption that it can fit into memory """
    try:
        with open(filename, 'rt') as f:
            data = f.read().splitlines()
            return data
    except OSError as e:
        log.fatal("Unable to load the input data from file; please check! Details: " + str(e))
        sys.exit(1)       		

def parse_file_and_build_representations(file_data):
    """ builds out data structures for places and routes based on 'file_data' """
    PLACE_COUNT_HEADER_OFFSET = 0
    PLACE_DATA_BEGIN_OFFSET = 1
    NUM_OF_PLACES = int(file_data[PLACE_COUNT_HEADER_OFFSET])
    ROUTE_COUNT_HEADER_OFFSET = NUM_OF_PLACES + 1
    NUM_OF_HISTORIC_ROUTES = int(file_data[ROUTE_COUNT_HEADER_OFFSET])
    ROUTE_DATA_OFFSET = ROUTE_COUNT_HEADER_OFFSET + 1
    CURRENT_ROUTE_HEADER_OFFSET = NUM_OF_PLACES + NUM_OF_HISTORIC_ROUTES + 2
    CURRENT_ROUTE = file_data[CURRENT_ROUTE_HEADER_OFFSET]

    log.debug("Header: Number of Places: " + str(NUM_OF_PLACES))

    for place in file_data[PLACE_DATA_BEGIN_OFFSET:ROUTE_COUNT_HEADER_OFFSET]:
        values = place.split()
        graph[values[0]] = { "type": values[1], "adj": values[2:]} 
        place_totals.append(0)

    log.debug("Header: Number of Historic Routes: " + str(NUM_OF_HISTORIC_ROUTES))

    for route in file_data[ROUTE_DATA_OFFSET:CURRENT_ROUTE_HEADER_OFFSET]:
        historical_routes[route] += 1
        places = route.split()
        for place in places:
            place_totals[int(place)] += 1

    log.debug("Current route: " + CURRENT_ROUTE)
    
    current_route.extend([int(x) for x in CURRENT_ROUTE.split()])

def suggest_most_popular_places(number_of_places=5):
    """ recommend places, based on most popular places from previous routes """
    # find current location
    current_location = current_route.pop()
    # get full list of recommendations, remove current location, after all, we are already there!
    top_recs = sorted(((value, index) for index, value in enumerate(place_totals)), reverse=True)
    top_recs = [x[1] for x in top_recs]
    top_recs.remove(current_location)
    # slice the recommendation to just return the number requested, or as close to as possible..
    print(" ".join(str(x) for x in top_recs[:number_of_places]))

def dump_representations():
    """ debug utility: pretty output the data models for the places, routes, etc. """
    pprint.pprint(graph)
    pprint.pprint(historical_routes)
    pprint.pprint(place_totals)
    pprint.pprint(current_route)

if __name__ == "__main__":
    log.info("welcome!")
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the input file with place and route data")
    args = parser.parse_args()
    raw = read_file(args.file)
    parse_file_and_build_representations(raw)
    suggest_most_popular_places(5)
    log.info("goodbye!")

