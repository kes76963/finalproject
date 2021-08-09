import pandas as pd
import re
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from konlpy.tag import Okt

pd.set_option('display.unicode.east_asian_width',True)

#사전 전처리
def preprocess_nlp(path):
    df = pd.read_csv(path)
    df = df.drop_duplicates(['copy'])
    df.reset_index(drop=True, inplace=True)
    copy_list = []
    for copy in df['copy']:
        copy_list.append(re.compile('[^가-힣a-zA-Z0-9]').sub(' ', copy))
    df['copy'] = copy_list
    df.to_csv('./datasets/slogan_category2.csv', index = None, encoding='utf-8-sig')
    print('완료')

preprocess_nlp('./datasets/slogan_category.csv')

#중복 확인
df = pd.read_csv('./datasets/slogan_category2.csv')
col_dup = df['copy'].duplicated()
print(col_dup)
sum_dup = df['copy'].duplicated().sum()
print(sum_dup)


df = df.drop_duplicates(subset=['copy'])
sum_dup = df['copy'].duplicated().sum()
print(sum_dup)

df.reset_index(drop=True, inplace=True)

X = df['copy']
Y = df['category']

#라벨인코딩
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
label = encoder.classes_
print(label)

#피클로 저장
with open('./models/category_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

print(labeled_Y)

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

okt = Okt()
print(type(X))
okt_X = okt.morphs(X[0])
print(X[0])
print(okt_X)


for i in range(len(X)):
    X[i] = okt.morphs(X[i])
print(X)

stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)

print(stopwords.head(30))

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

token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])

with open('./datasets/copy_token.pickle', 'wb') as f:
    pickle.dump(token, f)

wordsize = len(token.word_index) + 1
print(wordsize)

max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)
print(X_pad[:10])

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./datasets/copy_data_max_{}_size_{}'.format(max, wordsize), xy)

#"""