import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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

class P450(Data):
    def __init_(self, path, extinction_coef=None):
        super().__init__(path)
        self.extinction_coef = extinction_coef

    @property
    def norm(self):
        return self.baselineCorr(self.norm800(self.df))
    def concs(self, extinction_coef=None):
        if extinction_coef is None:
            extinction_coef = self.extinction_coef
        df = self.norm
        A420 = df.loc[420,:]
        conc_uM = A420/extinction_coef*1000
        conc_uM.name = 'P450 conc/uM'
        return conc_uM
    def norm800(self, df):
        return df.subtract(df.loc[800,:],axis=1)
    def baselineCorr(self, df, baselineCol=0):
        return df.subtract(df.iloc[:, baselineCol], axis=0)

class BM3(Data):
    def __init_(self, path, **args):
        super().__init__(path, **args)
        self.extinction_coef = 95

def plot_traces(df, 
                title=None,
                save_path=None,
                ):
    plt.figure(figsize=(15,7)) # manually make canvas
    for col in df: # loop through columns
        plt.plot(df[col], # plot columns
                 label=col) # set trace label as col name - for legend

    plt.legend(loc='right') # detects 'label' in plot
    plt.xlabel('Wavelength nm')
    plt.ylabel('Absorbance')
    plt.ylim(-0.1,1)
    plt.xlim(250,800)
    plt.xticks(range(250,800,50)) # x axis ticks every 50 nm
    plt.title(title)
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()

def calc_concentrations(v1,v2, c1):
    return (c1*v1)/v2

def calc_change_a420_a390(x):
    x = x.subtract(x.iloc[:,0], axis =0)
    a420 = x.loc[420,:]
    a390 = x.loc[390]
    total_change = a420.abs() + a390.abs()
    return total_change

def r_squared(yi,yj):
    residuals = yi - yj
    sum_sq_residual = sum(residuals ** 2)
    sum_sq_total = sum((yi - yi.mean()) ** 2) # check this!!!
    return 1 - (sum_sq_residual / sum_sq_total)

def MichaelisMenten(x,y):
    y = y.replace(np.inf, 0) # error handling
    mm = lambda x, km, vmax, c : ((x * vmax) / (km + x)) + c
    try:
        (km, vmax, c), covariance = curve_fit(mm, x, y,
                bounds=((0, 0,0),(1e2,0.2,1)))
    except RuntimeError:
        km, vmax, c = np.inf, np.inf, np.inf

    yh = mm(x, km, vmax, c)
    rsq = r_squared(y, yh)
    return {'km':km, 'vmax':vmax, 'c':c, 'rsq':rsq}

