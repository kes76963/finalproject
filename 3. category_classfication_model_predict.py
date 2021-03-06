# -*- coding: utf-8 -*-
"""prj01_news_category_classfication_04_model_predict

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JSoYkXIDhCoHwMTWPGlZhhdvEZi-BcUi
"""

#!pip install konlpy

import pandas as pd
import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
import pickle
from konlpy.tag import Okt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences

pd.set_option('display.unicode.east_asian_width', True)

model = load_model('/content/news_classfication_0.7437223196029663.h5')

with open('/content/news_token.pickle', 'rb') as f :
  token = pickle.load(f)

with open('/content/category_encoder.pickle', 'rb') as f:
  encoder = pickle.load(f)
category = encoder.classes_
print (category)

df_news_today = pd.read_csv('/content/naver_news_titles_210617_headline.csv', index_col=0)
print(df_news_today.head())

df_news_today.info()

df = df_news_today.drop_duplicates(subset=['title'])
sum_dup = df.title.duplicated().sum()
print(sum_dup)

df.info()

#중복 제거 후에 인덱스 빈 값을 없앤다
df.reset_index(drop=True, inplace=True)

X = df['title']
Y = df['category']

print(X[1])

####실행하면 안 됨
"""
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
label = encoder.classes_
print(label)


labeled_Y = encoder.transform(Y)
print(labeled_Y)

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)
"""





okt = Okt()
print(type(X))
okt_X = okt.morphs(X[1])
print(X[1])
print(okt_X)

for i in range(len(X)):
  X[i] = okt.morphs(X[i])
print(X)

stopwords = pd.read_csv('/content/stopwords.csv')

words = []
for word in okt_X:
    if word not in list(stopwords['stopword']):
        words.append(word)
print(words)

for i in range(len(X)):
    result = []
    for j in range(len(X[i])):
        if len(X[i][j]) > 1:
            if X[i][j] not in list(stopwords['stopword']):
                result.append(X[i][j])
    X[i] = ' '.join(result)
print(X)

#token = Tokenizer()
#token.fit_on_texts(X) 절대 하면 안 된다
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])

X_pad = pad_sequences(tokened_X, 27)
print(X_pad[:10])

predict = model.predict(X_pad)
print(predict[0])

result = np.argmax(predict[0])
print(category[result])

predict_category = []
for pred in predict :
  predict_category.append(category[np.argmax(pred)])
print(predict_category)
print(len(predict_category))

df['predict'] = predict_category
print(df_news_today.head())

df['OX'] = 'O'
print(df.head())

for i in range(len(df.predict)):
  if df.category[i] == df.predict[i]:
    df.OX[i] = 'O'
  else:
    df.OX[i] = 'X'
print(df.head())

print(df.OX.value_counts())

print(df.OX.value_counts()/ len(df.OX))

df.iloc[-30:, 0:3]