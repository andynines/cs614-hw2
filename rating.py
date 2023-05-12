import csv
import pathlib

import numpy as np

CACHE_FILE = "./ratings.csv"

if pathlib.Path(CACHE_FILE).exists():
    print("Loading cached ratings")
    ratings = np.genfromtxt(CACHE_FILE, float, delimiter=',')
else:
    print("Generating ratings")
    ratings = np.empty((0, 101))
    for n in range(1, 4):
        with open(f"ratings/jester-data-{n}.csv", 'r') as ratef:
            reader = csv.reader(ratef)
            new_rows = [
                [float(x) for x in row]
                for row in reader]
            ratings = np.concatenate((ratings, new_rows), axis=0)
    ratings = ratings[:, 1:]
    unrated_inds = (ratings == 99)
    ratings[unrated_inds] = np.nan
    ratings -= np.nanmean(ratings, axis=1).reshape(-1, 1)
    ratestd = np.nanstd(ratings, axis=1).reshape(-1, 1)
    ratestd[ratestd == 0] = 1
    ratings /= ratestd
    ratings += 10
    ratings[unrated_inds] = 0
    np.savetxt("ratings.csv", ratings, delimiter=',')

if __name__ == "__main__":
    print("First row:")
    print(ratings[0])
    print("Shape:")
    print(ratings.shape)
