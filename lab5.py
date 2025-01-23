#%%
import itertools
import os
from pandas import DataFrame

textpath = 'C:/Users/HELLO/Downloads/Fontanka/texts'


list = []
for path, subdirs, files in os.walk(textpath):
    for name in files:
        if(len(list) < 200):
            file = os.path.join(path, name)
            with open(file, 'r', encoding="utf8") as f:
                data = f.read().replace('\n', '')
                list.append(data)

df = DataFrame({"Text": list})
df["id"]=df.index + 1

print(df)
#%%
import stanza
stanza.download('ru')
stanza_model = stanza.Pipeline(lang='ru', processors='tokenize,ner')
needed_types = ['ORG']
stanza_entities = []


for index, row in df.iterrows():
    doc = stanza_model(row.Text)
    ents = {}
    ents=  {ent.text for ent in doc.ents if (ent.type in needed_types and not ent.text in ents)}
    print(ents)
    stanza_entities.append(ents)
print(stanza_entities)
df['entities'] = stanza_entities
df2 = df[['id', 'entities']].copy()
df2 = df2.explode('entities').reset_index(drop=True)
nodes = []
for index, row in df2.iterrows():
    node = {"id": row["id"], "entity": row["entities"]}
    nodes.append((index, node))

edges = []
for pair in itertools.product(nodes, nodes):
    (first, second) = (pair[0][1], pair[1][1])
    edge = (pair[0][0], pair[1][0], {})
    if (first != second):
        if(first['id'] == second['id']):
            edge[2]['label'] = first['id']
        elif (first['entity'] == second['entity']):
            edge[2]['label'] = 'synonym'
        else:
            continue
        edges.append(edge)




