import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# X_train and y_train are the training data
model = LinearRegression()
model.fit(X_train, y_train)
# Serialize model object into a file called model.pkl on disk using pickle
with open('model.pkl', 'wb') as handle:
    pickle.dump(model, handle, pickle.HIGHEST_PROTOCOL)
# pickle.HIGHEST_PROTOCOL using the highest available protocol
# (we used wb to open file as binary and use a higher pickling protocol)



# de-serialize model.pkl file into an object called model using pickle
with open('model.pkl', 'rb') as handle:
    model = pickle.load(handle)