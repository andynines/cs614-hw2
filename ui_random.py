from joke import jokes, request_rating

import random

if __name__ == "__main__":
    user_ratings = {}
    for _ in range(10):
        rand_joke_ind = random.randint(0, len(jokes) - 1)
        print(jokes[rand_joke_ind])
        user_ratings[rand_joke_ind] = request_rating()
    with open("user-ratings.dat", 'w') as ratef:
        ratef.write(str(user_ratings))
