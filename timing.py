import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import tqdm

from voronoi import Voronoi
from utils import Point


def main():
    seed = 10
    num_iterations = 15
    num_sites = [10, 50, 100, 200, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000]

    average_times = []
    np.random.seed(seed)

    for i in range(num_iterations):
        times = []
        for num in tqdm(num_sites):
            points = np.random.random(size=(num, 2)) * 1000
            sites = []
            for site in points:
                sites.append(Point(site[0], site[1]))
            start = time.perf_counter()
            v = Voronoi(sites)
            v.compute()
            total_time = time.perf_counter() - start
            times.append(total_time)
            # print(f"Voronoi diagram of size {num} computed in {total_time:.3f} seconds")
        print(f"Finished round {i}")
        average_times.append(times)
    average_times = np.mean(average_times, axis=0)

    plt.plot(num_sites, average_times, 'r')

    x = np.linspace(1, num_sites[-1], 100)

    # the function, which is y = x^2 here
    y = 0.00008 * x * np.log(x)
    plt.plot(x, y, 'b')
    plt.xlabel("Number of sites")
    plt.ylabel("Time (s)")
    plt.legend(["Runtime", "n * log(n)"])
    plt.show()


if __name__ == '__main__':
    main()
