import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge,Lasso

data=pd.read_hdf('feats.hdf','data')
x_train=data.drop(['area','name','unit_price','price','address','room_type','all_floor','Plate','PropertyID','floor_section','Module'],axis=1)
y_train=data.loc[x_train.index].unit_price
linreg = LinearRegression()
model=linreg.fit(x_train, y_train)
joblib.dump(model,'test.model')
