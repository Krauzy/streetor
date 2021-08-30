from pandas.core.frame import DataFrame
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.data.dataReader import get_dataset
import pandas as pd
import src.util.adaptalize as adapt # put_filter_data, get_filter_data, get_weekday_revert

class Analysis:

    def __init__(self, 
        data, 
        n_clusters=100, 
        k=1, 
        drop=['Road', 'City'], 
        acc=1.5, 
        hour='Geral', 
        day='Geral') -> None:

        if data is None:
            self.__data = get_dataset()
        elif type(data) == str:
            self.__data = get_dataset(data)
        else:
            self.__data = pd.DataFrame(data)     
        
        self.__data = self.__data.drop(columns=drop)

        if day != 'Geral':
            self.__day = adapt.get_weekday_revert(day)
        else:
            self.__day = day

        if hour != 'Geral':
            h = int((str(hour)[:2]))
            if h >= 0 and h < 6:
                self.__turn = 'Dawn'
            elif h >= 6 and h < 12:
                self.__turn = 'Morning'
            elif h >= 12 and h < 18:
                self.__turn = 'Afternoon'
            else:
                self.__turn = 'Night'
        else:
            self.__turn = hour

        if n_clusters == 0:
            self.__clusters = self.get_best_clusters()
        else:
            self.__clusters = n_clusters
        
        self.__k = k
        self.__acc = acc

    def get_best_clusters(self) -> int:
        return 100

    def filter(self) -> None:
        if self.__day != 'Geral':
            self.__data = self.__data[self.__data['Day of Week'] == self.__day]
        if self.__turn != 'Geral':
            self.__data = self.__data[self.__data['Period'] == self.__turn]
        self.__data = adapt.put_filter_data(self.__data)

    def run(self) -> None:
        
        self.filter()

        if self.__clusters >= len(self.__data):
            self.__clusters = int(len(self.__data) / 3)
        # Agrupar os clusters
        kmeans = KMeans(self.__clusters)        
        self.__data['cluster'] = kmeans.fit_predict(self.__data[['Latitude', 'Longitude']])
        
        # Excutar a regressão com KNN
        train = self.__data[:]
        self.__df = pd.DataFrame()
        self.__tf = pd.DataFrame()
        self.__tr = pd.DataFrame()
        for i in range(self.__clusters):
            knn = KNeighborsRegressor(n_neighbors=self.__k)
            df = train[train['cluster'] == i]
            # df = df.sort_values(by='Longitude')
            if len(df) > 2:
                total = len(df)
                frac = total - int(total / 2)
                t_train = df[:frac]
                t_train = t_train.sort_values(by='Longitude')
                t_test = df[frac:]
                X_train = t_train.drop(columns=['Latitude', 'Longitude'])
                y_train = t_train[['Latitude', 'Longitude']]
                knn.fit(X_train, y_train)
                predict = knn.predict(t_test.drop(columns=['Latitude', 'Longitude']))
                df_temp = pd.DataFrame(predict)
                df_temp = df_temp.rename(columns={0:'Latitude', 1:'Longitude'})
                self.__df = pd.concat([self.__df, df_temp])
                self.__tf = pd.concat([self.__tf, t_test[['Latitude', 'Longitude']]])
                self.__tr = pd.concat([self.__tr, t_train[['Latitude', 'Longitude']]])
                
        # print(len(self.__df))
        self.__mae = round(mean_absolute_error(self.__tf[['Latitude', 'Longitude']], self.__df[['Latitude', 'Longitude']]), 8)
        self.__mse = round(mean_squared_error(self.__tf[['Latitude', 'Longitude']], self.__df[['Latitude', 'Longitude']]), 8)
        self.__rmse = round(mean_squared_error(self.__tf[['Latitude', 'Longitude']], self.__df[['Latitude', 'Longitude']], squared=False), 8)
        self.__r2 = round(r2_score(self.__tf[['Latitude', 'Longitude']], self.__df[['Latitude', 'Longitude']]) * 100, 2)

        self.get_residual()
    
    def get_residual(self):
        test = self.__tf.values.tolist()
        pred = self.__df.values.tolist()
        self.__lat = []
        self.__lon = []
        self.__t_lat = []
        self.__t_lon = []
        
        for i in range(len(test)):
            x = test[i][0] - pred[i][0]
            y = test[i][1] - pred[i][1]
            self.__t_lat.append(x)
            self.__t_lon.append(y)
            self.__lat.append(abs(x))
            self.__lon.append(abs(y))
        self.__med_lat = round(sum(self.__lat) / len(self.__lat), 4)
        self.__med_lon = round(sum(self.__lon) / len(self.__lon), 4)

        self.__test = test

        t = self.__tf.reset_index()
        self.__res_lat = pd.DataFrame(data=self.__t_lat, columns=['Residual'])
        self.__res_lat['Latitude'] = t['Latitude']
        self.__res_lon = pd.DataFrame(data=self.__t_lon, columns=['Residual'])
        self.__res_lon['Longitude'] = t['Longitude']

        self.__sum_lon = round(sum(self.__res_lon['Residual']), 4)
        self.__sum_lat = round(sum(self.__res_lat['Residual']), 4)
        
    def plot(self):
        acc = []
        km = self.__acc / 100
        # print('km: ', km)
        for i in range(len(self.__test)):
            v = (self.__lat[i] + self.__lon[i]) / 2
            # print('var: ', v)
            if v <= km:
                res = 1
            else:
                res = 0
            acc.append(res)
        self.__df['check'] = acc
        self.__accuracy = round(len(self.__df[self.__df['check'] == 1]) * 100 / len(self.__df), 2)
        self.__df['Target'] = 'predict'
        self.__tf['Target'] = 'real'
        self.__tr['Target'] = 'real'
        self.__reg = len(self.__tf) + len(self.__tr)
        self.__dataset = pd.concat([self.__df, self.__tf])
    
    def get_attribute(self):
        dic = {
            'MAE': self.__mae,
            'MSE': self.__mse,
            'RMSE': self.__rmse,
            'R2': self.__r2,
            'M_LATITUDE': self.__med_lat,
            'M_LONGITUDE': self.__med_lon,
            'S_LATITUDE': self.__sum_lat,
            'S_LONGITUDE': self.__sum_lon,
            'ACC': self.__accuracy,
            'TOTAL': self.__reg
        }
        return self.__dataset, dic