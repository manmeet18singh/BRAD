import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import Imputer, scale
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

# Read in dataset and drop id/unnamed columns as they're useless

df = pd.read_csv("../datasets/updated.csv")
df = df.drop(columns=['Unnamed: 0'])

# Predicter variables. Everything but the diagnosis
X = df.drop('diagnosis', axis=1).values
# Target variable. The diagnosis
y = df['diagnosis'].values


# Drop all 0's and replace with NaN's
X[X == 0] = np.nan

# --- Random Forest Instantiation --- #
rf = RandomForestClassifier(
    criterion='entropy', max_depth=10000, n_estimators=100, max_features='auto')

# --------- PREPROCESSING --------- #

# Use sklearn imputer to fill in all NaNs with mean from each column
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(X)
X = imp.transform(X)

# Normalize X values using sklearn scale (standardization)
X = scale(X)

# Fit rf model
rf.fit(X,y)

# --------- TESTING --------- #

# Hyperparam Tuning
# param_grid = {'n_estimators': [1, 10, 100, 1000, 10000],
#               'max_features': ['sqrt', 'log2'],
#               'max_depth' : [1, 10, 100, 1000, 10000],
#               'criterion' :['gini', 'entropy']
# }
# clf = GridSearchCV(RandomForestClassifier(), param_grid, cv=5, n_jobs=-1)
# clf.fit(X, y)
# best_params = clf.best_params_
# print(best_params, '%.3f'%(clf.best_score_ * 100) + '%')

# Confusion Matrix
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# rf.fit(X_train, y_train)
# y_pred = rf.predict(X_test)
# confusion = confusion_matrix(y_test, y_pred)
# print(confusion)

# 5-Fold CV
# scores = cross_val_score(rf, X, y, cv=5)
# accuracy = np.mean(scores)
# print('Current Accuracy: ' + '%.3f' % (accuracy * 100) + "%")

# --------- PRODUCTION --------- #

def brad(X):
    # print(X)
    y_pred = rf.predict(X)
    # print('BRAD says: ' + str(y_pred))

    if y_pred == 0:
        return 'benign'
    else:
        return 'malignant'

def main():
    X_new = []

    inFile = open("../brad/temp.txt", "r")

    vector = inFile.read()

    X_new = np.fromstring(vector, sep=" ")

    X_new = X_new.reshape(1,-1)
    result = brad(X_new)
    print('BRAD says: ' + result)
#
if __name__ == "__main__":
    main()
