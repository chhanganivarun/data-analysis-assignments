#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures


# In[2]:


from sklearn.decomposition import PCA

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

from sklearn.linear_model import LinearRegression, LogisticRegression


# In[3]:


# Train and test data paths will be available as env variables during evaluation
TRAIN_DATA_PATH = os.getenv("TRAIN_DATA_PATH")
TEST_DATA_PATH = os.getenv("TEST_DATA_PATH")


# # Train and test data paths will be available as env variables during evaluation
# TRAIN_DATA_PATH = './143e2751-7e99-4d17-bb9b-f0faec66e4b9_train.csv'
# TEST_DATA_PATH = './83f63b01-14ae-450d-98cb-328e9467162f_test.csv'

# In[7]:


# Prepare the training data
train_data = pd.read_csv(TRAIN_DATA_PATH)
X_train, y_train = train_data.iloc[:,:-1], train_data.iloc[:,-1]

# Train the model
classifier = GradientBoostingClassifier(n_estimators=15)
classifier.fit(X_train, y_train)

# Predict on the test set
test_data = pd.read_csv(TEST_DATA_PATH)
submission = classifier.predict(test_data)
submission = pd.DataFrame(submission)

# Export the prediction as submission.csv
submission.to_csv('submission.csv', header=['class'], index=False) 


# In[ ]:




