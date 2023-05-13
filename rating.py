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
    # Insert test user preferences
    with open("toni-ratings.dat", 'r') as ratef:
        user_ratings = eval(ratef.read())
    user_vector = [0] * 100
    for ind, rating in user_ratings.items():
        user_vector[ind] = rating
    ratings = ratings[:, 1:]
    ratings = np.concatenate((ratings, [user_vector]), axis=0)
    unrated_inds = (ratings == 99)
    ratings[unrated_inds] = np.nan
    ratings *= 9
    ratings += 110
    ratings /= 20
    ratings[unrated_inds] = 0
    np.savetxt("ratings.csv", ratings, delimiter=',')

if __name__ == "__main__":
    print("First row:")
    print(ratings[0])
    print("Shape:")
    print(ratings.shape)
