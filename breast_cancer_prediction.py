# -*- coding: utf-8 -*-
"""Breast Cancer Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13OJ6ZMd80aEWVyTCbkV9vFMST3AxMoud

# **PREPARATION**



1.   Instalasi dan declarasi library
2.   Download dataset
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import pandas as pd 

# %matplotlib inline 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold   
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

!pip install kaggle

import os
os.environ['KAGGLE_USERNAME'] = "luthfanhadihilsan" 
os.environ['KAGGLE_KEY'] = "40c524dbf7d7d256cd53e34126e5f256" 
!kaggle datasets download -d uciml/breast-cancer-wisconsin-data

import zipfile,os
local_zip = '/content/breast-cancer-wisconsin-data.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/data')
zip_ref.close()

"""# **LOAD DATA**


1.   Explore data
2.   Feature distribution
3.   Target encoding
4.   Split train and test data


"""

import pandas as pd

data = pd.read_csv('/content/data/data.csv')

print(data.info())

data.drop('id',axis=1,inplace=True)
data.drop('Unnamed: 32',axis=1,inplace=True)
# size of the dataframe
len(data)

print(data.diagnosis.unique())
data['diagnosis'] = data['diagnosis'].map({'M':1,'B':0})
print(data.head())

data.describe()

count = data['diagnosis'].value_counts()
print(count)

#plt.bar()
plt.bar(['B','M'],count)
plt.title('Diagnosis')
plt.show()

feature_mean = list(data.columns[1:11])
datam = data[data['diagnosis'] == 1]
datab = data[data['diagnosis'] == 0]

#Stack the data
plt.rcParams.update({'font.size': 8})
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8,10))
axes = axes.ravel()
for idx,ax in enumerate(axes):
    ax.figure
    binwidth= (max(data[feature_mean[idx]]) - min(data[feature_mean[idx]]))/50
    ax.hist([datam[feature_mean[idx]],datab[feature_mean[idx]]], bins=np.arange(min(data[feature_mean[idx]]), max(data[feature_mean[idx]]) + binwidth, binwidth) , alpha=0.5,stacked=True, label=['M','B'],color=['r','g'])
    ax.legend(loc='upper right')
    ax.set_title(feature_mean[idx])
plt.tight_layout()
plt.show()

traindata, testdata = train_test_split(data, test_size = 0.2)

"""# **PREDICTIVE MODEL**



1.   Create funtion for training and validation
2.   Logistic Regression
3.   RandomForestClassifier


"""

from sklearn.model_selection import cross_validate
def cross_validation(model, _X, _y, _cv=5):
      '''Function to perform 5 Folds Cross-Validation
       Parameters
       ----------
      model: Python Class, default=None
              This is the machine learning algorithm to be used for training.
      _X: array
           This is the matrix of features.
      _y: array
           This is the target variable.
      _cv: int, default=5
          Determines the number of folds for cross-validation.
       Returns
       -------
       The function returns a dictionary containing the metrics 'accuracy', 'precision',
       'recall', 'f1' for both training set and validation set.
      '''
      _scoring = ['accuracy', 'precision', 'recall', 'f1']
      results = cross_validate(estimator=model,
                               X=_X,
                               y=_y,
                               cv=_cv,
                               scoring=_scoring,
                               return_train_score=True)
      
      return {"Training Accuracy scores": results['train_accuracy'],
              "Mean Training Accuracy": results['train_accuracy'].mean()*100,
              "Training Precision scores": results['train_precision'],
              "Mean Training Precision": results['train_precision'].mean(),
              "Training Recall scores": results['train_recall'],
              "Mean Training Recall": results['train_recall'].mean(),
              "Training F1 scores": results['train_f1'],
              "Mean Training F1 Score": results['train_f1'].mean(),
              "Validation Accuracy scores": results['test_accuracy'],
              "Mean Validation Accuracy": results['test_accuracy'].mean()*100,
              "Validation Precision scores": results['test_precision'],
              "Mean Validation Precision": results['test_precision'].mean()*100,
              "Validation Recall scores": results['test_recall'],
              "Mean Validation Recall": results['test_recall'].mean()*100,
              "Validation F1 scores": results['test_f1'],
              "Mean Validation F1 Score": results['test_f1'].mean()*100
              }

def classification_model(model, data, data_test, predictors, outcome):
  
  model.fit(data[predictors],data[outcome])
 
  predictions = model.predict(data[predictors])

  accuracy = metrics.accuracy_score(predictions,data[outcome])
  print("Accuracy : %s" % "{0:.3%}".format(accuracy))

  validation = cross_validation(model, data_test[predictors], data_test[outcome])
  print('Model mean-Accuracy score with cross validation : ',validation['Mean Validation Accuracy'])
  print('Model mean-Precision score with cross validation : ',validation['Mean Validation Precision'])
  print('Model mean-Recall score with cross validation : ',validation['Mean Validation Recall'])
  print('Model mean-F1 score with cross validation : ',validation['Mean Validation F1 Score'])
  model.fit(data[predictors],data[outcome])

predictor_var = ['radius_mean','perimeter_mean','area_mean','compactness_mean','concave points_mean']
outcome_var='diagnosis'
model=LogisticRegression()
classification_model(model,traindata,testdata,predictor_var,outcome_var)

predictor_var = feature_mean
print(predictor_var)
model = RandomForestClassifier(n_estimators=100,min_samples_split=25, max_depth=7, max_features=2)
classification_model(model, traindata,testdata ,predictor_var,outcome_var)