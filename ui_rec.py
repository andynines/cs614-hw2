from joke import jokes, request_rating

import numpy as np

import pickle

if __name__ == "__main__":
    with open("model.dat", 'rb') as modelf:
        model = pickle.load(modelf)
    preds = list(enumerate(model.predict(73420, np.arange(100))))
    preds.sort(key=lambda p: -p[1])
    result_ratings = []
    for pred_ind, _ in preds:
        print(jokes[pred_ind])
        result_ratings.append(request_rating())
