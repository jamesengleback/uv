import numpy as np
import pandas as pd

class Data:
    def __init__(self, path):
        self.path = path 
    @property
    def df(self):
        # clean df
        df = pd.read_csv(self.path)# dataframe object from csv
        headers = df.columns # save column headers
        df = df.iloc[1:,:] # trim top row
        df.columns = headers # replace with old headers
        df.index = df.iloc[:,0]
        ## remove wavelength cols
        df = df.iloc[:,1::2]
        ## remove machine info (remove nan rows)
        df = df.dropna()
        ## get sample names from headers
        ## col headers to sample names
        df.columns = headers[::2][:-1]
        # round wavelenths
        df.index = [round(float(i)) for i in df.index]
        return df.astype(float)

class BM3(Data):
    def __init_(self, path):
        super().__init__(path)

    @property
    def norm(self):
        return self.baselineCorr(self.norm800(self.df))
    @property
    def concs(self, ext = 95):
        df = self.norm
        A420 = df.loc[420,:]
        conc_uM = A420/ext *1000
        conc_uM.name = 'P450 conc/uM'
        return conc_uM
    def norm800(self, df):
        return df.subtract(df.loc[800,:],axis=1)
    def baselineCorr(self, df, baselineCol = 0):
        return df.subtract(df.iloc[:, baselineCol], axis = 0)

