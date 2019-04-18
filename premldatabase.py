# Library Imports.
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from patsy import dmatrices
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
import time
from sqlalchemy import create_engine


CONTRACT = 'Dublin'
APIKEY = '7b9a350297fefef5f4147e65b6bc3114aacde014'
STATIONS = 'https://api.jcdecaux.com/vls/v1/stations'
DBURL = 'swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com'
PORT = '3306'
DB = 'dublin_bikes'
USER = 'swen_main_'
PASSWORD = 'mixednuts'




def get_models():
    # df = pd.read_csv('stations.csv')
    # engine = main.get_db()
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, DBURL, PORT, DB))

    nums = range(2, 116)
    for num in nums:
        if num==20:
            continue
        # df = pd.read_csv('stations.csv')
        # engine = main.get_db()
        df = pd.read_sql_query("select * from availability2 ",engine)
        #                        engine, params={"number": num})
        print(df.shape)

        # df = engine.execute("select * from availability2")
        df = df.loc[df.stationNUM ==num, :]
        print(df.shape)
        print(num)
        df['last_update2'] = pd.to_datetime(df.last_update, unit='ms')
        df['last_date'] = pd.to_datetime(df.last_update, unit='ms').dt.date
        df['hour'] = pd.to_datetime(df.last_update, unit='ms').dt.hour
        df['dayofweek'] = pd.to_datetime(df.last_update, unit='ms').dt.dayofweek
        df['dayofweek'] = df['dayofweek'].astype('category')
        df['hour'] = df['hour'].astype('category')
        cont_features = ['hour', 'dayofweek']
        X = df[cont_features]
        y = df.available_bikes
        X1 = pd.get_dummies(X, drop_first=True)
        multiple_linreg = LinearRegression().fit(X1, y)
#         multiple_linreg_predictions = multiple_linreg.predict(X1)
# # print("\nPredictions with multiple linear regression: \n")
#         X2=X1
#         X2['Predicted']=multiple_linreg_predictions
#         X2['Actual']=y
#         # actual_vs_predicted_multiplelinreg = ['Predicted', 'Actual']
#         # X3 = X2[actual_vs_predicted_multiplelinreg]
#         testActualVal=y
#         predictions=multiple_linreg_predictions
#         MAE=metrics.mean_absolute_error(testActualVal, predictions)
#         MSE=metrics.mean_squared_error(testActualVal, predictions)
#         RMSE=metrics.mean_squared_error(testActualVal, predictions) ** 0.5
#         R2= metrics.r2_score(testActualVal, predictions)

        # X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.3)
        # linreg = LinearRegression().fit(X_train, y_train)
        # # Predicted price on training set
        # train_predictions = linreg.predict(X_train)
        # test_predictions = linreg.predict(X_test)
        # scores = -cross_val_score(LinearRegression(), X1, y, scoring='neg_mean_absolute_error', cv=5)
        # metrics = ['neg_mean_absolute_error', 'neg_mean_squared_error', 'r2']
        # scores = cross_validatescores = cross_validate(LinearRegression(), X1, y, scoring=metrics, cv=5)
        # scores = cross_validate(LinearRegression(), X1, y, scoring=metrics, cv=5)
        linreg=multiple_linreg
        num = str(num)
        sta = "station"
        piclName = sta + num + ".pickle"
        with open('static/models22/'+piclName, 'wb') as f:
            pickle.dump(linreg, f)
        # restore
        # with open('save/clf.pickle', 'rb') as f:
        #     clf2 = pickle.load(f)
        #     print(clf2.predict(X[0:1]))
        # time.sleep(1)

    return "Models have been built sucessfully."
get_models()