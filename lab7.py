import math
from collections import Counter

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

filepath = 'C:/Users/HELLO/Downloads/archive/Large Metal Lyrics Archive (LMLA) (fixed encoding removed non-lyrical elements language classification).csv'
df = pd.read_csv(filepath)

artist_list = {'SLIPKNOT', 'MOTIONLESS IN WHITE', 'ANNISOKAY', 'MEMPHIS MAY FIRE', 'ICE NINE KILLS','WARGASM','ASKING ALEXANDRIA', 'BRING ME THE HORIZON', 'SLAUGHTER TO PREVAIL', 'WHILE SHE SLEEPS'}

df2 = df[df['Artist'].isin(artist_list)]
df2 = df2[['Artist','Album', 'Song', 'Lyric']].copy()
df2 = df2.groupby('Artist').head(20)
df2 = df2[df2['Lyric'].notna()]

from nltk.corpus import stopwords
from string import punctuation

stopword = stopwords.words('english') + [a for a in punctuation]
stopword += ["i'm", "'m", "n't", "'re", "na", '...', '-', '—']

from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
word_tokenize = TweetTokenizer()

def removeStopsAndLemmatize(text):
    res = [word for word in text if word not in stopword and "'" not in word]
    res = [lemmatizer.lemmatize(word) for word in res]
    return res

def normalize(data):
    df_return = data.str.lower()
    df_return = df_return.apply(word_tokenize.tokenize)
    df_return = df_return.apply(removeStopsAndLemmatize)
    return df_return

df3 = df2.copy()
df3['Lyric'] = normalize(df3['Lyric'])

def tf(song):
    tf = {}
    for word, count in song.items():
        tf[word] = count / len(song)
    return tf

def idf(data):
    data_set = set.union(*[set(song.keys()) for song in data])
    idf = {}
    for word in data_set:
        count = [word for el in data if word in el.keys()].count(word)
        idf[word] = math.log(len(data)/ count, 10)
    return idf

def tfidf(docs):
    tfidf = []
    words = [dict(Counter(wrds)) for wrds in docs]
    iidf = idf(words)
    for words_ in words:
        ttf = tf(words_)
        res = {}
        for word in ttf.keys():
            res[word] = ttf[word] * iidf[word]
        tfidf.append(res)
    return tfidf

df4 = df3.copy()
df4['tfidf'] = tfidf(df3['Lyric'].tolist())

def merge(series):
    result = {}
    for dct in series.values:
        result.update(dct)
    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    return result

tfidfArtist = list(df4.groupby('Artist')['tfidf'].agg(merge).items())

import seaborn as sns
def createBarplots(data):
    fig, ax = plt.subplots(len(data) // 2, 2, figsize=(15, 30))
    fig.tight_layout(w_pad=10, h_pad=10)
    for index, (artist, tfidf) in enumerate(data):
        axes = ax[index // 2, index % 2]
        tfidf = dict(list(tfidf.items())[:9])
        sns.barplot(tfidf, x=tfidf.values(), y=tfidf.keys(), ax=axes).set_title(artist)
    plt.show()
createBarplots(tfidfArtist)
