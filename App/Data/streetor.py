from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class StreetorModel:

    def __init__(self) -> None:
        print('')
