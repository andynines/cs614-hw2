from rating import ratings

from scipy import sparse
from lightfm import LightFM
from lightfm.cross_validation import random_train_test_split
from lightfm.evaluation import precision_at_k

TEST_PERCENT = 0.2

interactions = sparse.coo_matrix(ratings)
train, test = random_train_test_split(interactions, test_percentage=TEST_PERCENT, random_state=0)

model = LightFM(
    loss='warp',
    learning_rate=0.001,
    random_state=0,
    user_alpha=0.01,
    item_alpha=0.01,
)
model.fit(train, epochs=10, num_threads=1, verbose=True)

print("Train precision: %.2f" % precision_at_k(model, train, k=5).mean())
print("Test precision: %.2f" % precision_at_k(model, test, k=5).mean())
