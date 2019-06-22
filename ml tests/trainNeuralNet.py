"""Trains a convolusional neural network on the 
   EMNIST dataset for handwritten diget recognition
"""
import tensorflow as tf
import numpy
import os
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

numClasses = 10
imgX = 28
imgY = 28

#change these if you want to train with different data
trainDirectories = ['EMNISTdata/digits/training', 'EMNISTdata/MNIST/training']
testDirectories = ['EMNISTdata/digits/testing', 'EMNISTdata/MNIST/testing']
x_train = []
y_train = []
x_test = []
y_test = []

#load image and label data into their respective lists
for directory in trainDirectories:
    for i in range(numClasses):
        newDirectory = os.path.join(directory, str(i))
        newDirectory= newDirectory.replace('\\', '/')
        print(newDirectory)
        for filename in os.listdir(newDirectory):
            if filename.endswith(".png"):
                newPath = os.path.join(newDirectory, filename)
                newPath = newPath.replace('\\', '/')
                print(newPath)
                img = load_img(newPath, grayscale=True, target_size=(imgX, imgY))
                img = img_to_array(img)
                img = img.reshape(imgX, imgY, 1)
                x_train.append(img)
                y_train.append(i)

for directory in testDirectories:
    for i in range(numClasses):
        newDirectory = os.path.join(directory, str(i))
        newDirectory= newDirectory.replace('\\', '/')
        print(newDirectory)
        for filename in os.listdir(newDirectory):
            if filename.endswith(".png"):
                newPath = os.path.join(newDirectory, filename)
                newPath = newPath.replace('\\', '/')
                print(newPath)
                img = load_img(newPath, grayscale=True, target_size=(imgX, imgY))
                img = img_to_array(img)
                img = img.reshape(imgX, imgY, 1)
                x_test.append(img)
                y_test.append(i)

print("train data length: ", str(len(x_train)))
print("train label length: ", str(len(y_train)))
print("test data length: ", str(len(x_test)))
print("test label length: ", str(len(y_test)))
x_train = numpy.array(x_train, dtype="float32")/255.0
x_test = numpy.array(x_test, dtype="float32")/255.0
y_train = numpy.array(y_train)
y_test = numpy.array(y_test)

y_train = to_categorical(y_train, numClasses)
y_test = to_categorical(y_test, numClasses)

print('x_train shape:', x_train.shape)
print('Number of images in x_train', x_train.shape[0])
print('Number of images in x_test', x_test.shape[0])

model = Sequential()
model.add(Conv2D(32, (5, 5), input_shape=(x_train.shape[1], x_train.shape[2], 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(numClasses, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, batch_size=200)

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#serialize model to json
jsonModel = model.to_json()
with open("model.json", "w") as jsonFile:
    jsonFile.write(jsonModel)

#serialize weights to HDF5
model.save_weights("model.h5")
print("saved model to disk")