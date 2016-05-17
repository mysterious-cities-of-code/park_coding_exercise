Park Technology Coding Exercise Discussion
==========================================

The text below reviews the implementation provided, explaining the decisions made for this short piece of code, and discusses what might be done differently in production code.



Single file, simple functions based implementation - in production code however, we would make use of separate file, classes, packages etc.

Logging - an early nod to production code, we use logging, although currently set to chuck log excerpts to STDOUT, whereas in production code we would have  a nicer place to direct it to.

Data ingest - in this example, we make the assumption data is provided in a single file, and that we can slurp it into memory in one go. In production code we would provide a range of ingest mechanisms, and handle very large files cases (stream and process).

Parsing of data and data structure population - a simplistic parse of the file based on the spec provided, making use of known file positions, and calculated offsets. Would need to adapt this for production code to handle streaming parsers.



Data structures - 

1. Uses a simple structure (graph) to map the places, their type and their adjacency lists. In production code we may wish to make use of an adjacency matrix instead of lists to aid analysis. We would probably also lean on better suited libs than hand-rolling this (numpy/scipy etc.)

2. Uses a simple structure (historical_routes) to maintain a tally of the routes as processed from the file. In production code we may also wish to maintain most recent or other ordering, and we would probably also want to store the original data in a lossless repository somewhere. 

3. Uses a simple structure (place_totals) to maintain a count of each place as encountered amongst the various routes. A simple “is this specific place popular?” list, irrespective of the arc weights etc. 

4. Uses a simple structure (current_route) to model the current route as provided.



Recommendation strategy - a single noddy strategy is provided (suggest_most_popular_places) - which takes a parameter for the number of suggestions to return, and looks at the most popular places based solely on ‘place_total’ (which places occur most frequently in past routes). In production code, we might want to apply algorithms like ‘Floyd–Warshall’ and related, with a range of different strategies that consider arc weight, place type, place popularity, and the various combinations of those.


Testing - obviously production code would have a fuller more comprehensive test suite.

