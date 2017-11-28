from __future__ import print_function
from keras.preprocessing import sequence
from keras.models import Sequential, load_model, Model
from keras.layers import Dense, TimeDistributed, Input, Dropout, Activation
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.optimizers import SGD
import random
import numpy as np
import time
import pickle

batch_size = 100
x_length = 12
max_risk = 2 #0~13, 14
log_length = 10

print('Loading data...')
s = time.time()
f = open("sex_age.data", "rb")
datas = pickle.load(f)
f.close()
print("[+] Loading data Done! (%s)"%(time.time() - s))

print('Build model...')

deepth = 60
dropout_rate = 0.5
s = time.time()
model = Sequential()
model.add(Dense(deepth ,input_dim=x_length, activation="relu"))
model.add(Dropout(dropout_rate))
model.add(Dense(deepth, activation="relu"))
model.add(Dropout(dropout_rate))
model.add(Dense(deepth, activation="relu"))
model.add(Dense(max_risk, activation='softmax'))

# try using different optimizers and different optimizer configs
#opt = SGD(lr=1e-2)
#binary_crossentropy
model.compile(loss=['categorical_crossentropy', 'binary_crossentropy'][0],
              optimizer=['adam', 'rmsprop'][1],
              metrics=['accuracy'])

print(model.summary())
print("[+] Build model Done! (%s)"%(time.time() - s))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def scale(value, maxValue, minValue = 0):
    if value >= maxValue:
        return 1
    return translate(value, minValue, maxValue, 0, 1)

def make_item(item):
    item[0] = scale(item[0], 200)
    item[1] = scale(item[1], 120)
    item[2] = scale(item[2], 100)
    item[3] = scale(item[3], 2.5)
    item[4] = scale(item[4], 2.5)
    item[5] = scale(item[5], 2)
    item[6] = scale(item[6], 2)
    item[7] = scale(item[7], 140, 60)
    item[8] = scale(item[8], 100, 40)
    item[9] = scale(item[9], 16, 10)
    if item[10] == 1:
        item[10] = 0
    elif item[10] == 2:
        item[10] = 1
    elif item[10] == 3:
        item[10] = 0.5
    return item

for sex in ["1", "2"]:# male, female
    for age in range(1, 25):
        data_length = len(datas[sex][str(age)])
        print("%s|%s|data_length: %s"%(sex,age,data_length))
        if data_length < 100:
            continue
        x_datas = []
        y_datas = []
        err_cnt = 0
        for data in datas[sex][str(age)]:
            try:
                item = list(map(float, data[0]))
                item = make_item(item)
                #filtered_item = [item[0], item[1], item[7], item[8], item[9], item[10], item[11]]
                x_datas.append(item)
                y = int(float(data[1])/3)
                y = 1 if y else 0
                y_datas.append(y)
            except Exception as e:
                print(e)
                err_cnt += 1
        print(err_cnt)
        y_datas = to_categorical(y_datas, max_risk)
        x_datas = np.asarray(x_datas)
        y_datas = np.asarray(y_datas)

        x_train, x_test, y_train, y_test = train_test_split(x_datas, y_datas, test_size=0.2,
                                                            random_state=random.randint(0, 1000))

        print('x_train shape:', x_train.shape)
        print('x_test shape:', x_test.shape)

        #model.reset_states()

        print('Train...')
        model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=5,
                  validation_data=(x_test, y_test))
        #bad_data = np.asarray([[140, 140, 100, 15, 0.333, 1]])
        '''
        bad_data = np.asarray([make_item([160, 100, 100, 0.1, 0.1, 1, 1, 140, 80, 16, 1, 1])])
        a = model.predict(bad_data)
        print(a[0])
        print(model.predict(np.asarray([x_datas[0]]))[0])
        a=b
        for fuck in x_train:
            a = np.argmax(model.predict(np.asarray([fuck])))
            b = model.predict_classes(np.asarray([fuck]))
            print(a, b, a==b)
        '''
        model.save("models\\%s_%s_model.h5"%(sex, age))
        score, acc = model.evaluate(x_test, y_test,
                                    batch_size=batch_size)



'''
model = load_model("model.h5")
fuck = np.asarray([[[0.98, 0.0, 68.14, 30.36, 25.0, 12.62, 12.62, 12.5, 12.5, 12.62], [4.78433, 4.76871, 5.17916, 5.22894, 5.23529, 5.58424, 5.6106, 5.61694, 5.65257, 5.63793]]])
print(fuck.shape)
data = model.predict(fuck)
print(data)
import tensorflow
print(tensorflow.__version__)'''