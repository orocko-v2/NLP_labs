import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'http://www.lib.ru/SHAKESPEARE/shks_korio.txt'
res = urlopen(url)
doc = res.read().decode('koi8-r')

s = BeautifulSoup(doc,'html.parser')
text = s.pre.pre

scenes, texts, act, scene = [], [], 0, 0

for tag in text.children:
    if tag.name == 'ul':
        tagText = tag.get_text().lower()
        if ('акт' in tagText):
            act += 1
            scene = 0
        if ('сцена' in tagText):
            scene += 1
            sceneText = tag.next_sibling.get_text().lower()
            scenes.append(f'{act}{scene}')
            texts.append(sceneText)

df = DataFrame({"scene": scenes, "texts": texts})


def findNames(text):
    stop_words = {"и", "все", "оба"}
    names = re.findall(r'^\n\s+([^.,!?()\n]+)\n{2}', text, re.M)
    f_names = filter(lambda x: not (stop_words & set(x.split())), names)
    return set(f_names)

def countPairs(names, scene):
    c = 0
    names = {*names}
    for namePair in scene:
        if len(names & namePair)==2:
            c+=1
    return c

def fillDF(charSet, scene):
    list1=[]
    charSet = sorted(charSet)
    for first in charSet:
        list2 = []
        for second in charSet:
            pair = [first, second]
            c = countPairs(pair, scene)
            list2.append(c)
        list1.append(list2)
    df = DataFrame(list1, columns=charSet, index=charSet)
    return df

def create_Heatmap(dataframe):
    plt.matshow(dataframe, interpolation='nearest', cmap='GnBu')
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=10)

    # Устанавливаем метки по осям
    plt.gca().set_xticks(range(len(dataframe.columns)))
    plt.gca().set_yticks(range(len(dataframe.index)))

    # Устанавливаем метки осей
    plt.gca().set_xticklabels(dataframe.columns, rotation=90, fontsize=8)
    plt.gca().set_yticklabels(dataframe.index, fontsize=8)
    plt.title('Correlation Matrix', fontsize=16)
    plt.show()

df['names'] = df['texts'].apply(findNames)
charSet = set().union(*df['names'].values)

matrix= fillDF(charSet, df["names"])

create_Heatmap(matrix)


