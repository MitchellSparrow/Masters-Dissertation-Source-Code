from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import os
from globals import *
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from sklearn.model_selection import KFold

n_split = 10
DATA_PATH = 'LSTM_Data_test/'

label_map = {label: num for num, label in enumerate(SPONGE_CLASSIFICATIONS)}

sequences, labels = [], []
for action in SPONGE_CLASSIFICATIONS:
    for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
        window = []
        for frame_num in range(SEQUENCE_LENGTH):
            res = np.load(os.path.join(DATA_PATH, action, str(
                sequence), "{}.npy".format(frame_num)))
            window.append(res.flatten())
            #print(res)
        sequences.append(window)
        #print(window)
        labels.append(label_map[action])   


X = np.array(sequences)
print(X.shape)

y = to_categorical(labels).astype(int)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)


def create_model():
    model = Sequential()
    model.add(LSTM(64, return_sequences=True,
                   activation='relu', input_shape=(SEQUENCE_LENGTH, 480*640)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(SPONGE_CLASSIFICATIONS.shape[0], activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy',
                  metrics=['categorical_accuracy'])

    return model


# model = Sequential()
# model.add(LSTM(64, return_sequences=True,
#                activation='relu', input_shape=(30, 4)))
# model.add(LSTM(128, return_sequences=True, activation='relu'))
# model.add(LSTM(64, return_sequences=False, activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(actions.shape[0], activation='softmax'))


# model.compile(optimizer='Adam', loss='categorical_crossentropy',
#               metrics=['categorical_accuracy'])

best_model = create_model()
best_accuracy = 0

for train_index, test_index in KFold(n_split, shuffle=True).split(X_train):
    x_train, x_test = X_train[train_index], X_train[test_index]
    y_train, y_test = Y_train[train_index], Y_train[test_index]

    model = create_model()
    model.fit(x_train, y_train, epochs=5)

    evaluation = model.evaluate(x_test, y_test)
    accuracy = evaluation[1]
    loss = evaluation[0]

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        print('This model performed better')

    #print('Model evaluation ', model.evaluate(x_test, y_test))

# model.fit(X_train, y_train, epochs=300, callbacks=[tb_callback])

# print(model.summary())

print('\n\nBest Model Evaluation:\n\n')
print(best_model.summary())

best_model.save('models/lstm_model_2.h5')

yhat = best_model.predict(X_test)
ytrue = np.argmax(Y_test, axis=1).tolist()
yhat = np.argmax(yhat, axis=1).tolist()

print(multilabel_confusion_matrix(ytrue, yhat))
print(accuracy_score(ytrue, yhat))
