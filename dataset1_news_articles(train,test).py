# -*- coding: utf-8 -*-
"""Dataset1_news_articles(train,test).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PIJQZ5JRN0_ZmzTrRDS_7PHzoH8q_8M7
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
from matplotlib import rcParams
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

"""Read news aricle csv file"""

import csv
train = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ML Freelance/train.csv')
train.head()

import csv
test = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ML Freelance/test.csv')
test.head()

# Veri setlerimizin boyutları ; 
print(f"Train Shape : {train.shape}")
print(f"Test Shape : {test.shape}")

train.info()

train.isnull().sum()

train.dtypes.value_counts()

"""visualize"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize = (9,9))
sorted_counts = train['label'].value_counts()
plt.pie(sorted_counts, labels = sorted_counts.index, startangle = 90, counterclock = False, wedgeprops = {'width' : 0.6},
       autopct='%1.1f%%', pctdistance = 0.7, textprops = {'color': 'black', 'fontsize' : 18}, shadow = True,
        colors = sns.color_palette("Paired")[7:])
plt.text(x = -0.35, y = 0, s = 'Total Value: {}'.format(train.shape[0]))
plt.title('Distribution of News in the Data Set', fontsize = 16);

"""Preprocessing"""

train.dropna(inplace=True)

train.reset_index(inplace=True)

test.isnull().sum()

test['text'].fillna('TEST',inplace=True)

test.text.isnull().sum()

test=test.fillna(' ')
train=train.fillna(' ')
test['total']=test['title']+' '+test['author']+test['text']
train['total']=train['title']+' '+train['author']+train['text']

transformer = TfidfTransformer(smooth_idf=False)
count_vectorizer = CountVectorizer(ngram_range=(1, 2))
counts = count_vectorizer.fit_transform(train['total'].values)
tfidf = transformer.fit_transform(counts)

targets = train['label'].values
test_counts = count_vectorizer.transform(test['total'].values)
test_tfidf = transformer.fit_transform(test_counts)

"""Training & Testing"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(tfidf, targets, random_state = 42)

"""# **Naive Bayes**"""

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(tfidf, targets)



pipeline = Pipeline([
     # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])



pipeline.fit(X_train,y_train)

predictions1 = pipeline.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(predictions1,y_test))

"""Random Forest"""

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
spam_detect_model = RandomForestClassifier(n_estimators=50, criterion='entropy',random_state=0)

pipeline_rf = Pipeline([
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', RandomForestClassifier()),  # train on TF-IDF vectors w/ SVM
])

pipeline_rf.fit(X_train,y_train)

predictions2 = pipeline_rf.predict(X_test)

print(classification_report(predictions2,y_test))

"""DT"""

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=42, criterion="entropy",
                             min_samples_split=10, min_samples_leaf=10, max_depth=3, max_leaf_nodes=5)

pipeline_dt = Pipeline([
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', DecisionTreeClassifier()),  # train on TF-IDF vectors w/ DT
])

pipeline_dt.fit(X_train,y_train)

predictions_dt = pipeline_dt.predict(X_test)

print(classification_report(predictions_dt,y_test))

"""SVM"""

from sklearn.svm import LinearSVC
svm=LinearSVC()

pipeline_svm = Pipeline([
  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', LinearSVC()),  # train on TF-IDF vectors w/ SVM
])

pipeline_svm.fit(X_train,y_train)

predictions_svm = pipeline_gbm.predict(X_test)

print(classification_report(predictions_svm,y_test))