# -*- coding: utf-8 -*-
"""Dataset2_news_articles.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NblosR0OP6BbFcjoWGHdwMF8iMWj1Tbp
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import nltk 
import re
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns 
import sklearn.metrics
import sklearn
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import nltk
nltk.download('stopwords')

"""Read news aricle csv file"""

data = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/ML Freelance/news_articles.csv', encoding="latin", index_col=0)
data = data.dropna()
data.count()



"""EDA"""

data.groupby('label').describe()

data=data.dropna()

# Seperating Independent and dependent features
X = data.drop(columns=['label'],axis=1)
y = data['label']

data.head()

data['text_len'] = data['text'].apply(len)

data['len_title'] = data['title'].apply(len)

import seaborn as sns
import matplotlib.pyplot as plt

# Plot article type distribution
df_type = data['type'].value_counts()
sns.barplot(np.arange(len(df_type)), df_type)
plt.xticks(np.arange(len(df_type)), df_type.index.values.tolist(), rotation=90)
plt.title('Article type count', fontsize=20)
plt.show()

from nltk.corpus import stopwords
import string
stopwords.words('english')[0:10] # Show some stop words

def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Perform lemmatization
    4. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
    lemma = nlp.WordNetLemmatizer()
    nopunc = [ lemma.lemmatize(word) for word in nopunc]

data['title'].apply(text_process)

data['text'].head(5).apply(text_process)

from sklearn.feature_extraction.text import CountVectorizer
bow_transformer = CountVectorizer(analyzer=text_process).fit(data['text'])

# Print total number of vocab words
print(len(bow_transformer.vocabulary_))

messages_bow = bow_transformer.transform(data['text'])

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer().fit(messages_bow)

messages_tfidf = tfidf_transformer.transform(messages_bow)
print(messages_tfidf.shape)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

y = le.fit_transform(data.label)

"""Training & Testing"""

from sklearn.model_selection import train_test_split

X_train, X_test, label_train, label_test = train_test_split(data['text'], y, test_size=0.2, random_state = 42)

print(len(X_train), len(X_test), len(X_train) + len(X_test))

"""# Naive Bayes"""

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(messages_tfidf, data['label'])

pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])

pipeline.fit(X_train,label_train)

predictions1 = pipeline.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(predictions1,label_test))

"""Random Forest"""

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=50, criterion='entropy',random_state=0)
classifier.fit(messages_tfidf, data['label'])

pipeline_rf = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', RandomForestClassifier()),  # train on TF-IDF vectors w/ SVM
])

pipeline_rf.fit(X_train,label_train)

predictions2 = pipeline_rf.predict(X_test)

print(classification_report(predictions2,label_test))

"""DT"""

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=42, criterion="entropy",
                             min_samples_split=10, min_samples_leaf=10, max_depth=3, max_leaf_nodes=5)

pipeline_dt = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', DecisionTreeClassifier()),  # train on TF-IDF vectors w/ SVM
])

pipeline_dt.fit(X_train,label_train)

predictions_dt = pipeline_dt.predict(X_test)

print(classification_report(predictions_dt,label_test))

"""Gradient Boosting

svm
"""

from sklearn.svm import LinearSVC
svm=LinearSVC()

pipeline_svm = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', LinearSVC()),  # train on TF-IDF vectors w/ SVM
])

pipeline_svm.fit(X_train,label_train)

predictions_svm = pipeline_gbm.predict(X_test)

print(classification_report(predictions_svm,label_test))