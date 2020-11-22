import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC

# Train and test data paths will be available as env variables during evaluation
TRAIN_DATA_PATH = os.getenv("TRAIN_DATA_PATH")
TEST_DATA_PATH = os.getenv("TEST_DATA_PATH")

# Prepare the training data
train_data = pd.read_csv(TRAIN_DATA_PATH)
X_train, y_train = train_data.iloc[:,:-1], train_data.iloc[:,-1]

# Train the model
classifier = SVC(gamma='auto')
classifier.fit(X_train, y_train)

# Predict on the test set
test_data = pd.read_csv(TEST_DATA_PATH)
submission = classifier.predict(test_data)
submission = pd.DataFrame(submission)

# Export the prediction as submission.csv
submission.to_csv('submission.csv', header=['class'], index=False) 
