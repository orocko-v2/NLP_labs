from deeppavlov import build_model
import spacy
import stanza
import lab3

tags = {

    'ADJ': 'adjective',
    'ADP': 'adposition',
    'ADV': 'adverb',
    'AUX': 'auxiliary',
    'CCONJ': 'coordinating conjunction',
    'DET': 'determiner',
    'INTJ': 'interjection',
    'NOUN': 'noun',
    'NUM': 'numeral',
    'PART': 'particle',
    'PRON': 'pronoun',
    'PROPN': 'proper noun',
    'PUNCT': 'punctuation',
    'SCONJ': 'subordinating conjunction',
    'SYM': 'symbol',
    'VERB': 'verb',
    'X': 'other',
}
# spacy_model = spacy.load('de_core_news_sm')
# doc = spacy_model(lab3.list[0])
# for token in doc:
#     if not token.is_stop and not token.is_space:
#         print(token.text, token.pos_, tags.get(token.pos_))
# #
# import re
#
# txt = lab3.list[0]
# print(txt)
# input = [sen for sen in re.split('\.|!|\?|\n', txt) if len(sen)>0]
# print(input)
# ner_model = build_model('ner_ontonotes_bert_mult')
#
# for i in input:
#     print(ner_model([i]))





stanza_model = stanza.Pipeline(lang='de', processors='tokenize, mwt, ner')
doc2 = stanza_model(lab3.list[0])
print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in doc2.ents], sep='\n')