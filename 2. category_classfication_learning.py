
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './datasets/copy_data_max_10_size_9256.npy',
    allow_pickle=True)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# model = Sequential()
# model.add(Embedding(9256, 300, input_length=10))
# model.add(Conv1D(32, kernel_size=5,
#             padding='same', activation='relu'))
# model.add(MaxPool1D(pool_size=1))
# model.add(LSTM(128, activation='tanh',
#                return_sequences=True))
# model.add(Dropout(0.3))
# model.add(LSTM(64, activation='tanh',
#                return_sequences=True))
# model.add(Dropout(0.3))
# model.add(LSTM(64, activation='tanh'))
# model.add(Dropout(0.3))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# model.add(Dense(18, activation='softmax'))

model = Sequential()
model.add(Embedding(9256, 300, input_length=10))
model.add(Conv1D(32, kernel_size=5,
            padding='same', activation='relu'))
model.add(MaxPool1D(pool_size=1))
model.add(LSTM(64, activation='tanh',
               return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(18, activation='softmax'))

print(model.summary())

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=100,
        epochs=50, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test)
print(score[1])

model.save('./models/news_classfication_{}.h5'.format(score[1]))