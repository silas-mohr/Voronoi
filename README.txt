Before running this program, make sure you have the required packages installed.
- numpy
- matplotlib

To run the program, use the command 'python -m main [random seed] [number of points]'.

The random seed just allows for controlled random generation of points, so you can repeat the same points everytime if
needed, or completely randomize them at will. The number of points controls how many sites of the voronoi diagram there
will be.

For example, you could run the program with a random seed of 10 and 40 points with 'python -m main 10 40'

The algorithm is implemented within the Voronoi class in voronoi.py. To use it, create a new Voronoi(sites) object by
creating an array of Points, the sites, and calling the Voronoi.compute() method. Examples of this can be seen in
main.py and timing.py.