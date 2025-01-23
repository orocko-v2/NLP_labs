import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import pymorphy2

def jaccard_Distance(set1, set2):
    intersection = len(set1.intersection(set2))
    union=len(set1.union(set2))
    return (intersection / union)

def create_Heatmap(dataframe):
    plt.matshow(dataframe, interpolation='nearest')
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Correlation Matrix', fontsize=16)
    plt.show()

def open_File(file_path):
    df = pd.read_excel(file_path, sheet_name=0, header=0)
    texts = df[df.columns[0]].tolist()
    return texts

def normalize_Texts(texts):
    return_texts = []
    for text in texts:
        set_text = set()
        text = text.lower()
        words = word_tokenize(text)
        stopword = stopwords.words('russian') + [a for a in punctuation]
        words2 = [word for word in words if word not in stopword]
        morph = pymorphy2.MorphAnalyzer()
        for ii in range(len(words2)):
            words2[ii] = morph.parse(words2[ii])[0].normal_form
        for word in words2:
            set_text.add(word)
        return_texts.append(set_text)
    return return_texts

def jaccard_Distance_All_Sets(texts):
    list = []
    for text in texts:
        list2 = []
        for text2 in texts:
            res = jaccard_Distance(text, text2)
            if texts.index(text) == texts.index(text2):
                res = 0
            list2.append(res)
        list.append(list2)
    return pd.DataFrame(list)

texts = open_File("data/texts.xlsx")
print(jaccard_Distance_All_Sets(normalize_Texts(texts)))
# create_Heatmap(jaccard_Distance_All_Sets(normalize_Texts(texts)))
