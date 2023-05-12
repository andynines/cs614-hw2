import rating

from surprise import SVD
from surprise.model_selection import cross_validate

algo = SVD()
cross_validate(algo, rating.ratings, measures=['RMSE', 'MAE'], cv=5, verbose=True)
