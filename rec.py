from rating import ratings

import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
from lightfm.cross_validation import random_train_test_split
from lightfm.evaluation import precision_at_k

TEST_PERCENT = 0.2

user_ids = np.arange(ratings.shape[0])
joke_ids = np.arange(ratings.shape[1])

dataset = Dataset()
dataset.fit(user_ids, joke_ids)
interactions, _ = dataset.build_interactions(zip(*np.nonzero(ratings), ratings.ravel()))
train, test = random_train_test_split(interactions, test_percentage=TEST_PERCENT, random_state=0)

model = LightFM(loss='warp')
model.fit(train, epochs=1, num_threads=1, verbose=True)

print("Train precision: %.2f" % precision_at_k(model, train, k=5).mean())
print("Test precision: %.2f" % precision_at_k(model, test, k=5).mean())

def sample_recommendation(model, data, user_ids):
    # number of users and movies in training data
    n_users, n_items = data['train'].shape

    # generate recommendations for each user we input
    for user_id in user_ids:

        # movies they already like
        known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]

        # movies our model predicts they will like
        scores = model.predict(user_id, np.arange(n_items))
        # rank them in order of most liked to least
        top_items = data['item_labels'][np.argsort(-scores)]

        # print out the results
        print("User %s" % user_id)
        print("     Known positives:")

        for x in known_positives[:3]:
            print("        %s" % x)

        print("     Recommended:")

        for x in top_items[:3]:
            print("        %s" % x)


#sample_recommendation(model, data, [3, 25, 450])
