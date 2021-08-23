import pandas as pd


class Data:
    EUCLIDEAN = 0
    MANHATTAN = 1
    CHEBYSHEV = 2


    def __init__(self, data=pd.DataFrame()):
        self.data = data
        self.old = data.copy()

    def show(self, size=0):
        if size == 0:
            return self.data
        else:
            return self.data[:size]

    def remove_column(self, columns='', save=False, copy=False):
        if save:
            self.data = self.data.drop(columns)
            return self.data
        else:
            if copy:
                return (self.data.drop(columns)).copy()
            return self.data.drop(columns)

    def change_column(self, column='', to_replace={}, save=False, copy=False):
        if save:
            self.data[column] = self.data[column].replace(to_replace)
        else:
            if copy:
                return (self.data[column].replace(to_replace)).copy()
            else:
                return self.data[column].replace(to_replace)

    def remove_row(self, index=[], save=False, copy=False):
        if save:
            self.data = self.data.drop(index=index)
        else:
            if copy:
                return (self.data.drop(index=index)).copy()
            else:
                return self.data.drop(index=index)

    def clean(self, fields=[], value=0, save=False):
        temp = self.data.copy()
        for field in fields:
            temp[field] = temp[field].fillna(value=value)
        if save:
            self.data = temp
        return temp

    def load(self, path='', type='EXCEL'):
        if type == 'CSV':
            self.data = pd.read_csv(path)
        else:
            self.data = pd.read_excel(path)

    def query(self, filter={}):
        temp = self.data.copy()
        for key in filter:
            temp = temp[temp[key] == filter[key]]
        return temp

    # def clustering(self, fields=[], k=1, n=200):

    # def predict(self, distance=EUCLIDEAN):