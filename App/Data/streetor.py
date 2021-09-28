from pandas import DataFrame, concat
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import streamlit as st


class StreetorModel:

    def __init__(self, data) -> None:

        if data is None:
            st.error('Failed to load the dataset')
            self.error = True
            return
        else:
            self.error = False
            self.data = DataFrame(data)
            if 'MONTH' in self.data.columns:
                self.data['MONTH'] = self.data['MONTH'].replace({
                    'JANUARY': 1,
                    'FEBRUARY': 2,
                    'MARCH': 3,
                    'APRIL': 4,
                    'MAY': 5,
                    'JUNE': 6,
                    'JULY': 7,
                    'AUGUST': 8,
                    'SEPTEMBER': 9,
                    'OCTOBER': 10,
                    'NOVEMBER': 11,
                    'DECEMBER': 12
                })

        self.n_clusters = None

        self.data_predict = None
        self.data_test = None
        self.data_train = None

        self.k = None

        self.diff = 3

        self.mae = None
        self.mse = None
        self.rmse = None
        self.r2 = None

        self.lat = None
        self.lon = None
        self.t_lat = None
        self.t_lon = None

        self.res_lat = None
        self.res_lon = None
        self.sum_lat = None
        self.sum_lon = None

        self.med_lat = None
        self.med_lon = None

        self.acc = None

        self.total = None
        self.dataset = None

        self.period = None
        self.week = None

        self.km = None

    def filter(self, field, value) -> None:

        if value is not None:
            self.data = self.data[self.data[field] == value]

    def run(self, k=1, clusters=100, acc=1.5) -> None:

        if k <= 0:
            self.k = 1
        else:
            self.k = k

        if (clusters <= 0) | (clusters >= len(self.data)):
            self.n_clusters = int(len(self.data) / 3)
        else:
            self.n_clusters = clusters
        # print('CLUSTERS:', self.n_clusters)
        kmeans = KMeans(self.n_clusters)
        self.data['cluster'] = kmeans.fit_predict(self.data[['LATITUDE', 'LONGITUDE']])
        # print(self.data)
        train = self.data[:]

        self.data_predict = DataFrame()
        self.data_test = DataFrame()
        self.data_train = DataFrame()

        for i in range(self.n_clusters):
            knn = KNeighborsRegressor(n_neighbors=k)
            df = train[train['cluster'] == i]
            # print('len(df): ', len(df), 'self.diff: ', self.diff)
            if len(df) > self.diff:
                total = len(df)
                half = int(total - (total / 2))

                t_train = df[:half].sort_values(by='LONGITUDE')
                t_test = df[half:]

                x_train = t_train.drop(columns=['LATITUDE', 'LONGITUDE'])
                y_train = t_train[['LATITUDE', 'LONGITUDE']]

                knn.fit(x_train, y_train)

                predict = knn.predict(t_test.drop(columns=['LATITUDE', 'LONGITUDE']))

                df_temp = DataFrame(predict)
                df_temp = df_temp.rename(columns={0: 'LATITUDE', 1: 'LONGITUDE'})

                self.data_predict = concat([self.data_predict, df_temp])
                self.data_test = concat([self.data_test, t_test[['LATITUDE', 'LONGITUDE']]])
                self.data_train = concat([self.data_train, t_train[['LATITUDE', 'LONGITUDE']]])

        self.mae = round(mean_absolute_error(
            self.data_test[['LATITUDE', 'LONGITUDE']],
            self.data_predict[['LATITUDE', 'LONGITUDE']]
        ), 8)

        self.mse = round(mean_squared_error(
            self.data_test[['LATITUDE', 'LONGITUDE']],
            self.data_predict[['LATITUDE', 'LONGITUDE']],
            squared=False
        ), 8)

        self.rmse = round(mean_squared_error(
            self.data_test[['LATITUDE', 'LONGITUDE']],
            self.data_predict[['LATITUDE', 'LONGITUDE']]
        ), 8)

        self.r2 = round(r2_score(
            self.data_test[['LATITUDE', 'LONGITUDE']],
            self.data_predict[['LATITUDE', 'LONGITUDE']]
        ) * 100, 2)

        test = self.data_test.values.tolist()
        pred = self.data_predict.values.tolist()

        self.lat = []
        self.lon = []
        self.t_lat = []
        self.t_lon = []

        for i in range(len(test)):

            x = test[i][0] - pred[i][0]
            y = test[i][1] - pred[i][1]

            self.t_lat.append(x)
            self.t_lon.append(y)

            self.lat.append(abs(x))
            self.lon.append(abs(y))

        self.med_lat = round(sum(self.lat) / len(self.lat), 8)
        self.med_lon = round(sum(self.lon) / len(self.lon), 8)

        t = self.data_test.reset_index()
        self.res_lat = DataFrame(data=self.t_lat, columns=['RESIDUAL'])
        self.res_lat['LATITUDE'] = t['LATITUDE']
        self.res_lon = DataFrame(data=self.t_lon, columns=['RESIDUAL'])
        self.res_lon['LONGITUDE'] = t['LONGITUDE']

        self.sum_lat = round(sum(self.res_lat['RESIDUAL']), 8)
        self.sum_lon = round(sum(self.res_lon['RESIDUAL']), 8)

        self.km = acc

        _acc = []
        km = acc / 100
        for i in range(len(test)):
            v = (self.lat[i] + self.lon[i]) / 2
            # print(v, km, v <= km)
            if v <= km:
                res = 1
            else:
                res = 0
            _acc.append(res)

        self.data_predict['CHECK'] = _acc
        self.acc = round(len(self.data_predict[self.data_predict['CHECK'] == 1]) * 100 / len(self.data_predict), 2)
        self.data_predict['TARGET'] = 'PREDICT'
        self.data_test['TARGET'] = 'REAL'
        self.data_train['TARGET'] = 'REAL'
        self.total = len(self.data_test) + len(self.data_train)
        self.dataset = concat([self.data_predict, self.data_test])
        self.dataset['WEEK'] = self.week
        self.dataset['PERIOD'] = self.period

    def response(self) -> tuple:
        return self.dataset, {
            'MAE': self.mae,
            'MSE': self.mse,
            'RMSE': self.rmse,
            'R2': self.r2,
            'MED_LAT': self.med_lat,
            'MED_LON': self.med_lon,
            'SUM_LAT': self.sum_lat,
            'SUM_LON': self.sum_lon,
            'ACC': self.acc,
            'TOTAL': self.total,
            'KNN': self.k,
            'CLUSTERS': self.n_clusters,
            'PERIOD': self.period,
            'WEEK': self.week,
            'KM': self.km,
            'RES_LON': self.res_lon,
            'RES_LAT': self.res_lat
        }
