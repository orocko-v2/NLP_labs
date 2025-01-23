import math
from collections import Counter
import numpy as np

import sklearn
from pandas import DataFrame
from sklearn.datasets import fetch_20newsgroups


categories = ['sci.space', 'sci.med', 'sci.crypt', 'sci.electronics']
train = fetch_20newsgroups(categories=categories)
print(train.filenames.shape)

category_list = []
for i in train.target:
    category_list.append(train.target_names[i])
print(category_list)

def lower(data):
    return data.lower()

from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer

def lowerr(data):
    return data.lower()

def removeStop(data):
    stopword = stopwords.words('english') + [a for a in punctuation]
    return [word for word in data if word not in stopword and '@' not in word]

def tokenize(data):
    word_tokenize = TweetTokenizer()
    return word_tokenize.tokenize(data)

def lemmatize(data):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in data]

def dataToDF(data):
    df = DataFrame()
    df = data.apply(lower) \
        .apply(tokenize) \
        .apply(removeStop) \
        .apply(lemmatize)
    return df

def TF(data):
    tf = {}
    for word, count in data.items():
        tf[word] = count / len(data)
    return tf

def IDF(data):
    data_set = set.union(*[set(song.keys()) for song in data])
    idf = {}
    for word in data_set:
        count = [word for el in data if word in el.keys()].count(word)
        idf[word] = math.log(len(data)/ count, 10)
    return idf

def tfidf(docs):
    tfidf = []
    words = [dict(Counter(wrds)) for wrds in docs]
    iidf = IDF(words)
    for words_ in words:
        ttf = TF(words_)
        res = {}
        for word in ttf.keys():
            res[word] = ttf[word] * iidf[word]
        tfidf.append(res)
    return tfidf

df = DataFrame({'Text': train.data,
                'Category': category_list})
df['Text'] = dataToDF(df['Text'])
df['TFIDF'] = tfidf(df['Text'].tolist())
print(df)
lexems = []
for text in df['TFIDF']:
    for word in text.keys():
        if word not in lexems:
            lexems.append(word)

print(len(lexems))

table = []
for text in df['TFIDF']:
    row = []
    for word in lexems:
        if word in text.keys():
            row.append(text.get(word))
        else:
            row.append(0)
    table.append(row)

print(np.asarray(table).shape)
print(df.groupby(['Category']).count())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
x_train, x_test, y_train, y_test = train_test_split(table, train.target, test_size=0.3, random_state=0)
print(y_train.shape, y_test.shape)
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

print('svc')
svc = svm.SVC()
svc.fit(x_train, y_train)
svc_pred = svc.predict(x_test)
print(metrics.accuracy_score(y_test, svc_pred))
print(metrics.classification_report(svc_pred, y_test, target_names = train.target_names))
print('---------------------------------------')

print('linear')
sgd = SGDClassifier(random_state=42)
sgd.fit(x_train, y_train)
sgd_pred = sgd.predict(x_test)
print(metrics.accuracy_score(y_test, sgd_pred))
print(metrics.classification_report(sgd_pred, y_test, target_names = train.target_names))
print('---------------------------------------')

print('neighbors')
kneighbors = KNeighborsClassifier(n_neighbors=1, weights='uniform')
kneighbors.fit(x_train, y_train)
kneighbors_pred = kneighbors.predict(x_test)
print(metrics.accuracy_score(y_test, kneighbors_pred))
print(metrics.classification_report(kneighbors_pred, y_test, target_names = train.target_names))
print('---------------------------------------')

print('tree')
tree = DecisionTreeClassifier()
tree.fit(x_train, y_train)
tree_pred = tree.predict(x_test)
print(metrics.accuracy_score(y_test, tree_pred))
print(metrics.classification_report(tree_pred, y_test, target_names = train.target_names))
print('---------------------------------------')

print('random forest')
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier()
forest.fit(x_train, y_train)
forest_pred = forest.predict(x_test)
print(metrics.accuracy_score(y_test, forest_pred))
print(metrics.classification_report(forest_pred, y_test, target_names = train.target_names))

