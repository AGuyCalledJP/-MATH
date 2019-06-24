"""Allows the user to test the neural network
   on images of their choosing
"""
import numpy
import os
import tensorflow as tf
from keras.models import model_from_json
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img

#Run NN to deduce what were working with
def PinkyAnd():
   #Load the neural net in from json file
   jsonFile = open('model.json', 'r')
   loadedJsonModel = jsonFile.read()
   jsonFile.close()
   loadedModel = model_from_json(loadedJsonModel)

   #Load the neural net weights
   loadedModel.load_weights("model.h5")
   loadedModel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

   #Set name of file which is going to be grabbed and analyzed
   filename = "/run.png"

   img = load_img(str(os.getcwd()) + filename, grayscale=True, target_size=(28, 28))
   img = img_to_array(img)
   img = img.reshape(1, 28, 28, 1)
   img = img.astype('float32')
   img = img / 255.0
   return loadedModel.predict_classes(img)