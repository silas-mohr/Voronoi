import matplotlib.pyplot as plt
import numpy as np
import sys
import time

from voronoi import Voronoi
from utils import Point


def main():
    if len(sys.argv) < 3:
        print("Please provide a seed and number of points.")
        return
    seed = int(sys.argv[1])
    num_sites = int(sys.argv[2])

    start = time.perf_counter()
    np.random.seed(seed)
    points = np.random.random(size=(num_sites, 2)) * 1000
    sites = []
    for site in points:
        sites.append(Point(site[0], site[1]))
    v = Voronoi(sites)
    v.compute()
    total_time = time.perf_counter() - start
    print(f"Voronoi diagram computed in {total_time:.3f} seconds")
    v_edges = v.get_output()
    for site in sites:
        plt.scatter(site.x, site.y)
    for edge in v_edges:
        plt.plot(edge[::2], edge[1::2], 'k', linestyle='-', marker='')
    plt.xlim(-10, 1010)
    plt.ylim(-10, 1010)
    plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
    plt.show()


if __name__ == "__main__":
    main()
