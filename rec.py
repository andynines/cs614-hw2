from rating import ratings

import numpy as np
from scipy import sparse
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

TRAIN_PORTION = 0.66

np.random.seed(0)
n_items = ratings.shape[1]
inds = np.arange(n_items)
np.random.shuffle(inds)
split_ind = round(n_items * TRAIN_PORTION)
train_inds, test_inds = inds[:split_ind], inds[split_ind:]
interactions_train = ratings.copy()
interactions_train[:, test_inds] = 0
interactions_train = sparse.coo_matrix(interactions_train)
interactions_test = ratings.copy()
interactions_test[:, train_inds] = 0
interactions_test = sparse.coo_matrix(interactions_test)

model = LightFM(loss='warp')
model.fit(interactions_train, epochs=1, num_threads=1)

print("Train precision: %.2f" % precision_at_k(model, interactions_train, k=5).mean())
print("Test precision: %.2f" % precision_at_k(model, interactions_test, k=5).mean())

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
